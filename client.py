#!/usr/bin/env python3

# WS client example

import asyncio
import json
import websockets
from pprint import pprint


async def get_ticker():
    url = "wss://ws.kraken.com"
    # url = "wss://ws-feed.gdax.com"
    # url = "ws://localhost:8765"
    try:
        async with websockets.connect(url) as websocket:

            # subscribe_msg = {
            #     "type": "subscribe",
            #     "product_ids": ['BTC-USD'],
            #     "channels": ["ticker"]
            # }

            subscribe_msg = {
                "event": "subscribe",
                "pair": ["XBT/EUR"],
                "subscription": {"name": "ticker"},
            }

            await websocket.send(json.dumps(subscribe_msg))

            last = 0
            channel_id = 0

            async for data in websocket:
                global price
                data = json.loads(data)
                if type(data) is dict and data.get("event") == "subscriptionStatus":
                    channel_id = data.get("channelID")
                elif type(data) is list and data[0] == channel_id:
                    low24h = float(data[1].get("l", 0)[1])
                    price = float(data[1].get("a", 0)[0])

                    if price == last:
                        continue

                    print(" BTC Price: €", end="")
                    if price > last:
                        set_color(2, 15)
                    elif price < last:
                        set_color(1, 15)

                    print(price, end="")
                    reset_color()
                    carriage_return()
                    await asyncio.sleep(1)
                    print(" BTC Price: €", end="")
                    if price > low24h:
                        set_color(None, 2)
                    elif price < low24h:
                        set_color(None, 1)

                    print(price, end="")
                    reset_color()
                    carriage_return()

                    last = price

    except websockets.ConnectionClosed:
        print("Connection Dropped. Attempting to reconnect")
        carriage_return()
        await get_ticker()
    except ConnectionRefusedError:
        print("Can't connect. Trying again in a bit")
        carriage_return()
        await asyncio.sleep(2)
        await get_ticker()


def hide_cursor():
    print("\033[?25l", end="")


def carriage_return():
    print("\033[K\r", end="")


def set_color(bg=None, fg=None):
    """
    Print escape codes to set the terminal color.
    fg and bg are indices into the color palette for the foreground and
    background colors.
    """
    if fg:
        print("\x1b[38;5;%dm" % fg, end="")
    if bg:
        print("\x1b[48;5;%dm" % bg, end="")


def reset_color():
    """
    Reset terminal color to default.
    """
    print("\x1b[0m", end="")


try:
    hide_cursor()
    print(" loading...", end="")
    carriage_return()
    price = 0
    asyncio.get_event_loop().run_until_complete(get_ticker())
except Exception as e:
    print("Exiting. Last price was " + str(price))
