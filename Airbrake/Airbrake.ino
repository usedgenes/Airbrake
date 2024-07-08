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

#define SEALEVELPRESSURE_HPA (1013.25)
#define CLOSED_DRAG_COEFFICIENT (0.5)
#define OPENED_DRAG_COEFFICIENT (0.78)
#define AIR_DENSITY (1.225)
#define AREA (0.003)
#define MASS (0.62)
#define CUTOFF_FREQUENCY (0.9)
#define INITIAL_ALPHA (0.03)
#define LAUNCH_CONDITION_ALTITUDE (4)
#define MOTOR_DELAY (1500)
#define TARGET_ALTITUDE (243)
#define MAX_AIRBRAKE_EFFICIENCY (3)
#define MAX_SERVO_POSITION (150)


float timeConstant;
float alpha;
float launchAltitude;
float currentAltitude;
unsigned long currentTime;
unsigned long launchTime;
float filteredProjectedAltitude;
int servoPosition;
bool firstLoop = true;
float adjustedTargetAltitude;


Adafruit_BMP3XX bmp;
File myFile;
Servo servo;


void setup() {
  Serial.begin(9600);


  servo.attach(9);
  servo.write(10);
  servoPosition = 10;


  timeConstant = 1/(6.283 * CUTOFF_FREQUENCY);
  alpha = INITIAL_ALPHA / (INITIAL_ALPHA + timeConstant);


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
  while(millis() < 10000) {
    logger(millis(), bmp.readAltitude(SEALEVELPRESSURE_HPA), bmp.pressure, 0, 0, 10);
  }


  myFile = SD.open("LOGGER.TXT", FILE_WRITE);
  myFile.print(millis());
  myFile.println(" Calibrated");
  myFile.close();


  launchAltitude = bmp.readAltitude(SEALEVELPRESSURE_HPA);
  currentAltitude = launchAltitude;
  adjustedTargetAltitude = currentAltitude + TARGET_ALTITUDE;


  myFile = SD.open("LOGGER.TXT", FILE_WRITE);
  myFile.print(launchAltitude);
  myFile.println(" Launch Altitude");
  myFile.close();


  //Launch condition
  while(currentAltitude - launchAltitude < LAUNCH_CONDITION_ALTITUDE) {
    logger(millis(), bmp.readAltitude(SEALEVELPRESSURE_HPA), bmp.pressure, 0, 0, 10);
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
  if(firstLoop) {
    firstLoop = false;
    currentAltitude = bmp.readAltitude(SEALEVELPRESSURE_HPA);
    currentTime = millis();
    filteredProjectedAltitude = currentAltitude;
    delay(10);
    return;
  }
  unsigned long previousTime = currentTime;
  currentTime = millis();


  float previousAltitude = currentAltitude;
  currentAltitude = bmp.readAltitude(SEALEVELPRESSURE_HPA);


  //Could find more accurate way to calculate altitude by using more of previous velocities
  float velocity = 1000*(currentAltitude - previousAltitude)/(currentTime - previousTime);
 
  float projectedAltitude = currentAltitude + (velocity * velocity / (19.6 + ((CLOSED_DRAG_COEFFICIENT * AIR_DENSITY * velocity * velocity * AREA * 0.5) / MASS)));;
 
  float previousFilteredProjectedAltitude = filteredProjectedAltitude;


  filteredProjectedAltitude = (projectedAltitude*alpha)+(previousFilteredProjectedAltitude*(1-alpha));


  if(currentTime - launchTime > 15000) {
    servo.write(50);
    logger(currentTime, currentAltitude, bmp.pressure, projectedAltitude, filteredProjectedAltitude, 50);
    return;
  }
 
  if(currentTime - launchTime > MOTOR_DELAY) {
    float altitudeDifference = filteredProjectedAltitude - adjustedTargetAltitude;
    if(altitudeDifference > 0) {
      if(altitudeDifference > MAX_AIRBRAKE_EFFICIENCY) {
        servo.write(MAX_SERVO_POSITION);
        servoPosition = MAX_SERVO_POSITION;
      }
      else {
        servoPosition = 10 + ((altitudeDifference / MAX_AIRBRAKE_EFFICIENCY) * (MAX_SERVO_POSITION - 10));
        servo.write(servoPosition);
      }
    }
    else {
      servo.write(10);
      servoPosition = 10;
    }
  }


  logger(currentTime, currentAltitude, bmp.pressure, projectedAltitude, filteredProjectedAltitude, servoPosition);
}


void logger(unsigned long time, float altitude, float pressure, float projectedAltitude, float filteredProjectedAltitude, int servoPosition) {
  myFile = SD.open("ALTITUDE.TXT", FILE_WRITE);
 
  if (myFile) {
    myFile.print(time);
    myFile.print(" ");
    myFile.print(altitude);
    myFile.print(" ");
    myFile.print(pressure);
    myFile.print(" ");
    myFile.print(projectedAltitude);
    myFile.print(" ");
    myFile.print(filteredProjectedAltitude*100);
    myFile.print(" ");
    myFile.println(servoPosition);
    myFile.close();
  } else {
    myFile.println("ERROR");
    myFile.close();
  }


}
