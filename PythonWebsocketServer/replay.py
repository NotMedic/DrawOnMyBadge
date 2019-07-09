#!/usr/bin/python

from ws4py.client import WebSocketBaseClient
import time
import sys

ws = WebSocketBaseClient('ws://52.43.252.153:9001/')
ws.connect()

for line in sys.stdin:
    print(line)
    ws.send(line)
    time.sleep(.02)

ws.close()
