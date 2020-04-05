from src.sensors import Motor
import time
from pynput import keyboard
import RPi.GPIO as GPIO


rearMotor = Motor(13, 15, 11, "RM")
frontMotor = Motor(16, 18, 22, "FM")

speed = [0, 25, 50, 75, 100]
speedIdx = 0
maxSpeedIdx = len(speed) - 1


def onKeyPress(key):
    global speedIdx
    if key == keyboard.Key.up:
        if rearMotor.direction == Motor.Direction.CLOCKWISE:
            if speedIdx < maxSpeedIdx:
                speedIdx += 1
                rearMotor.clockwise(speed[speedIdx])
        elif rearMotor.direction == Motor.Direction.COUNTERCLOCKWISE:
            if speedIdx > 0:
                speedIdx -= 1
                rearMotor.counterClockwise(speed[speedIdx])
            else:
                speedIdx = 0
                rearMotor.stop()
                rearMotor.clockwise(speed[speedIdx])
        else:
            speedIdx = 0
            rearMotor.clockwise(speed[speedIdx])
    elif key == keyboard.Key.down:
        if rearMotor.direction == Motor.Direction.COUNTERCLOCKWISE:
            if speedIdx < maxSpeedIdx:
                speedIdx += 1
                rearMotor.counterClockwise(speed[speedIdx])
        elif rearMotor.direction == Motor.Direction.CLOCKWISE:
            if speedIdx > 0:
                speedIdx -= 1
                rearMotor.clockwise(speed[speedIdx])
            else:
                speedIdx = 0
                rearMotor.stop()
                rearMotor.counterClockwise(speed[speedIdx])
        else:
            speedIdx = 0
            rearMotor.counterClockwise(speed[speedIdx])
    elif key == keyboard.Key.right:
        if frontMotor.direction == Motor.Direction.COUNTERCLOCKWISE:
            frontMotor.stop()
        else:
            frontMotor.clockwise(speed[maxSpeedIdx])
    elif key == keyboard.Key.left:
        if frontMotor.direction == Motor.Direction.CLOCKWISE:
            frontMotor.stop()
        else:
            frontMotor.counterClockwise(speed[maxSpeedIdx])
    elif key == keyboard.Key.esc:
        frontMotor.stop()
        rearMotor.stop()
        return False


def destroy():
    GPIO.cleanup()                     # Release all GPIO


if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    try:
        listener = keyboard.Listener(on_press=onKeyPress)
        listener.start()  # start to listen on a separate thread
        listener.join()  # remove if main thread is polling self.keys
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
