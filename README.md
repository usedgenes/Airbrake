# Airbrake
 
This project is designed to be an airbrake to fit a model rocket that uses a BT-80 body tube for both the booster and transition. It uses a BMP390 to get altitude data, and a low-pass filter to smooth the data out. To adjust the low-pass filter values, change the macros CUTOFF_FREQUENCY and INITIAL_ALPHA. It then uses basic kinematics equations to produce real-time estimates of apogee altitude during a rocket launch, and deploys the airbrakes as necessary. Using an F-67 motor, the airbrake when deployed from the very start is able to reduce the apogee by approximately 200 feet. 

Macros that also need to be changed:
MASS (rocket mass)
MOTOR_DELAY 
TARGET_ALTITUDE

Materials:
SG90 servo
Arduino Pro Mini
BMP390
SD card module
7.4v Lipo battery

Link to the CAD files: https://cad.onshape.com/documents/ae3e569ec67173b7e15d4f91/w/e4bd71f28ac7837aae9bb0d0/e/4af31456cef63293cc1a82e8?renderMode=0&uiState=66dbf4e0bf94e2384714ffb7

What the airbrake looks like:  
![Airbrake](https://github.com/usedgenes/Airbrake/blob/main/Parts/Airbrake%20Picture.png)
