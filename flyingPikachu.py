__author__ = 'danny12823125@gmail.com'

from cProfile import run
from webbrowser import BackgroundBrowser

import pygame
import random
from time import sleep

import sys
import importlib

from gpio.ultrasonic import *
from gpio.button import *

WHITE = (255,255,255)
RED = (255, 0, 0)
pad_width = 1024
pad_height = 512
background_width = 1024
aircraft_width = 90
aircraft_height = 55

ball_width = 250
ball_height = 250

fireball1_width = 140
fireball1_height = 60
fireball2_width = 86
fireball2_height = 60


# 게임오버 화면
def textObj(text, font) :
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

def dispMessage(text):
    global gamepad

    largeText = pygame.font.Font('freesansbold.ttf', 90)
    TextSurf, TextRect = textObj(text, largeText)
    TextRect.center = ((pad_width/2), (pad_height/2))
    gamepad.blit(TextSurf, TextRect)
    pygame.display.update()
    #runGame()


# 충돌 return 다음 액션값
def crash():
    global gamepad, ultra, gkey
    dispMessage('<- to retry, -> to quit')
    
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT : 
                    return "flyingPikachu"
                elif event.key == pygame.K_RIGHT :
                    return "select_menu"

        if gkey != None:
            if gkey.getCurPressedKey("UP") :
                return "flyingPikachu"
            elif gkey.getCurPressedKey("DOWN") :
                return "select_menu"
        clock.tick(60)

def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))

# 게임실행
def runGame():
    global gamepad, aircraft, clock, background1, background2, ultra
    global ball, fires

    x = pad_width * 0.05
    y = pad_height * 0.8
    y_change = 0

    background1_x = 0
    background2_x = background_width

    ball_x = pad_width
    ball_y = random.randrange(0, pad_height)

    fire_x = pad_width
    fire_y = random.randrange(0, pad_height)
    random.shuffle(fires)
    fire = fires[0]

    max_y = float(pad_height - aircraft_height)

    replayGame = False
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5

                # bullet 빠짐

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
        

        # 게임패드 초기화
        gamepad.fill(WHITE)
        
        # 배경화면 그리기
        background1_x -= 2
        background2_x -= 2

        if background1_x == -background_width:
            background1_x = background_width

        if background2_x == -background_width:
            background2_x = background_width

        drawObject(background1, background1_x, 0)
        drawObject(background2, background2_x, 0)

        # s:울트라센서
        if ultra != None :
            distance = (ultra.distance -10.0)*10.0

            if distance <0.0 :
                y = 0.0
            elif distance > max_y:
                y = max_y
            else :
                y = distance
            
            y = max_y - distance

            # print("distance:" + str(y))
        # e:울트라센서

        # 피카츄 위치
        if y_change != 0 :
            y += y_change
            if y < 0:
                y = 0
            elif y > pad_height - aircraft_height:
                y = pad_height - aircraft_height
        
        # 찌리리공 위치
        ball_x -= 7
        if ball_x <= 0:
            ball_x = pad_width
            ball_y = random.randrange(0, pad_height)
        
        # 파이어볼 위치
        if fire[1] == None:
            fire_x -= 30
        else:
            fire_x -= 15

        if fire_x <= 0:
            fire_x = pad_width
            fire_y = random.randrange(0, pad_height)
            random.shuffle(fires)
            fire = fires[0]

        # 불릿 제외함

        #-----------------
        # 충돌 (피카츄 -> 찌리리공)
        # if x + aircraft_width > ball_x:
        #     if(y > ball_y and y < ball_y + ball_height) or \
        #     (y + aircraft_height > ball_y and y + aircraft_height < ball_y + ball_height):
        #         return crash()

        # # 충돌 (피카츄 -> 파이어볼)
        # if fire[1] != None :
        #     if fire[0] == 0 :
        #         fireball_width = fireball1_width
        #         fireball_height = fireball1_height
        #     elif fire[0] == 1 :
        #         fireball_width = fireball2_width
        #         fireball_height = fireball2_height
            
        #     if x + aircraft_width > fire_x :
        #         if (y > fire_y and y < fire_y + fireball_height) or \
        #         (y + aircraft_height > fire_y and y + aircraft_height < fire_y + fireball_height) :
        #             return crash()
        #-----------------


        drawObject(aircraft, x, y)
        drawObject(ball, ball_x, ball_y)
       
        if fire[1] != None:
            drawObject(fire[1], fire_x, fire_y)


        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
    cleanupGPIO()

def initGame():
    global gamepad, aircraft, clock, background1, background2, ultra, gkey
    global ball, fires

    fires = []

    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('Flying Pikachu')
    aircraft = pygame.image.load("images/flyingPikachu_Pikachu.png")
    background1 = pygame.image.load('images/flyingPikachu_background.png')
    background2 = background1.copy()
    
    ball = pygame.image.load('images/flyingPikachu_ball.png')

    fires.append((0, pygame.image.load('images/flyingPikachu_fireball.png')))
    fires.append((1, pygame.image.load('images/flyingPikachu_fireball2.png')))

    for i in range(3):
        fires.append((i+2, None))

    clock = pygame.time.Clock()

    gkey = GPIOKey()
    if gkey != None:
        gkey.daemon = True
        gkey.start()

    ultra = Ultrasonic()
    if ultra != None :
        ultra.daemon = True
        ultra.start()

    while True :

        importModule = runGame()

        
        if importModule == "flyingPikachu":
            continue
        elif importModule != None :
            if importModule in sys.modules:
                importlib.reload(sys.modules[importModule])
            else:
                module = __import__(importModule)

        if ultra != None:
            ultra.endGame()
        break

    # while True:
    #     importModule = runGame()
    #     if importModule == "replay" :
    #         continue
    #     elif importModule == "select_menu" :
    #         import select_menu
    #         ultra.endGame()
    #         break
    #     else :
    #         break
    

if __name__ == '__main__':
    initGame()
else :
    print("flyingPikachu")
    initGame()
