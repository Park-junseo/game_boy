import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(18, GPIO.IN)

try: 
    while True:
        if GPIO.input(18) == True:
            print("Detect!")
            GPIO.output(21, True)
            sleep(0.3)
        if GPIO.input(18) == False:
            GPIO.output(21, False)

except Keyboardinterrupt:
    GPIO.cleanup()