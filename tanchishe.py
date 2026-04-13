import pgzrun
import random

import pgzero.screen
from pgzero import screen
from pgzero.actor import Actor

HEIGHT = 600
WIDTH = 800
sList = []
bg = Actor('bg.png')
snakeHead = Actor('snake.png', [400, 300])
x = random.randint(10, 30) * 20
y = random.randint(10, 21) * 20
star = Actor('star.png', [x, y])
sList.append(snakeHead)
for i in range(1, 4):
    x = snakeHead.x - 20 * i
    snakeBody = Actor('snake.png', [x, 300])
    sList.append(snakeBody)

fx = 'right'
fs = 0
state = '1'


def draw():
    bg.draw()
    for s in sList:
        s.draw()
    star.draw()
    screen.draw.text('得分：' + str(fs), (50, 40), fontsize=40, color='red', fontname="simhei.ttf")
    if state == '0':
        bg.draw()
        screen.draw.text('Game Over !', center=[400, 300], fontsize=40, color='red', fontname="simhei.ttf")


def on_key_down():
    global fx
    if keyboard.left or keyboard.A:
        fx = 'left'
    if keyboard.right or keyboard.D:
        fx = 'right'
    if keyboard.up or keyboard.W:
        fx = 'up'
    if keyboard.down or keyboard.S:
        fx = 'down'


def sMove():
    global fx, fs, state
    newSHead = Actor('snake.png')
    if fx == 'right':
        newSHead.x = sList[0].x + 20
        newSHead.y = sList[0].y
    if fx == 'left':
        newSHead.x = sList[0].x - 20
        newSHead.y = sList[0].y
    if fx == 'up':
        newSHead.x = sList[0].x
        newSHead.y = sList[0].y - 20
    if fx == 'down':
        newSHead.x = sList[0].x
        newSHead.y = sList[0].y + 20
    sList.insert(0, newSHead)
    if star.collidepoint(sList[0].pos):
        star.x = random.randint(10, 30) * 20
        star.y = random.randint(10, 21) * 20
        fs += 1
    else:
        sList.remove(sList[-1])
    if sList[0].x < 10 or sList[0].x > 790 or sList[0].y < 10 or sList[0].y > 590:
        clock.unschedule(sMove)
        state = '0'
    for s in sList:
        if s == sList[0]:
            pass
        else:
            if s.collidepoint(sList[0].pos):
                state = '0'


clock.schedule_interval(sMove, 0.3)

pgzrun.go()