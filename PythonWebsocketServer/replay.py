#!/usr/bin/python
#cat file | ./replay.py

from ws4py.client import WebSocketBaseClient
import time
import sys
import json

ws = WebSocketBaseClient('ws://127.0.0.1:9001/')
ws.connect()


k=0
data ={ 'CMD': [], 'DATA': []}

for line in sys.stdin:
    line2 = line.replace(':',',').rstrip()
    rawdata = line2.split(',')
    pixels=[]
    pixels.append(rawdata[1])
    pixels.append(rawdata[2])
    pixels.append(rawdata[3])

    data["DATA"].append(pixels)
    data.update({"CMD" : "DRAW"})
    json_data = json.dumps(data)
    ws.send(json_data)
    time.sleep(0.007)
    k = 0
    data["DATA"] *= 0
