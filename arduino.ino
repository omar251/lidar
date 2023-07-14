// This sketch code is based on the RPLIDAR driver library provided by RoboPeak
#include <RPLidar.h>
#include <math.h>

float distance = 0;
float angle = 0;
unsigned long refresh_interval = 2000;  // Set the refresh interval in milliseconds
unsigned long prev_refresh_time = 0;
unsigned int mindistance = 20;
float res = 1.0;
bool running = true;
bool canAddPoints = false;

struct Point {
  float x;
  float y;
};

Point points[100];
int pointCount = 0;

struct Obstacle {
  float x;
  float y;
};

Obstacle obstacles[100];
int obstacleCount = 0;

// You need to create an driver instance 
RPLidar lidar;
 
#define RPLIDAR_MOTOR 4 // The PWM pin for control the speed of RPLIDAR's motor.
                        // This pin should connected with the RPLIDAR's MOTOCTRL signal 
                                                
void setup() {
  pinMode(13, OUTPUT);
   Serial.begin(115200);
   Serial1.begin(115200);
  // bind the RPLIDAR driver to the arduino hardware serial
  lidar.begin(Serial1);
   
  // set pin modes
  pinMode(RPLIDAR_MOTOR, OUTPUT);
}
 
void loop() {
  if (IS_OK(lidar.waitPoint())) {
    float distance = lidar.getCurrentPoint().distance/10; //distance value in cm unit
    float angle    = lidar.getCurrentPoint().angle; //anglue value in degree
    bool  startBit = lidar.getCurrentPoint().startBit; //whether this point is belong to a new scan
    byte  quality  = lidar.getCurrentPoint().quality; //quality of the current measurement
     
    //perform data processing here... 
    
     Serial.print(startBit);       
     Serial.print(","); 
     Serial.print(quality);       
     Serial.print(",");      
     Serial.print(distance);       
     Serial.print(",");  
     Serial.print(angle);   
     Serial.println(",");  
    if (distance > 150 || distance < 15) {
    // Skip invalid distance values
    return;
  }

  if (angle > 360 || angle == 122 || angle == 123 || angle == 124 || angle == 125) {
    // Skip invalid angle values
    return;
  }

  float x = distance * cos(radians(angle)) * res;
  float y = distance * sin(radians(angle)) * res;
   
    if (distance < mindistance ) {
      obstacleCount++;
    }
  if (obstacleCount > 10){
     digitalWrite(13, HIGH);
     }
  else{
     digitalWrite(13, LOW);
  } 
  unsigned long elapsed_time = millis() - prev_refresh_time;
  if (elapsed_time >= refresh_interval) {
    // canAddPoints = true;
    pointCount = 0;
    obstacleCount = 0;
    prev_refresh_time = millis();
  }
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
