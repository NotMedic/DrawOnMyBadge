/*******************************************************************
  DrawOnMyBadge.
  Original idea Brian Lough
  Adapted for websocket client, json, and updates my Tim McGuffin
*******************************************************************/

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>
#include <Hash.h>
#include <ArduinoJson.h>
#include <Ticker.h>

#include <PxMatrix.h>
// The library for controlling the LED Matrix
// Needs to be manually downloaded and installed
// https://github.com/2dom/PxMatrix

#define ELEMENTS(x)   (sizeof(x) / sizeof(x[0]))

Ticker display_ticker;

// Pins for LED MATRIX
#define P_LAT 16
#define P_A 5
#define P_B 4
#define P_C 15
#define P_OE 2
#define P_D 12
#define P_E 0

PxMATRIX display(64, 32, P_LAT, P_OE, P_A, P_B, P_C, P_D, P_E);

//------- Replace the following! ------
#define WIFI_NAME "APName"
#define WIFI_PASS "APPassword"

char ssid[] = WIFI_NAME;       // your network SSID (name)
char password[] = WIFI_PASS;  // your network key

unsigned long delayStart = 0;
bool delayRunning = false;

WebSocketsClient webSocket;

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  int x;
  int y;
  uint16_t colour;
  String inPayload;
  String colourString;

  switch (type) {
    case WStype_DISCONNECTED:
      Serial.println("Disconnected");
      clearDisplay();
      display.setCursor(1, 1);
      display.println("No WS");
      break;
    case WStype_CONNECTED:
      {
        //        IPAddress ip = webSocket.remoteIP(num);
        //        Serial.printf("[%u] Connected from %d.%d.%d.%d url: %s\n", num, ip[0], ip[1], ip[2], ip[3], payload);

        clearDisplay();
        display.setCursor(1, 1);
        display.println("WS OK!");
        delay(500);
        clearDisplay();

        webSocket.sendTXT("{\"CMD\":\"FRAME\"}");
      }
      break;
    case WStype_TEXT:
      {
        // Serial.printf("[%u] get Text: %s\n", num, payload);
        //      inPayload = String((char *) payload);

        DynamicJsonBuffer jsonBuffer(4096);
        JsonObject& root = jsonBuffer.parseObject((char *)payload);

        String commandtemp = root["CMD"];

       if (commandtemp == "CLEAR") {

          clearDisplay();

        } else if (commandtemp == "DRAW") {

          int node_length = root["DATA"].size();

          for (int i = 0; i < node_length; i++) {

            x = int(root["DATA"][i][0]);
            y = int(root["DATA"][i][1]);
            String c = root["DATA"][i][2];

            //        Serial.println("x: " + String(x));
            //        Serial.println("y: " + String(y));
            //        Serial.println("c: " + c);

            colour = strtol(c.c_str(), NULL, 0);
            //        Serial.println(colour);
            display.drawPixel(x , y, colour);

          }
        }
      }
      break;
    case WStype_BIN:
      Serial.printf("get binary length: %u\n", length);
      hexdump(payload, length);

      // send message to client
      // webSocket.sendBIN(num, payload, length);
      break;
  }

}

void display_updater()
{

  display.display(70);

}

void clearDisplay() {
  for (int i = 0; i < 64; i++) {
    for (int j = 0; j < 32; j++) {
      display.drawPixel(i , j, 0x0000);
    }
  }
}

void setup() {

  Serial.begin(115200);

  display.begin(16);
  display.clearDisplay();

  display_ticker.attach(0.002, display_updater);
  yield();

  // Set WiFi to station mode and disconnect from an AP if it was Previously
  // connected
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  display.setCursor(1, 1);
  display.setTextSize(1);
  display.setTextWrap(1);


  // Attempt to connect to Wifi network:
  Serial.print("Connecting Wifi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  int wificount = 0;
  while (WiFi.status() != WL_CONNECTED) {
    wificount = wificount + 1;
    Serial.print(".");
    clearDisplay();
    display.setCursor(1, 1);
    display.println("No WiFi");

    delay(500);

    if (wificount > 20) {
      WiFi.disconnect();
      //WiFi of Last Resort.
      display.println("Fallback");
      //Should probably consider WifiManager, but this is good for DEFCON Wireless.
      //------- Replace the following! ------
      WiFi.begin("BackupAP", "BackupPassword");
      wificount = 0;
    }

  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  IPAddress ip = WiFi.localIP();
  Serial.println(ip);

  clearDisplay();
  display.setCursor(1, 1);
  display.println("WiFi: OK");

  delayStart = millis();
  delayRunning = true;

  //webSocket.begin();
  webSocket.begin("x.x.x.x", 9001, "/");
  webSocket.onEvent(webSocketEvent);
}

void loop() {
  if (delayRunning && ((millis() - delayStart) >= 30000)) {
    webSocket.sendPing();
    Serial.println("Sent Ping");
    delayStart = millis();
  }
  webSocket.loop();
  yield();
}
