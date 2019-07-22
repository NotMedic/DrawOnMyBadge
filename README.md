# Summary
This code is in 3 parts:
1. Arduino Sketch
2. WebSocket Server 
3. HTML Client

The Arduino Sketch is based on code from Brian Lough to do something similar, but has been updated per the Inspiration and Modifications section below. It should be pretty self-explanatory when reading through it, but it basically:
  1. Connects to a wireless network
  2. Connects to a websocket server
  3. Sends a "FRAME" request to get the current Canvas and update the panel
  4. Wait for new websocket messages for DRAW and CLEAR commands. Others commands may be added as time allows. 
  
The WebSocket Server started out as a simple relay, but has added functionality.  It basically:
  1. Listens for new connections
  2. When a new websocket message is recieved, updates a local array of the status and broadcasts this change out to all clients
  3. on SAVE commands, it saves the current array to disk for replay later. Consider it a screenshot.
  
The HTML Client:
  1. loads an HTML5 canvas and auto-scales to your resolution
  2. Connects to a websocket server 
  3. Sends a FRAME command, recieves the response, and draws the current state of the canvas
  4. Listens for Mouse and Touch events to send to the server

Demo Video:
https://www.youtube.com/watch?v=_mOYt15QKRg&feature=youtu.be

# Hardware:
1. [P3 64x32 LED Matrix](https://www.amazon.com/panels-digital-module-display-P3-19296mm/dp/B079JSKF21/)
2. [Wemos (LoLin) D1 Mini](https://www.amazon.com/IZOKEE-NodeMcu-Internet-Development-Compatible/dp/B076F53B6S/)
3. I originally had this breadboard wired, but Brian Louth sells a nice [breakout board](https://www.tindie.com/products/brianlough/d1-mini-matrix-shield/) to clean up the wiring.

Brian also has a solid wiring instructions here:
https://www.instructables.com/id/RGB-LED-Matrix-With-an-ESP8266/

# Inspiration and Modifications

This project originally started out as just various ways to use a P3 64x32 LED Panel around the house.  I ran across a project by Brian Lough (@witnessmenow) where he had setup a websocket server on an ESP8266 and developed a client-side web page to draw pixel art on the badge in real-time.  This project was a good inspiration, and the shell from his code still exists with some pretty significant changes:

1. The ESP8266 is now a websocket client and connects to a websocket server hosted on the Internet.
2. The html drawing client was rewritten to use an HTML5 canvas instead of a DIV grid, making it mobile friendly.
3. The html drawing client provides for a shared canvas so multiple people can draw and see updates in real-time.
3. The html drawing client dynamically sizes based on screen-size for desktops and mobile.
4. The client->websocket->client protocol was rewritten to use JSON and allow for multiple pixels drawn in a single message. 
