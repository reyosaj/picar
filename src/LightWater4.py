#!/usr/bin/env python3
########################################################################
# Filename    : LightWater.py
# Description : Use LEDBar Graph(10 LED) 
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
from gpiozero import LEDBoard
from gpiozero import DistanceSensor
from time import sleep
from signal import pause


# LED setting
ledPins = ["J8:11", "J8:12","J8:13","J8:15","J8:16","J8:18","J8:22","J8:3","J8:5","J8:24"]
leds = LEDBoard(*ledPins, active_high=False)

#Distance sensor setting
trigPin = 36
echoPin = 38
MAX_DISTANCE = 220          # define the maximum measuring distance, unit: cm
timeOut = MAX_DISTANCE*60   # calculate timeout according to the maximum measuring distance



print ('Program is starting ... ')



def onLeds(count):
    print ('>> leds turned on {}'.format(count))
    for index in range(0,count,1):       #move led(on) from left to right 
        leds.on(index)  
        
def offLeds(count):
    print ('>> leds turned off {}'.format(count))
    for index in range(0,count,1):       #move led(on) from left to right 
        leds.off(index)

def destroy():
    print ('>>> Program Interrupted')

if __name__ == '__main__':     # Program entrance
    print ('>>> Program is starting...')
    try:
#         setup()
        
#         while(True):
#             distance = getSonar() # get distance
#             print ("The distance is : %.2f cm"%(distance))
#             print (">> Distance : {}".format(distanceSensor.distance))
#             time.sleep(0.5)

        onLeds(1)
        sleep(1)
        onLeds(3)
        sleep(1)
        onLeds(5)
        distanceSensor = DistanceSensor(echo=38, trigger=36, threshold_distance=0.5, max_distance=2)

#         sleep(1)
#         onLeds(7)
#         sleep(1)
#         onLeds(9)
#         sleep(1)
#         offLeds(9)
#         sleep(1)
#         onLeds(7)
    except:  # Press ctrl-c to end the program.
        print(sys.exc_info()[0])

