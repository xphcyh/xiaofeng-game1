import pgzrun
import random

# 需要导入的模块
from pgzero.actor import Actor
from pgzero import music
from pgzero import keyboard
from pgzero import clock
from pgzero import screen

# 游戏配置
CAR_IMAGES = ['car1.png', 'car2.png', 'car3.png']
MUSIC_NAME = '1.mp3'
GAME_TIME = 30
LEFT_SPEED = 15
RIGHT_SPEED = 15
COIN_SPEED = 10
BANANA_SPEED = 12

# 游戏窗口尺寸
WIDTH = 960
HEIGHT = 720

# 游戏状态变量
game_state = {
    'is_loose': False,
    'skill_active': False,
    'time': GAME_TIME,
    'score': 0,
    'car_num': random.randint(1, 3),
    'coin_num': random.randint(1, 3),
    'banana_num': 1,
    'skill_num': random.randint(1, 3),
    'rotation': 0,
    'skill2_y': 1200,
    'end_shown': False
}

# 计算香蕉皮的位置（不能与金币在同一车道）
def calculate_banana_num():
    for i in range(1, 4):
        if i != game_state['coin_num']:
            return i
    return 1

game_state['banana_num'] = calculate_banana_num()

# 车道位置配置
coin_list = {1: 450, 2: 500, 3: 540}
coin_pos = {1: 390, 2: 500, 3: 580}
banana_list = {1: 450, 2: 480, 3: 540}
banana_pos = {1: 390, 2: 480, 3: 580}
car_pos = {1: 500, 2: 480, 3: 455}
skill_pos = {1: 500, 2: 480, 3: 455}

# 游戏对象
bg = Actor('bg1.png', (480, 360))
bg_num = 1

car1 = Actor(CAR_IMAGES[game_state['car_num']-1], (car_pos[game_state['car_num']], -200))
car1.scale = 1.3

car_ = Actor('car1.png', (480, 630))

coin = Actor('coin.png', (coin_pos[game_state['coin_num']], 40))

banana = Actor('banana.png', (banana_pos[game_state['banana_num']], 40))

# 技能相关
skill = Actor("skill.png", (skill_pos[game_state['skill_num']], -200))
skill.scale = 1.3

skill2 = Actor("skill2.png", (480, game_state['skill2_y']))
skill2.scale = 1.3

# UI元素
left = Actor('left.png', (70, 650))
right = Actor('right.png', (890, 650))
time_icon = Actor('time.png', (70, 50))
coin_icon = Actor('coinum.png', (870, 50))
end_bg = Actor('bg_1.png', (480, 360))
game_over = Actor('end.png', (480, 360))
score_board = Actor('fen.png', (480, 360))
score_board.scale = 0.5

# 移动端控制
direction = ''

def on_mouse_down(pos):
    """处理鼠标点击事件"""
    global direction
    if left.collidepoint(pos):
        direction = 'left'
    elif right.collidepoint(pos):
        direction = 'right'

def bg_move():
    """背景动画"""
    global bg_num
    if not game_state['is_loose']:
        bg_num += 1
        if bg_num > 14:
            bg_num = 1
        bg.image = 'bg' + str(bg_num) + '.png'

def timer():
    """游戏计时器"""
    global game_state
    if not game_state['is_loose']:
        game_state['time'] -= 1
        if game_state['time'] <= 0:
            game_state['is_loose'] = True

def activate_skill():
    """激活技能"""
    global game_state
    game_state['skill_active'] = True
    game_state['skill2_y'] = 1200

def reset_objects():
    """重置游戏对象位置"""
    global game_state
    # 重置对向车
    car1.y = -200
    game_state['car_num'] = random.randint(1, 3)
    car1.x = car_pos[game_state['car_num']]
    car1.image = CAR_IMAGES[game_state['car_num']-1]
    
    # 重置金币
    coin.y = -50
    game_state['coin_num'] = random.randint(1, 3)
    coin.x = coin_list[game_state['coin_num']]
    
    # 重置香蕉皮
    banana.y = -50
    game_state['banana_num'] = calculate_banana_num()
    banana.x = banana_list[game_state['banana_num']]
    
    # 重置技能
    skill.y = -200
    game_state['skill_num'] = random.randint(1, 3)
    skill.x = skill_pos[game_state['skill_num']]

