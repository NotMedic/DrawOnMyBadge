#!/usr/bin/python

from websocket_server import WebsocketServer
from datetime import datetime

f= open("wslog.txt","a+", 1)

# Called for every client connecting (after handshake)
def new_client(client, server):
        print("New client connected from %s and was given id %d" % (client['address'][0], client['id']))
#       server.send_message_to_all("Hey all, a new client has joined us")
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " New Client %d %s\n" % (client['id'], client['address'][0]))

# Called for every client disconnecting
def client_left(client, server):
        print("Client(%s) disconnected" % client['address'][0])
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Client(%s) disconnected\n" % client['address'][0])

# Called when a client sends a message
def message_received(client, server, message):
        if len(message) > 200:
                message = message[:200]+'..'
        print("Client(%s) said: %s" % (client['address'][0], message))
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Client(%s) said: %s\n" % (client['address'][0], message))
        server.send_message_to_all(message)


PORT=9001
server = WebsocketServer(PORT, host='0.0.0.0')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
