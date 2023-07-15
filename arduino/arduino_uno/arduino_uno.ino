// This sketch code is based on the RPLIDAR driver library provided by RoboPeak
#include <RPLidar.h>
#include <SoftwareSerial.h>

#define rxPin 8
#define txPin 9
#define baudrate 9600
#define RPLIDAR_MOTOR 3 // The PWM pin for control the speed of RPLIDAR's motor.
                        // This pin should connected with the RPLIDAR's MOTOCTRL signal 
  

String msg;
SoftwareSerial hc05(rxPin, txPin);
// You need to create an driver instance 
RPLidar lidar;
          
void setup() {
  // bind the RPLIDAR driver to the arduino hardware serial
    Serial.begin(115200);
    lidar.begin(Serial);
    pinMode(RPLIDAR_MOTOR, OUTPUT);
    lidar.startScan();
    analogWrite(RPLIDAR_MOTOR, 0);
  // set pin modes
  // setup bluetooth
    pinMode(rxPin, INPUT);
    pinMode(txPin, OUTPUT);
    hc05.begin(baudrate);

}

void loop() {
  if (IS_OK(lidar.waitPoint())) {
    analogWrite(RPLIDAR_MOTOR, 255);
    float distance = lidar.getCurrentPoint().distance/10; //distance value in cm unit
    float angle    = lidar.getCurrentPoint().angle; //anglue value in degree
    bool  startBit = lidar.getCurrentPoint().startBit; //whether this point is belong to a new scan
    byte  quality  = lidar.getCurrentPoint().quality; //quality of the current measurement
    msg = String(startBit)+","+String(quality)+","+String(distance)+","+String(angle)+",""\n";
    // send msg
    hc05.println(msg); 
  } else {
    analogWrite(RPLIDAR_MOTOR, 0); //stop the rplidar motor
    
    // try to detect RPLIDAR... 
    rplidar_response_device_info_t info;
    if (IS_OK(lidar.getDeviceInfo(info, 100))) {
       // detected...
       lidar.startScan();
       
       // start motor rotating at max allowed speed
       analogWrite(RPLIDAR_MOTOR, 255);
       delay(1000);
    }
  }
}
