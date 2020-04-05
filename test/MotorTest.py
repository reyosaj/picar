from src.sensors import Motor
import time
import RPi.GPIO as GPIO


rearMotor = Motor(13, 15, 11, 'RearMotor')
frontMotor = Motor(16, 18, 22, 'FrontMotor')

speed = [25, 50, 75, 100]


def loop():

    while True:
        time.sleep(1)

        stdin = raw_input()
        print("input: {}".format(stdin))

        if stdin == 'f1':
            rearMotor.clockwise(25)
        elif stdin == 'f2':
            rearMotor.clockwise(50)
        elif stdin == 'f3':
            rearMotor.clockwise(75)
        elif stdin == 'f4':
            rearMotor.clockwise(100)
        elif stdin == 'b1':
            rearMotor.counterClockwise(25)
        elif stdin == 'b2':
            rearMotor.counterClockwise(50)
        elif stdin == 'b3':
            rearMotor.counterClockwise(75)

        elif stdin == 'r1':
            frontMotor.clockwise(25)
        elif stdin == 'l1':
            frontMotor.counterClockwise(25)
        elif stdin == 'fs':
            frontMotor.stop()

        elif stdin == 's':
            rearMotor.stop()
        elif stdin == 'e':
            break
        else:
            print("invalid:  suported (f1, f2, f3, b1, b2, b3, s, e)")



if __name__ == '__main__':     # Program entrance
    print('Program is starting...')
    try:
        loop()
        GPIO.cleanup()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        frontMotor.stop()
        rearMotor.stop()
        
        print("exit")