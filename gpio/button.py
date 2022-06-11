import RPi.GPIO as GPIO
from time import sleep
import threading

class GPIOKey(threading.Thread):

    def __init__(self) :
        super().__init__()

        print('init!')

    def __new__(cls):
        if not hasattr(cls,'instance'):
            print('create')
            cls.instance = super(GPIOKey, cls).__new__(cls)

            cls.instance.UP_PIN = 15
            cls.instance.DOWN_PIN = 16
            cls.instance.CON_PIN = 17
            cls.instance.X_PIN = 18

            cls.instance.UP=0
            cls.instance.DOWN=0
            cls.instance.CON=0
            cls.instance.X =0

            cls.instance.curPressedKey = False

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(cls.instance.UP_PIN,GPIO.IN)
            GPIO.setup(cls.instance.DOWN_PIN,GPIO.IN)
            GPIO.setup(cls.instance.CON_PIN,GPIO.IN)
            GPIO.setup(cls.instance.X_PIN,GPIO.IN)

            cls.instance.isStart = False
        else:
            print('recycle')
        return cls.instance

    def run(self):
        if self.isStart :
            return
        else :
            self.isStart = True
            print("start!")

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