def update():
    """游戏主循环更新函数"""
    global direction, game_state
    
    # 背景音乐
    if not music.is_playing(MUSIC_NAME):
        music.play(MUSIC_NAME)
    
    # 检查游戏结束状态
    if game_state['is_loose']:
        # 隐藏游戏对象
        banana.pos = (1500, 1500)
        car1.pos = (1500, 1500)
        coin.pos = (1500, 1500)
        skill.pos = (1500, 1500)
        skill2.pos = (1500, 1500)
        return
    
    # 车辆控制
    if (keyboard.keyboard.right or direction == 'right') and car_.x + 10 < 870:
        car_.x += RIGHT_SPEED + (5 if direction == 'right' else 0)
        direction = ''
        
    if (keyboard.keyboard.left or direction == 'left') and car_.x - 10 > 70:
        car_.x -= LEFT_SPEED + (5 if direction == 'left' else 0)
        direction = ''
    
    # 根据车辆位置改变车辆图像
    if car_.x > 800:
        car_.image = 'car1_r.png'
        car_.scale = 1.1
    elif car_.x < 100:
        car_.image = 'car1_f.png'
        car_.scale = 1.1
    else:
        car_.image = 'car1.png'
        car_.scale = 1.0
    
    # 对向车移动
    if game_state['car_num'] == 1:
        car1.angle = -30
        car1.y += 10
        car1.x -= 5
    elif game_state['car_num'] == 3:
        car1.angle = 30
        car1.y += 10
        car1.x += 5
    else:
        car1.angle = 0
        car1.y += 12
    
    # 对向车重置
    if car1.y > HEIGHT:
        reset_objects()
    
    # 金币移动
    if game_state['coin_num'] == 1:
        coin.y += COIN_SPEED
        coin.x -= COIN_SPEED / 1.5
    elif game_state['coin_num'] == 3:
        coin.y += COIN_SPEED
        coin.x += COIN_SPEED / 1.5
    else:
        coin.y += COIN_SPEED
    
    # 金币重置
    if coin.y > HEIGHT:
        reset_objects()
    
    # 香蕉皮移动
    if game_state['banana_num'] == 1:
        banana.y += BANANA_SPEED
        banana.x -= BANANA_SPEED / 1.5
    elif game_state['banana_num'] == 3:
        banana.y += BANANA_SPEED
        banana.x += BANANA_SPEED / 1.5
    else:
        banana.y += BANANA_SPEED
    
    # 香蕉皮重置
    if banana.y > HEIGHT:
        reset_objects()
    
    # 技能球移动
    if game_state['skill_num'] == 1:
        skill.y += 12
        skill.x -= 6
    elif game_state['skill_num'] == 3:
        skill.y += 12
        skill.x += 6
    else:
        skill.y += 12
    
    # 技能球重置
    if skill.y > HEIGHT:
        skill.y = -200
        game_state['skill_num'] = random.randint(1, 3)
        skill.x = skill_pos[game_state['skill_num']]
    
    # 碰到技能球
    if car_.colliderect(skill):
        skill.y = -200
        game_state['skill_num'] = random.randint(1, 3)
        skill.x = skill_pos[game_state['skill_num']]
        activate_skill()
    
    # 释放技能
    if game_state['skill_active']:
        skill2.y -= 45
        if skill2.y <= -600:
            game_state['skill_active'] = False
            skill2.y = 1200
    
    # 技能影响其他对象
    if skill2.colliderect(car1):
        car1.y = -200
        game_state['car_num'] = random.randint(1, 3)
        car1.x = car_pos[game_state['car_num']]
        car1.image = CAR_IMAGES[game_state['car_num']-1]
    
    if skill2.colliderect(banana):
        banana.y = -50
        game_state['banana_num'] = calculate_banana_num()
        banana.x = banana_list[game_state['banana_num']]
    
    if skill2.colliderect(skill):
        skill.y = -200
        game_state['skill_num'] = random.randint(1, 3)
        skill.x = skill_pos[game_state['skill_num']]
    
    # 收集金币
    if car_.colliderect(coin):
        coin.y = -50
        game_state['coin_num'] = random.randint(1, 3)
        coin.x = coin_list[game_state['coin_num']]
        game_state['score'] += 1
    
    # 碰到香蕉皮（旋转效果）
    if car_.colliderect(banana):
        banana.y = -50
        game_state['banana_num'] = calculate_banana_num()
        banana.x = banana_list[game_state['banana_num']]
        game_state['rotation'] = 0
        clock.clock.schedule_interval(rotate_car, 0.01)
    
    # 两车相撞
    if car_.colliderect(car1):
        game_state['is_loose'] = True
        car1.y = -1000

def rotate_car():
    """车辆旋转效果"""
    global game_state
    if game_state['is_loose']:
        clock.clock.unschedule(rotate_car)
        car_.angle = 0
        return
        
    game_state['rotation'] += 10
    car_.angle = game_state['rotation']
    
    if game_state['rotation'] >= 720:
        clock.clock.unschedule(rotate_car)
        car_.angle = 0
        game_state['rotation'] = 0

def draw():
    """绘制游戏画面"""
    # 绘制背景
    bg.draw()
    
    # 如果游戏结束，显示结束画面
    if game_state['is_loose']:
        show_end_screen()
        return
    
    # 绘制游戏对象
    car1.draw()
    car_.draw()
    coin.draw()
    banana.draw()
    skill.draw()
    skill2.draw()
    
    # 绘制UI
    left.draw()
    right.draw()
    time_icon.draw()
    coin_icon.draw()
    
    # 绘制时间
    time_text = str(game_state['time']) + 'S'
    text_x = 54 if game_state['time'] <= 9 else 44
    screen.screen.draw.text(time_text, (text_x, 33), fontsize=26, color='white')
    
    # 绘制分数
    screen.screen.draw.text(str(game_state['score']), (874, 23), fontsize=40, color='white')

def show_end_screen():
    """显示游戏结束画面"""
    global game_state
    if not game_state['end_shown']:
        # 播放结束音乐
        music.play_once('win.mp3')
        game_state['end_shown'] = True
    
    end_bg.draw()
    game_over.draw()
    score_board.draw()
    
    # 绘制最终分数
    score_text_x = 462 if game_state['score'] >= 10 else 472
    screen.screen.draw.text(str(game_state['score']), (score_text_x, 409), fontsize=40, color='white')

# 启动定时器
clock.clock.schedule_interval(bg_move, 0.1)
clock.clock.schedule_interval(timer, 1)

# 启动游戏
pgzrun.go()