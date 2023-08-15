#include <Servo.h>
Servo Servo1;
int servoPin = 9;
int rLed = 4;
int yLed = 5;
int gLed = 3;
int x;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(1);
  Servo1.attach(servoPin);
  pinMode(rLed,OUTPUT);
  pinMode(gLed,OUTPUT);
  pinMode(yLed,OUTPUT);
}

void loop() {   
  // put your main code here, to run repeatedly:
  while(!Serial.available());
  x = Serial.readString().toInt();
  if (x==1){
    digitalWrite(rLed, HIGH);
    Servo1.write(150);
    delay(1000);}
  if (x==2){
    digitalWrite(gLed, HIGH);
    Servo1.write(90);
    delay(1000);}
  if (x==3){
    digitalWrite(yLed, HIGH);
    Servo1.write(25);
    delay(1000);}
  else {
    digitalWrite(rLed, LOW);
    digitalWrite(gLed, LOW);
    digitalWrite(yLed, LOW);
  }
}
