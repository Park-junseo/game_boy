import os
import pygame
from env import *
from pygame.surface import Surface

from gpio.button import GPIOKey

def drawMenuBg():
    global gamepad, menuBg
    gamepad.blit(menuBg,(0,0))

def initMenuList():
    global menuList, menuListFont, menuKey

    menuKey = 0
    menuListFont = pygame.font.SysFont("arial",40, True)
    menuList = [
        "FLYING PIKACHU",
        "NEW GAME",
        "Back"
    ]


def drawMenuList(curIndex):
    global gamepad, menuListFont, menuList

    index = 0

    textList:list[Surface] = []

    for text in menuList:
        backgroundColor = WHITE if curIndex == index else None
        textList.append(menuListFont.render(text, True, BLACK, backgroundColor))
        index += 1

    margin = 50
    initX = pad_width*0.5
    initY = (pad_hegith-margin*len(menuList))*0.5
    
    container = pygame.Surface((pad_width-160, margin*len(menuList)+20))
    container.set_alpha(80)

    pygame.draw.rect(container, (200,200,255), container.get_rect())
    
    gamepad.blit(container, (80, initY-10))

    index = 0
    for textButton in textList:
        gamepad.blit(textButton, (initX - textButton.get_width()*0.5, initY + index*margin))
        index += 1
        

def getMenuKey(delta):
    global menuList, menuKey
    length = len(menuList)
    key = (menuKey + delta) % length

    return key

def getMenuList(index):
    global menuList
    return menuList[index]

def runGame():
    global gamepad, clock, menuKey, gkey

    
    crashed =False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            #s: 키 조작

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menuKey = getMenuKey(-1)
                elif event.key == pygame.K_DOWN:
                    menuKey = getMenuKey(1)
                elif event.key == pygame.K_x:
                    crashed = True
                elif event.key == pygame.K_SPACE:
                    if getMenuList(menuKey) == "Back":
                        import gameboy_menu
                        gameboy_menu.initGame()
                        return

            #e: 키 조작

        #s: gpio 키조작
        if gkey != None :
            if gkey.getCurPressedKey("UP") :
                menuKey = getMenuKey(-1)
            elif gkey.getCurPressedKey("DOWN") :
                menuKey = getMenuKey(1)
            elif gkey.getCurPressedKey("X") :
                crashed = True
            elif gkey.getCurPressedKey("CON") :
                if getMenuList(menuKey) == "Back":
                    import gameboy_menu
                    gameboy_menu.initGame()
                    return
        #e: gpio 키조작

        #s: 화면 표시
        gamepad.fill(WHITE)
        drawMenuBg()
        drawMenuList(menuKey)
        pygame.display.update()
        #e: 화면 표시

        clock.tick(60)

    pygame.quit()

def initGame():
    global gamepad, clock, menuBg, gkey

    #s: 초기 설정
    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_hegith))
    menuBg = pygame.image.load(os.path.join(rpImages, rsMainBgSrc))#pygame.image.load(mainBgSrc).convert_alpha()
    initMenuList()

    if(GPIOKey.gpioKey == None):
        print("unset gpio!")
    gkey = GPIOKey.start()
    if(GPIOKey.gpioKey != None):
        print("set gpio!")
    #e: 초기 설정

    clock = pygame.time.Clock()
    runGame()

# 여기에서 실행 시 gameboy_menu로 실행
if __name__ == '__main__':
    import gameboy_menu
    gameboy_menu.initGame()