#!/usr/bin/env python3
########################################################################

########################################################################
from gpiozero import DistanceSensor
from time import sleep
from signal import pause


#Distance sensor setting
trigPin = 36
echoPin = 38
MAX_DISTANCE = 220          # define the maximum measuring distance, unit: cm
timeOut = MAX_DISTANCE*60   # calculate timeout according to the maximum measuring distance


def destroy():
    print ('>>> Program Interrupted')

if __name__ == '__main__':     # Program entrance
    print ('>>> Program is starting...')
    try:
        distanceSensor = DistanceSensor(echo="J8:35", trigger="J8:37", max_distance=2)
        while True:
             sleep(1)
             print ('distance : {}'.format(distanceSensor.distance))
    except:  # Press ctrl-c to end the program.
        print(sys.exc_info()[0])

