#!/usr/bin/env python3

########################################################################
import RPi.GPIO as GPIO
import time


class DistanceSensor:
    def __init__(self, triggerPin, echoPin, maxDistance):
        self.triggerPin = triggerPin
        self.echoPin = echoPin
        self.maxDistance = maxDistance
        self.timeOut = maxDistance*60   # calculate timeout according to the maximum measuring distance
        GPIO.setmode(GPIO.BOARD)      # use PHYSICAL GPIO Numbering
        GPIO.setup(triggerPin, GPIO.OUT)   # set trigPin to OUTPUT mode
        GPIO.setup(echoPin, GPIO.IN)    # set echoPin to INPUT mode

    def getDistance(self):     # get the measurement results of ultrasonic module,with unit: cm
        GPIO.output(self.triggerPin,GPIO.HIGH)      # make trigPin output 10us HIGH level 
        time.sleep(0.00001)     # 10us
        GPIO.output(self.triggerPin,GPIO.LOW) # make trigPin output LOW level 
        pingTime = self.pulseIn(self.echoPin,GPIO.HIGH)   # read plus time of echoPin
        distance = pingTime * 340.0 / 2.0 / 10000.0     # calculate distance with sound speed 340m/s 
        # print("pingTime={0}, distance={1}".format(str(pingTime), str(distance)))
        return distance

    def pulseIn(self,pin,level): # obtain pulse time of a pin under timeOut
      #  print("pin={0}, level={1}".format(str(pin), level))
        t0 = time.time()
        while(GPIO.input(pin) != level):
            if((time.time() - t0) > self.timeOut*0.000001):
                return 0;
        t0 = time.time()
        while(GPIO.input(pin) == level):
            if((time.time() - t0) > self.timeOut*0.000001):
                return 0;
        pulseTime = (time.time() - t0)*1000000
        # print("pulseTime={}".format(str(pulseTime)))
        return pulseTime


class LEDBar:
    def __init__(self, ledPins=[], *args):
        self.ledPins = ledPins   
        self.ledCount = len(ledPins)
        # GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
        GPIO.setup(ledPins, GPIO.OUT)   # set all ledPins to OUTPUT mode
        GPIO.output(ledPins, GPIO.HIGH) # make all ledPins output HIGH level, turn off all led

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
    def __init__(self, forwardPin, backwardPin, pwmPin):
        self.forwardPin = forwardPin
        self.backwardPin = backwardPin
        self.pwmPin = pwmPin
        GPIO.setmode(GPIO.BOARD)
        # set up GPIO pins
        GPIO.setup(pwmPin, GPIO.OUT) # Connected to PWMA
        GPIO.setup(forwardPin, GPIO.OUT) # Connected to AIN2
        GPIO.setup(backwardPin, GPIO.OUT) # Connected to AIN1
        self.pwm = GPIO.PWM(pwmPin,1000)

    def clockwise(self, spinCycle):
        # Drive the motor clockwise
        GPIO.output(self.backwardPin, GPIO.HIGH) # Set AIN1
        GPIO.output(self.forwardPin, GPIO.LOW) # Set AIN2
        self.pwm.ChangeDutyCycle(spinCycle)

    def counterClockwise(self, spinCycle):
        # Drive the motor counterclockwise
        GPIO.output(self.backwardPin, GPIO.LOW) # Set AIN1
        GPIO.output(self.forwardPin, GPIO.HIGH) # Set AIN2
        self.pwm.ChangeDutyCycle(spinCycle)

    def stop(self):
        GPIO.output(self.backwardPin, GPIO.LOW) # Set AIN1
        GPIO.output(self.forwardPin, GPIO.LOW) # Set AIN2