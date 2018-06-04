#!/usr/bin/env python

# WS client example

import asyncio
import json
import websockets


async def get_ticker():
    async with websockets.connect(
            'wss://ws-feed.gdax.com') as websocket:

        subscribe_msg = {
            "type": "subscribe",
            "product_ids": [
                "ETH-EUR"
            ],
            "ticker": [
                "level2",
            ]
        }

        await websocket.send(json.dumps(subscribe_msg))

        last = 0

        while True:
            data = await websocket.recv()
            price = float(json.loads(data).get('price', '0'))
            if price > last:
                set_color(15, 2)
            else:
                set_color(15, 1)

            print(price, end="\r")
            reset_color()
            last = price


def set_color(fg=None, bg=None):
    """
    Print escape codes to set the terminal color.
    fg and bg are indices into the color palette for the foreground and
    background colors.
    """
    if fg:
        print('\x1b[38;5;%dm' % fg, end='')
    if bg:
        print('\x1b[48;5;%dm' % bg, end='')


def reset_color():
    """
    Reset terminal color to default.
    """
    print('\x1b[0m', end='')


asyncio.get_event_loop().run_until_complete(get_ticker())
