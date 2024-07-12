#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP3XX.h"
#include <SD.h>
#include <Servo.h>


#define BMP_SCK 13
#define BMP_MISO 12
#define BMP_MOSI 11
#define BMP_CS 10

#define LAUNCH_CONDITION_ALTITUDE (3)
#define STARTUP_TIME (10000)
#define SEALEVELPRESSURE_HPA (1013.25)
#define CLOSED_DRAG_COEFFICIENT (0.5)
#define OPENED_DRAG_COEFFICIENT (0.8)
#define Kp (0.0005)
#define Ki (0.000085)
#define Kd (0)
#define TARGET_ALTITUDE (850)
#define MAX (1)
#define MIN (0)

float launchAltitude;
unsigned long currentTime;
unsigned long launchTime;
int servoPosition;
float previousError;
float integralError;
unsigned long previousTime;
float adjustedTargetAltitude;

Adafruit_BMP3XX bmp;
File myFile;
Servo servo;


void setup() {
  Serial.begin(115200);

  servo.attach(9);
  servo.write(10);
  servoPosition = 10;

  if (!SD.begin(10)) {
    myFile = SD.open("LOGGER.TXT", FILE_WRITE);
    myFile.print(millis());
    myFile.println(" No SD card");
    myFile.close();
    while (1);
  }

  while (!Serial);

  if (!bmp.begin_I2C()) {
    myFile = SD.open("LOGGER.TXT", FILE_WRITE);
    myFile.print(millis());
    myFile.println(" No BMP3 sensor");
    myFile.close();
  }
 
  bmp.setPressureOversampling(BMP3_OVERSAMPLING_8X);
  bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_7);
  bmp.setOutputDataRate(BMP3_ODR_200_HZ);


  myFile = SD.open("ALTITUDE.TXT", FILE_WRITE);
  myFile.println("---------------------------------------------------------------");
  myFile.close();


  myFile = SD.open("LOGGER.TXT", FILE_WRITE);
  myFile.print(millis());
  myFile.println(" Started");
  myFile.close();


  //Change this
  while(millis() < STARTUP_TIME) {
    logger(millis(), bmp.readAltitude(SEALEVELPRESSURE_HPA), bmp.pressure, 10);
  }


  myFile = SD.open("LOGGER.TXT", FILE_WRITE);
  myFile.print(millis());
  myFile.println(" Calibrated");
  myFile.close();


  launchAltitude = bmp.readAltitude(SEALEVELPRESSURE_HPA);
  float currentAltitude = launchAltitude;
  adjustedTargetAltitude = launchAltitude + TARGET_ALTITUDE;


  myFile = SD.open("LOGGER.TXT", FILE_WRITE);
  myFile.print(launchAltitude);
  myFile.println(" Launch Altitude");
  myFile.close();


  //Launch condition
  while(currentAltitude - launchAltitude < LAUNCH_CONDITION_ALTITUDE) {
    logger(millis(), bmp.readAltitude(SEALEVELPRESSURE_HPA), bmp.pressure, 10);
    currentAltitude = bmp.readAltitude(SEALEVELPRESSURE_HPA);
  }
 
  launchTime = millis();
  currentTime = launchTime;


  myFile = SD.open("LOGGER.TXT", FILE_WRITE);
  myFile.print(launchTime);
  myFile.print(" ");
  myFile.println(" Launched");
  myFile.close();
 
}


void loop() {

  logger(currentTime, currentAltitude, bmp.pressure, servoPosition);
}


float pid(float currentAltitude, unsigned long currentTime) {
  unsigned long dt = currentTime - previousTime;
  if(dt == 0) {
    return 0;
  }
  previousTime = currentTime;
  float error = 3.28*(adjustedTargetAltitude - currentAltitude);
  float derivativeError = (error - previousError) / dt;
  float integralError += error * dt;
  
  float output = Kp*error + Ki*integralError + Kd*derivativeError
  if (output > self.saturation_max) {
    output = self.saturation_max;
  }
  else if (output < self.saturation_min) {
    output = self.saturation_min
  }
  return (OPENED_DRAG_COEFFICIENT-CLOSED_DRAG_COEFFICIENT)*output;
}


void logger(unsigned long time, float altitude, float pressure, int servoPosition) {
  myFile = SD.open("ALTITUDE.TXT", FILE_WRITE);
 
  if (myFile) {
    myFile.print(time);
    myFile.print(" ");
    myFile.print(altitude);
    myFile.print(" ");
    myFile.print(pressure);
    myFile.print(" ");
    myFile.println(servoPosition);
    myFile.close();
  } else {
    myFile.println("ERROR");
    myFile.close();
  }
}
