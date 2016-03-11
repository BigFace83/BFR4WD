/*
CMPS03 with arduino I2C example
 
This will display a value of 0 - 359 for a full rotation of the compass.
 
The SDA line is on analog pin 4 of the arduino and is connected to pin 3 of the CMPS03.
The SCL line is on analog pin 5 of the arduino and is conected to pin 2 of the CMPS03.
Both SDA and SCL are also connected to the +5v via a couple of 1k8 resistors.
A switch to callibrate the CMPS03 can be connected between pin 6 of the CMPS03 and the ground.
 
 
*/
#include <Wire.h>
 
#define compassaddress 0x60 //defines address of compass
 
void setup(){
  Wire.begin(); //connects I2C
  Serial.begin(115200);
}
 
void loop(){
  byte highByte;
  byte lowByte;
 
   Wire.beginTransmission(compassaddress);      //starts communication with cmps03
   Wire.write(2);                         //Sends the register we wish to read
   Wire.endTransmission();
   //delay(10);
   Wire.requestFrom(compassaddress, 2);        //requests high byte
   while(Wire.available() < 2);         //while there is a byte to receive
   highByte = Wire.read();           //reads the byte as an integer
   lowByte = Wire.read();
   int bearing = ((highByte*255)+lowByte)/10; 
 
   
   Serial.print("Bearing = ");
   Serial.println(bearing);
   delay(100);
}
