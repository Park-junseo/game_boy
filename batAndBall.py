import pygame, sys 
from pygame.locals import *

# 설정
pygame.init() # 초기화
screen = pygame.display.set_mode((480, 320)) # 화면 크기 설정
pygame.display.set_caption('벽돌깨기')
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 1)

# 색깔 변수
Black = (0, 0, 0) 
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 공 변수
x = int(480 / 2)
y = 320 - 30
dx = 10
dy = 10

# 패달 변수
paddleHeight = 10
paddleWidth = 75
paddleX = (480 - paddleWidth) / 2
paddle = pygame.Rect(paddleX, 320-paddleHeight-10, paddleWidth, paddleHeight)

# 벽돌
bricks = []
for c in range(6) :
    for r in range(5) :
        brick = pygame.Rect(c*(60 + 10)+35, r*(16+5)+24, 60, 16)
        bricks.append(brick)


# draw 함수 정의
def drawBall():
    pygame.draw.circle(screen,(0, 221, 149), (int(x), int(y)), 7)

def drawPaddle():
    pygame.draw.rect(screen, (0,221,149), paddle)

def draw():
    screen.fill(Black)
    drawBall()

def drawbrick():
    for brick in bricks:
        pygame.draw.rect(screen, (0, 221, 149), brick)



while True:
    #이벤트 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        # 키 이벤트 처리
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle.left -= 1
                paddleX -= 1
            elif event.key == pygame.K_RIGHT:
                paddle.right += 1
                paddleX += 1


    # 그리기 함수 호출
    draw()
    drawPaddle()
    drawbrick()

    # 공과 벽돌 충돌 검사
    if x + dx > 480-7 or x + dx < 7 :
        dx = -dx
    if y + dy < 7:
        dy = -dy
    elif(y + dy > 300): # 실패시 종료
        if x+10 > paddleX and x < paddleX + paddleWidth: #페달에 닿으면 튕기기
            dy = -dy
        else: 
            sys.exit()
    
    for b in bricks: 
        if x > b.x and x < b.x+b.width and y > b.y and y < b.y+b.height:
            dy = -dy
            bricks.remove(b)

    
    # 공 이동
    x += dx
    y += dy

    # 모듈 갱신
    pygame.display.update()

    #프레임 변경
    clock.tick(30)