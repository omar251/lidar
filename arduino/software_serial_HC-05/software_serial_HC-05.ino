#include <SoftwareSerial.h>

#define rxPin 8
#define txPin 9
#define baudrate 9600
String startBit = "1";
String quality = "1";
String distance= "1";
String angle= "1";
String msg;
SoftwareSerial hc05(rxPin, txPin);

void setup() {
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  Serial.begin(9600);
  hc05.begin(baudrate);
}

void loop() {
  if (hc05.available() > 0) {
    char receivedChar = hc05.read();

    if (receivedChar == '0') {
      // Stop sending message
      msg = "";
    } else if (receivedChar == '1') {
      // Start sending message
      msg = startBit+","+quality+","+distance+","+angle+",";
    }
  }

  if (msg != "") {
    hc05.println(msg);
  }
}
