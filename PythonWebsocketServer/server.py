from websocket_server import WebsocketServer
from datetime import datetime
import time

w = 64
h = 32
frame = [[0 for x in range(h)] for y in range(w)]

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
        if message == "FRAME":
#            print "FRAME Request"
            for i in range(w):
                for j in range(h):
                    if (str(frame[i][j]) != "0") and (str(frame[i][j]) != "0x000"):
                        message = "0:" + str(i) + "," + str(j)  + "," + str(frame[i][j])
                        server.send_message(client,message)
                        time.sleep(.01)
        elif message == "CLEAR":
#            print "CLEAR Request"
            for i in range(w):
                for j in range(h):
                    frame[i][j] = 0
        elif message.startswith('0:'):
#            print "Draw Pixel Message"
            elements =  message.split(":")[1].split(",")
            x = int(elements[0])
            y = int(elements[1])
            c = elements[2]
            frame[x][y] = c

        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Client(%s) said: %s\n" % (client['address'][0], message))
        server.send_message_to_all(message)


PORT=9001
server = WebsocketServer(PORT, host='0.0.0.0')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
