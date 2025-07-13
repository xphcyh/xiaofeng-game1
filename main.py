import pgzrun
import random
#print('点赞了吗')
#while True :
 #   a=str(input())
#    if a=='点了':
#        print('信你一回')
#        break 
#    else :
       # while True :
            #print('先赞后玩')
        
    
#更换背景音乐
bgm = 'bgm1.mp3'
#更换关卡（1_3）
r = 1

music.play(bgm)
WIDTH = 960
HEIGHT = 720
start = Actor('开始游戏.png',[480,360])
bg = Actor('背景.png',[480,360])
success = Actor('成功.png')
fail = Actor('失败.png')
r2 = Actor('第二关.png')
r3 = Actor('第三关.png')
r4 = Actor('奖励关卡.png')
st = '游戏开始'
canmove = [25,35,14,8,9,15]
moved = []
cards = []
slot = []
post = [[280, 620], [345, 620], [410, 620], [475, 620], [540, 620], [605,620], [670, 620]]

def init():
    global slot,cards
    slot.clear()
    cards.clear()
    if r == 1:
        #更换第1关卡牌，每张卡牌的出现次数需要是3的倍数！
        actors = ['1_2.png', '1_1.png', '1_3.png', '1_2.png', '1_1.png', '1_3.png', '1_2.png', '1_1.png', '1_3.png', '1_2.png','1_1.png', '1_3.png', '1_2.png', '1_1.png', '1_3.png', '1_2.png', '1_1.png', '1_3.png']
        random.shuffle(actors)
        for i in range(9):
            card = Actor(actors[i], (240 * (i % 3 + 1), 160 * (i // 3 + 1) - 20))
            card.p = 0
            card.level=1
            cards.append(card)
        for i in range(9):
            card = Actor(actors[i + 9], (240 * (i % 3 + 1), 160 * (i // 3 + 1)))
            card.p = 1
            card.level=3
            cards.append(card)
    if r == 2:
        #更换第2关卡牌，每张卡牌的出现次数需要是3的倍数！
        actors = ['2_1.png','2_1.png','2_1.png','2_1.png','2_1.png','2_1.png','2_2.png','2_2.png','2_2.png','2_2.png','2_2.png','2_2.png','2_3.png','2_3.png','2_3.png','2_3.png','2_3.png','2_3.png','2_4.png','2_4.png','2_4.png','2_4.png','2_4.png','2_4.png','2_5.png','2_5.png','2_5.png','2_5.png','2_5.png','2_5.png']
        actors = ['1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_!.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png']
        random.shuffle(actors)
        for i in range(12):
            card = Actor(actors[i], (65+120 * (i % 6 + 1), 160 * (i // 6 + 1) - 20))
            card.p = 0
            card.level = 1
            cards.append(card)
        for i in range(18):
            card = Actor(actors[i + 12], (65+120 * (i % 6 + 1), 160 * (i // 6 + 1)))
            card.p = 1
            card.level = 3
            cards.append(card)
    if r == 3:
        #更换第3关卡牌，每张卡牌的出现次数需要是3的倍数！
        actors = ['3_1.png','3_1.png','3_1.png','3_1.png','3_1.png','3_1.png','3_2.png','3_2.png','3_2.png','3_3.png','3_3.png','3_3.png','3_3.png','3_3.png','3_3.png','3_4.png','3_4.png','3_4.png','3_5.png','3_5.png','3_5.png','3_5.png','3_5.png','3_5.png','3_6.png','3_6.png','3_6.png','3_6.png','3_6.png','3_6.png','3_7.png','3_7.png','3_7.png','3_8.png','3_8.png','3_8.png']
    if r==4:
        actors = ['1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png','1_1.png']
        
        random.shuffle(actors)
        x = 0
        for i in range(5):
            card = Actor(actors[x], (300+200- i*30, 200+30+i*30))
            card.p = 0
            card.n = x
            cards.append(card)
            x+=1
            card = Actor(actors[x], (300+200+ i*30,200+30+i*30))
            card.p = 0
            card.n = x
            cards.append(card)
            x+=1
        for i in range(3):
            card = Actor(actors[x], (300+200- i*30, 200+90+i*30))
            card.p = 0
            card.n = x
            cards.append(card)
            x+=1
            card = Actor(actors[x], (300+200+ i*30,200+90+i*30))
            card.p = 0
            card.n = x
            cards.append(card)
            x+=1
            
     
        for i in range(10):
            card = Actor(actors[x], (300+i*10+50, 200+210))
            card.p = 1
            card.n = x
            cards.append(card)
            x+=1
        for i in range(10):
            card = Actor(actors[x], (300+350-i*10, 200+210))
            card.p = 1
            card.n = x
            cards.append(card)
            x+=1
init()

def judge():
    global slot,st,r
    if st=='游戏中':
        if len(slot)>2:
            if len(slot)==3:
                if slot[0].image == slot[1].image and slot[1].image == slot[2].image:
                    slot.clear()
            else:
                for i in range(len(slot) - 2):
                    if i+2<len(slot):
                        if slot[i].image == slot[i + 1].image and slot[i + 1].image == slot[i + 2].image:
                            slot = slot[:i] + slot[i + 3:]
                            for x in range(len(slot)):
                                slot[x].pos = post[x]
                            judge()
                    else:
                        break
        if len(cards)==0:
            r +=1
            if r < 5:
                st = '游戏开始'
                init()
            else:
                st ='游戏成功'

        if len(slot) > 6 :
            st = '游戏失败'
            return


def draw():
    global st
    if st == '游戏开始':
        if r == 1:
            start.draw()
        elif r == 2:
            r2.draw()
        elif r == 3:
            r3.draw()
        elif  r==4:
            r4.draw()
        else:
            st = '游戏成功'
    if st == '游戏中':
        bg.draw()
        for card in cards:
            card.draw()
        for card in slot:
            card.draw()
    if st == '游戏失败':
        fail.draw()
    if st=='游戏成功':
        success.draw()


def on_mouse_down(pos):
    global st, slot
    if st == '游戏开始':
        st = '游戏中'
        return
    if st == '游戏中':
        for card in cards[::-1]:
            if card.collidepoint(pos):
                if r<3:
                    if card.level<3:
                        break
                    if card.level==3:
                        t = 9
                        if r==2:
                            t=18
                        for x in cards[:t]:
                            if x.x==card.x and x.y==card.y-20:
                                x.level=4
                                break
                else:
                    if card.n not in canmove:
                        break
                    if card.n>25: 
                        if card.n!=26:
                            for tt in cards:
                                if tt.n==card.n-1:
                                    canmove.append(tt.n)
                                    break
                    elif card.n<=25 and card.n>=16:
                        if card.n!=16:
                            for tt in cards:
                                if tt.n==card.n-1:
                                    canmove.append(tt.n)
                                    break
                    else:
                        moved.append(card.n)
                        if 1 in moved and 2 in moved and 3 in moved:
                            canmove.append(0)
                        if 2 in moved and 3 in moved :
                            canmove.append(1)
                        if 4 in moved and 10 in moved :
                            canmove.append(2)
                        if 5 in moved and 11 in moved :
                            canmove.append(3)
                        if 6 in moved and 12 in moved :
                            canmove.append(4)
                        if 7 in moved and 13 in moved :
                            canmove.append(5)
                        if 8 in moved and 14 in moved :
                            canmove.append(6)
                        if 9 in moved and 15 in moved :
                            canmove.append(7)
                        if 11 in moved and 12 in moved  and 13 in moved:
                            canmove.append(10)
                        if 12 in moved and 13 in moved :
                            canmove.append(11)
                        if 14 in moved :
                            canmove.append(12)
                        if 15 in moved :
                            canmove.append(13)
                if len(slot) > 0:
                    for i in range(len(slot)):
                        if slot[i].image == card.image:
                            slot = slot[:i + 1] + [card] + slot[i + 1:]
                            for x in range(len(slot)):
                                slot[x].pos = post[x]
                            break
                    else:
                        card.pos = post[len(slot)]
                        slot.append(card)
                else:
                    card.pos = post[0]
                    slot.append(card)
                cards.remove(card)
                break
        clock.schedule_unique(judge, 0.1)

pgzrun.go()