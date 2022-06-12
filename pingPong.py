import sys
import math
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, Rect, KEYUP
import time

from gpio.ultrasonic import *
from gpio.button import *

import importlib

class Block:
    """ 블록, 공, 패들 오브젝트 """
    def __init__(self, col, rect, speed=0):
        self.col = col
        self.rect = rect
        self.speed = speed
        self.dir = random.randint(-45, 45) + 270

    def move(self):
        """ 공을 움직인다 """
        self.rect.centerx += math.cos(math.radians(self.dir))\
             * self.speed
        self.rect.centery -= math.sin(math.radians(self.dir))\
             * self.speed

    def draw(self):
        """ 블록, 공, 패들을 그린다 """
        if self.speed == 0:
            pygame.draw.rect(SURFACE, self.col, self.rect)
        else:
            pygame.draw.ellipse(SURFACE, self.col, self.rect)

# 피버 타임 이벤트
def feverTime():
    global BALLS

    # 공 두개 추가
    for i in range(2):
        BALLS.append(Block((200, 242, 0), Rect(300, 400, 20, 20), 10))

    # 공의 속도 15
    for BALL in BALLS:
        BALL.speed = 15

def tick():
    """ 프레임별 처리 """
    global BALLS, BLOCKS, score, isFeverTime, startTime, endTime, ultra, gkey, min_x, max_x

    # 키 입력 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            cleanupGPIO()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                PADDLE.rect.centerx -= 10
            elif event.key == K_RIGHT:
                PADDLE.rect.centerx += 10

    # s:울트라센서
    if ultra != None :
        distance = int((ultra.distance -10.0)*15.0)
        PADDLE.rect.centerx = distance
        print("distance:" + str(distance))
    # e:울트라센서

    if PADDLE.rect.centerx < min_x :
        PADDLE.rect.centerx = min_x
    elif PADDLE.rect.centerx > max_x :
        PADDLE.rect.centerx = max_x

    for BALL in BALLS:
        if BALL.rect.centery < 1000:
            BALL.move()

        # 블록과 충돌하면
        prevlen = len(BLOCKS)
        BLOCKS = [x for x in BLOCKS
                if not x.rect.colliderect(BALL.rect)]
        if len(BLOCKS) != prevlen:
            BALL.dir *= -1
            score += 100 # get score + 100

        # 점수가 1000점이고, 피버타임이 아니면 피버타임으로 진입한다.
        if score == 1000 and isFeverTime == False:
            isFeverTime = True
            feverTime()
        # 10초를 카운트하고 10초 뒤에는 피버타임을 off한다.
        elif isFeverTime == True:    
            if startTime == 0.0:
                startTime = time.time()
            elif startTime != 0.0:
                endTime = time.time()
                if endTime - startTime >= 10: # 10초
                    isFeverTime = False

        # 패들과 충돌하면
        if PADDLE.rect.colliderect(BALL.rect):
            BALL.dir = 90 + (PADDLE.rect.centerx - BALL.rect.centerx) \
                / PADDLE.rect.width * 80

        # 벽과 충돌하면
        if BALL.rect.centerx < 0 or BALL.rect.centerx > 600:
            BALL.dir = 180 - BALL.dir
        if BALL.rect.centery < 0:
            BALL.dir = -BALL.dir
            BALL.speed = 15

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((600, 800))
FPSCLOCK = pygame.time.Clock()
BLOCKS = []
PADDLE = Block((242, 242, 0), Rect(300, 700, 100, 30))
BALLS = [Block((242, 242, 0), Rect(300, 400, 20, 20), 10)]

isNeedToRestart = False
isFeverTime = False
score = 0
startTime = 0.0
endTime = 0.0

# 초기화
def init():
    global SURFACE, FPSCLOCK, BLOCKS, PADDLE, BALLS, isNeedToRestart, isFeverTime, score, startTime, endTime, min_x, max_x

    pygame.init()
    pygame.key.set_repeat(5, 5)
    SURFACE = pygame.display.set_mode((600, 800))
    FPSCLOCK = pygame.time.Clock()
    BLOCKS = []
    PADDLE = Block((242, 242, 0), Rect(300, 700, 100, 30))
    BALLS = [Block((242, 242, 0), Rect(300, 400, 20, 20), 10)]
    isNeedToRestart = False
    isFeverTime = False
    score = 0
    startTime = 0.0
    endTime = 0.0

    min_x = 50
    max_x = 550

