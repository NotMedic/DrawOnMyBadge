from websocket_server import WebsocketServer
from datetime import datetime
import time
import json
from collections import defaultdict

w = 64
h = 32
data ={ 'CMD': [], 'DATA': []}

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
        messager = json.loads(message)
        print messager['CMD']
        
        print("Client(%s) said: %s" % (client['address'][0], message))
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Client(%s) said: %s\n" % (client['address'][0], message))
        if messager['CMD'] == 'FRAME':
             k = 0
             for i in range(w):
                for j in range(h):
                    if (str(frame[i][j]) != "0") and (str(frame[i][j]) != "0x000"):
                        pixels=[]
                        pixels.append(str(i))
                        pixels.append(str(j))
                        pixels.append(str(frame[i][j]).rstrip())
                        if k < 48:
                            data["DATA"].append(pixels)
                            k = k + 1 
                        else: 
                            data["DATA"].append(pixels)
                            data.update({"CMD" : "DRAW"})
                            json_data = json.dumps(data)
                            server.send_message(client,json_data)
                           # time.sleep(.1)
                            k = 0
                            data["DATA"] *= 0
             #Send Final Frame
             data.update({"CMD" : "DRAW"})
             json_data = json.dumps(data)
             server.send_message(client,json_data)
             data["DATA"] *= 0

        elif messager['CMD'] == 'CLEAR':
#            print "CLEAR Request"
            for i in range(w):
                for j in range(h):
                    frame[i][j] = 0
            server.send_message_to_all(message)
        elif messager['CMD'] == 'DRAW':
            for pixel in messager['DATA']:
               print pixel
            x = int(pixel[0])
            y = int(pixel[1])
            c = pixel[2]
            
            try:
                frame[x][y] = c
            except IndexError:
                pass
            server.send_message_to_all(message)

        elif messager['CMD'] == "SAVE":
            print "SAVING"
            savefile=open(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".save","w", 1)
            for i in range(w):
                for j in range(h):
                    if (str(frame[i][j]) != "0") and (str(frame[i][j]) != "0x000"):
                        message = "0:" + str(i) + "," + str(j)  + "," + str(frame[i][j])
                        savefile.write(message + "\n")
            savefile.close()
        else:
            server.send_message_to_all(message)

PORT=9001
server = WebsocketServer(PORT, host='0.0.0.0')
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
