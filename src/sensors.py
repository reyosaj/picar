#!/usr/bin/env python3

########################################################################
import RPi.GPIO as GPIO
import time
from enum import Enum
import logging, sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("sensors")


class DistanceSensor:
    def __init__(self, triggerPin, echoPin, maxDistance):
        self.triggerPin = triggerPin
        self.echoPin = echoPin
        self.maxDistance = maxDistance
        # calculate timeout according to the maximum measuring distance
        self.timeOut = maxDistance*60
        GPIO.setmode(GPIO.BOARD)      # use PHYSICAL GPIO Numbering
        GPIO.setup(triggerPin, GPIO.OUT)   # set trigPin to OUTPUT mode
        GPIO.setup(echoPin, GPIO.IN)    # set echoPin to INPUT mode

    def getDistance(self):     # get the measurement results of ultrasonic module,with unit: cm
        # make trigPin output 10us HIGH level
        GPIO.output(self.triggerPin, GPIO.HIGH)
        time.sleep(0.00001)     # 10us
        GPIO.output(self.triggerPin, GPIO.LOW)  # make trigPin output LOW level
        # read plus time of echoPin
        pingTime = self.pulseIn(self.echoPin, GPIO.HIGH)
        # calculate distance with sound speed 340m/s
        distance = pingTime * 340.0 / 2.0 / 10000.0
        # print("pingTime={0}, distance={1}".format(str(pingTime), str(distance)))
        return distance

    def pulseIn(self, pin, level):  # obtain pulse time of a pin under timeOut
      #  print("pin={0}, level={1}".format(str(pin), level))
        t0 = time.time()
        while(GPIO.input(pin) != level):
            if((time.time() - t0) > self.timeOut*0.000001):
                return 0
        t0 = time.time()
        while(GPIO.input(pin) == level):
            if((time.time() - t0) > self.timeOut*0.000001):
                return 0
        pulseTime = (time.time() - t0)*1000000
        # print("pulseTime={}".format(str(pulseTime)))
        return pulseTime


class LEDBar:
    def __init__(self, ledPins=[], *args):
        self.ledPins = ledPins
        self.ledCount = len(ledPins)
        # GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
        GPIO.setup(ledPins, GPIO.OUT)   # set all ledPins to OUTPUT mode
        # make all ledPins output HIGH level, turn off all led
        GPIO.output(ledPins, GPIO.HIGH)

    def on(self, start, end):
        print("Led on from={0}, to={1}".format(start, end))
        if start < 0 or end > self.ledCount:
            print("invalid start or end")
        else:
            for idx, pin in enumerate(self.ledPins):
                if idx < start or idx > end:
                    GPIO.output(pin, GPIO.HIGH)
                else:
                    GPIO.output(pin, GPIO.LOW)

    def off(self, start, end):
        print("Led off from={0}, to={1}".format(start, end))
        if start < 0 or end > self.ledCount:
            print("invalid start or end")
        else:
            for idx, pin in enumerate(self.ledPins):
                if idx >= start and idx <= end:
                    GPIO.output(pin, GPIO.HIGH)


class Motor:
    class Direction(Enum):
        STANDBY = 0
        CLOCKWISE = 1
        COUNTERCLOCKWISE = -1

    def __init__(self, forwardPin, backwardPin, pwmPin, alias=''):
        self.forwardPin = forwardPin
        self.backwardPin = backwardPin
        self.pwmPin = pwmPin
        GPIO.setmode(GPIO.BOARD)
        # set up GPIO pins
        GPIO.setup(pwmPin, GPIO.OUT, initial=GPIO.HIGH)  # Connected to PWMA
        GPIO.setup(forwardPin, GPIO.OUT, initial=GPIO.LOW)  # Connected to AIN2
        GPIO.setup(backwardPin, GPIO.OUT, initial=GPIO.LOW)  # Connected to AIN1
        self.pwm = GPIO.PWM(pwmPin, 1500)
        self.started = False
        self.direction = Motor.Direction.STANDBY
        self.__alias = alias
        logger.debug('%s: Initialising', self.__alias)

    def clockwise(self, spinCycle):
        logger.info('%s: Clockwise  , spinCycle:%s ', self.__alias, spinCycle)
        # Drive the motor clockwise
        GPIO.output(self.backwardPin, GPIO.LOW)  # Set AIN1
        GPIO.output(self.forwardPin, GPIO.HIGH)  # Set AIN2
        self.startSpin(spinCycle)
        self.direction = Motor.Direction.CLOCKWISE

    def startSpin(self, spinCycle):
        if self.started:
            self.pwm.ChangeDutyCycle(spinCycle)
            logger.debug('%s:changing duty cycle', self.__alias)
        else:
            logger.debug('%s:start Spin', self.__alias)
            self.started = True
            self.pwm.start(spinCycle)

    def counterClockwise(self, spinCycle):
        logger.info('%s:counterClockwise , spinCycle:%s',
                    self.__alias, spinCycle)
        # Drive the motor counterclockwise
        GPIO.output(self.backwardPin, GPIO.HIGH)  # Set AIN1
        GPIO.output(self.forwardPin, GPIO.LOW)  # Set AIN2
        self.startSpin(spinCycle)
        self.direction = Motor.Direction.COUNTERCLOCKWISE

    def stop(self):
        logger.info('%s:stop ', self.__alias)
        GPIO.output(self.backwardPin, GPIO.LOW)  # Set AIN1
        GPIO.output(self.forwardPin, GPIO.LOW)  # Set AIN2
        # self.pwm.stop()
        self.started = False
        self.direction = Motor.Direction.STANDBY
        # GPIO.cleanup()