def main():
    global isNeedToRestart, score, isFeverTime, startTime, endTime, gkey, ultra, min_x, max_x

    myfont = pygame.font.SysFont(None, 80)
    smallfont = pygame.font.SysFont(None, 36)
    scorefont = pygame.font.SysFont(None, 25)
    mess_clear = myfont.render("Cleared!", True, (255, 255, 0))
    mess_over = myfont.render("Game Over!", True, (255, 255, 0))
    mess_replay = smallfont.render("replay (press r)", True, (255, 0, 0))
    mess_back = smallfont.render("select menu (press q)", True, (255, 0, 0))
    fps = 30
    colors = [(255, 0, 0), (255, 165, 0), (242, 242, 0),
              (0, 128, 0), (128, 0, 128), (0, 0, 250)]
    min_x = 50
    max_x = 550

    importModule = None

    # 블록 추가
    for ypos, color in enumerate(colors, start=0):
        for xpos in range(0, 5):
            BLOCKS.append(Block(color, Rect(xpos * 100 + 60, ypos * 50 + 40, 80, 30)))

    while True:
        tick()

        # 공 생성
        SURFACE.fill((0, 0, 0))
        for BALL in BALLS:
            BALL.draw()
        PADDLE.draw()

        # 블록 생성
        for block in BLOCKS:
            block.draw()        

        # 블록 모두 제거하면 성공
        if len(BLOCKS) == 0:
            SURFACE.blit(mess_clear, (200, 400))
        
        # 공이 패들 밑으로 내려가면 해당 공은 삭제
        for BALL in BALLS:
            if BALL.rect.centery > 800 and len(BLOCKS) > 0:
                BALLS.remove(BALL)

        # 피버타임이 끝난 경우
        if isFeverTime == False and startTime != 0.0 and endTime != 0.0:
            # 공 하나만 제외하고 모두 제거
            for BALL in BALLS:
                BALLS.remove(BALL)
                if(len(BALLS) == 1):
                    break
            startTime = 0.0
            endTime = 0.0
            # 속도 10으로 원복
            for BALL in BALLS:
                BALL.speed = 10

        # 공이 하나도 없는 경우(끝난 경우)
        if len(BALLS) <= 0:
            SURFACE.blit(mess_over, (150, 400))
            SURFACE.blit(mess_replay, (230, 460))
            SURFACE.blit(mess_back, (230, 480))
            isNeedToRestart = True

        # 스코어 보드
        mess_score = scorefont.render("score : " + str(score), True, (255, 255, 255))
        SURFACE.blit(mess_score, (10, 10))

        pygame.display.update()
        FPSCLOCK.tick(fps)

        # r키를 누르면 재시작 가능하도록 설정
        while isNeedToRestart:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == pygame.K_r:
                    isNeedToRestart = False
                    break
                if event.type == KEYDOWN and event.key == pygame.K_q:
                    importModule = "select_menu"
                if event.type == QUIT:
                    pygame.quit()
                    cleanupGPIO()
                    sys.exit()
                    break

            if gkey != None:
                if gkey.getCurPressedKey("UP") :
                    isNeedToRestart = False
                elif gkey.getCurPressedKey("DOWN") :
                    importModule = "select_menu"
            
            if importModule != None :
                ultra.endGame()
                if importModule in sys.modules:
                    importlib.reload(sys.modules[importModule])
                else:
                    module = __import__(importModule)
                return

            if isNeedToRestart == False:
                init()
                main()
                break

def initThread():
    global gkey, ultra
    gkey = GPIOKey()
    if gkey != None:
        gkey.daemon = True
        gkey.start()

    ultra = Ultrasonic()
    if ultra != None :
        ultra.daemon = True
        ultra.start()

if __name__ == '__main__':
    initThread()
    main()
else :
    initThread()
    main()