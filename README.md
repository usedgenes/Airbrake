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