import RPi.GPIO as GPIO
from time import sleep
import threading

class GPIOKey(threading.Thread):

    def __init__(self) :
        super().__init__()

        self.UP_PIN = 15
        self.DOWN_PIN = 16
        self.CON_PIN = 17
        self.X_PIN = 18

        self.UP=0
        self.DOWN=0
        self.CON=0
        self.X =0

        self.curPressedKey = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.UP_PIN,GPIO.IN)
        GPIO.setup(self.DOWN_PIN,GPIO.IN)
        GPIO.setup(self.CON_PIN,GPIO.IN)
        GPIO.setup(self.X_PIN,GPIO.IN)

    def __new__(cls):
        if not hasattr(cls,'instance'):
            print('create')
            cls.instance = super(GPIOKey, cls).__new__(cls)
        else:
            print('recycle')
        return cls.instance

    def run(self):
        while True:
            if GPIO.input(self.UP_PIN) == 0:
                self.UP = self.UP + 1
            else :
                self.UP = 0
            if GPIO.input(self.DOWN_PIN) == 0:
                self.DOWN = self.DOWN + 1
            else :
                self.DOWN = 0
            if GPIO.input(self.CON_PIN) == 0:
                self.CON = self.CON + 1
            else :
                self.CON = 0
            if GPIO.input(self.X_PIN) == 0:
                self.X = self.X + 1
            else :
                self.X = 0

            if self.UP == 1:
                self.curPressedKey = "UP"
            elif self.DOWN == 1:
                self.curPressedKey = "DOWN"
            elif self.CON == 1:
                self.curPressedKey = "CON"
            elif self.X == 1:
                self.curPressedKey = "X"
            
            if bool(self.UP) | bool(self.DOWN) | bool(self.CON) | bool(self.X) == False :
                self.curPressedKey = False
            
            sleep(0.1)
    
    def getCurPressedKey(self, key) :
        if(self.curPressedKey == key):
            self.curPressedKey = False
            return True

    @classmethod
    def cleanupGPIO(cls) :
        GPIO.cleanup()
    

def testButton():
    t = GPIOKey()
    t.daemon = True
    t.start()
    try:
        while True:
            if t.getCurPressedKey("UP") :
                print("UP")
            elif t.getCurPressedKey("DOWN") :
                print("DOWN")
            elif t.getCurPressedKey("CON") :
                print("CON")
            elif t.getCurPressedKey("X") :
                print("X")
            sleep(1.0)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    testButton()