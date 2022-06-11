import RPi.GPIO as GPIO
import time

import threading
"""
TRIG_PIN = 20
ECHO_PIN = 21
def initUltrasonic():
	GPIO.setup(TRIG_PIN, GPIO.OUT)
	GPIO.setup(ECHO_PIN, GPIO.IN)
def controlUltrasonic():
	distance = 0.0
	GPIO.output(TRIG_PIN, False)
	time.sleep(0.5)
	GPIO.output(TRIG_PIN, True)
	time.sleep(0.00001)
	GPIO.output(TRIG_PIN, False)
	while GPIO.input(ECHO_PIN) == 0 :
		pulse_start = time.time()
	while GPIO.input(ECHO_PIN) == 1 :
		pulse_end = time.time()
	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17000
	distance = round(distance, 2)
	return distance
def main():
	GPIO.setmode(GPIO.BCM)
	distance = 0.0
	initUltrasonic()
	print("Ultrasonic Operating...")
	try:
		while True:
			distance = controlUltrasonic()
			print("Distance:%.2f cm"%distance)
	except KeyboardInterrupt:
		GPIO.cleanup()

if __name__ == '__main__':
	main()
"""

class Ultrasonic(threading.Thread):

    def __init__(self) :
        super().__init__()

    def __new__(cls):
        if not hasattr(cls,'instance'):
            print('create')
            cls.instance = super(Ultrasonic, cls).__new__(cls)

            cls.instance.TRIG_PIN = 20
            cls.instance.ECHO_PIN = 21

            cls.instance.distance = 0.0

            # GPIO.setmode(GPIO.BCM)
            GPIO.setup(cls.instance.TRIG_PIN, GPIO.OUT)
            GPIO.setup(cls.instance.ECHO_PIN, GPIO.IN)

            cls.instance.isStart = False
        else:
            print('recycle')
        return cls.instance


    def controlUltrasonic(self):
        distance = 0.0
        GPIO.output(self.TRIG_PIN, False)
        time.sleep(0.5)
        GPIO.output(self.TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG_PIN, False)
        while GPIO.input(self.ECHO_PIN) == 0 :
            pulse_start = time.time()
        while GPIO.input(self.ECHO_PIN) == 1 :
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)

        print(distance)

        return distance

    def run(self) :
        if self.isStart :
            return
        else :
            self.isStart = True
            print("start!")
        

        while self.isStart:
            self.distance = self.controlUltrasonic()

            
    def endGame(self) :
        self.isStart = False

