try: 
    import RPi.GPIO as GPIO
except:
    GPIO = None
import time

import threading


class Ultrasonic(threading.Thread):

    def __init__(self) :
        super().__init__()

    def __new__(cls):
        if not hasattr(cls,'instance'):
            print('create ultra')
            cls.instance = super(Ultrasonic, cls).__new__(cls)

            cls.instance.TRIG_PIN = 20
            cls.instance.ECHO_PIN = 21

            cls.instance.distance = 0.0

            cls.instance.isStart = False

            # GPIO.setmode(GPIO.BCM)
            if GPIO == None :
                return None

            GPIO.setup(cls.instance.TRIG_PIN, GPIO.OUT)
            GPIO.setup(cls.instance.ECHO_PIN, GPIO.IN)

            
        else:
            print('recycle ultra')

        return cls.instance


    def controlUltrasonic(self):

        distance = 0.0
        pulse_start = 0.0
        pulse_end = 0.0
        inturrupt = 0.0
        GPIO.output(self.TRIG_PIN, False)
        time.sleep(0.5)
        GPIO.output(self.TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG_PIN, False)
        inturrupt = time.time()
        while GPIO.input(self.ECHO_PIN) == 0 :
            pulse_start = time.time()
            if pulse_start - inturrupt > 0.02 :
                return self.distance

        inturrupt = time.time()
        while GPIO.input(self.ECHO_PIN) == 1 :
            pulse_end = time.time()
            if pulse_end - inturrupt > 0.02 :
                return self.distance
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)
        
        # print(distance)

        return distance

    def run(self) :
        if self.isStart :
            print("stop ultra!")
            return
        else :
            self.isStart = True
            print("start ultra!")
        
        while self.isStart == True and GPIO != None:
            self.distance = self.controlUltrasonic()

        print("end ultra")

            
    def endGame(self) :
        self.isStart = False

def cleanupGPIO():
    if GPIO != None:
        GPIO.cleanup()

