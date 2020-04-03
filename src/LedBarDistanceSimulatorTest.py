

from random import randint

from sensors import DistanceSensor
from sensors import LEDBar


import time

ledPins = [11, 12, 13, 15, 16, 18, 22, 3, 5, 24]
distanceSensor = DistanceSensor(36,38,220)
ledBar = LEDBar(ledPins)

    
def loop():
    totalLeds = len(ledPins)

    while True: 
    	time.sleep(0.5)
        distance = distanceSensor.getDistance()
    	print("distance: {}".format(str(distance)))
    	# ledBar.on(0, randint(1, 7))
        ledBar.on(0, distanceAsNumberOfLed(totalLeds, distance))


def distanceAsNumberOfLed(totalLeds, distance):
    oneUnit = 120 / totalLeds
    return totalLeds - int(distance / oneUnit)
    	


            
def destroy():
    GPIO.cleanup()                     # Release all GPIO

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
