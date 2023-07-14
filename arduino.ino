// This sketch code is based on the RPLIDAR driver library provided by RoboPeak
#include <RPLidar.h>
 
// You need to create an driver instance 
RPLidar lidar;
 
#define RPLIDAR_MOTOR 4 // The PWM pin for control the speed of RPLIDAR's motor.
                        // This pin should connected with the RPLIDAR's MOTOCTRL signal 
                        
                         
void setup() {
 
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
