import pgzrun
import random
from pgzero.actor import Actor
from pgzero.rect import Rect

# 游戏常量
WIDTH = 400
HEIGHT = 600
GRAVITY = 0.5
JUMP_SPEED = -10
SCROLL_SPEED = 5
OBSTACLE_FREQUENCY = 60  # 每60帧生成一次障碍物
COIN_FREQUENCY = 100     # 每100帧生成一次金币
ITEM_DURATION = 300      # 道具持续时间（5秒，基于60帧/秒）
# ITEM_FREQUENCY 已不再使用

# 玩家类
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.width = 40
        self.height = 60
        self.velocity_y = 0
        self.is_jumping = False
        self.lane = 1  # 0=左, 1=中, 2=右
        self.lanes_x = [WIDTH // 4, WIDTH // 2, WIDTH * 3 // 4]
        self.x = self.lanes_x[self.lane]
        
    def update(self):
        # 更新垂直速度
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # 地面碰撞检测
        if self.y > HEIGHT - 100:
            self.y = HEIGHT - 100
            self.velocity_y = 0
            self.is_jumping = False
            
        # 更新水平位置
        target_x = self.lanes_x[self.lane]
        if self.x < target_x:
            self.x += 10
            if self.x > target_x:
                self.x = target_x
        elif self.x > target_x:
            self.x -= 10
            if self.x < target_x:
                self.x = target_x
                
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_SPEED
            self.is_jumping = True
            
    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            
    def move_right(self):
        if self.lane < 2:
            self.lane += 1

# 障碍物类
class Obstacle:
    def __init__(self, lane):
        self.lane = lane
        self.lanes_x = [WIDTH // 4, WIDTH // 2, WIDTH * 3 // 4]
        self.x = self.lanes_x[lane]
        self.y = -50
        self.width = 40
        self.height = 40
        self.type = "obstacle"
        
    def update(self):
        self.y += SCROLL_SPEED
        return self.y > HEIGHT
        
    def collides_with(self, player):
        # 简单的矩形碰撞检测
        return (abs(self.x - player.x) * 2 < (self.width + player.width)) and \
               (abs(self.y - player.y) * 2 < (self.height + player.height))

# 金币类
class Coin:
    def __init__(self, lane):
        self.lane = lane
        self.lanes_x = [WIDTH // 4, WIDTH // 2, WIDTH * 3 // 4]
        self.x = self.lanes_x[lane]
        self.y = -30
        self.width = 30
        self.height = 30
        self.type = "coin"
        
    def update(self):
        self.y += SCROLL_SPEED
        return self.y > HEIGHT
        
    def collides_with(self, player):
        # 简单的矩形碰撞检测
        return (abs(self.x - player.x) * 2 < (self.width + player.width)) and \
               (abs(self.y - player.y) * 2 < (self.height + player.height))

# 道具类
class Item:
    def __init__(self, lane):
        self.lane = lane
        self.lanes_x = [WIDTH // 4, WIDTH // 2, WIDTH * 3 // 4]
        self.x = self.lanes_x[lane]
        self.y = -30
        self.width = 30
        self.height = 30
        self.type = "item"
        self.active = False
        self.timer = 0
        
    def update(self):
        self.y += SCROLL_SPEED
        # 道具激活时更新计时器
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False
        return self.y > HEIGHT
        
    def collides_with(self, player):
        # 简单的矩形碰撞检测
        return (abs(self.x - player.x) * 2 < (self.width + player.width)) and \
               (abs(self.y - player.y) * 2 < (self.height + player.height))

# 排行榜文件路径
LEADERBOARD_FILE = "subway_leaderboard.txt"

# 读取排行榜
def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            lines = f.readlines()
            leaderboard = []
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    leaderboard.append((int(parts[0]), int(parts[1]), int(parts[2])))
            return sorted(leaderboard, key=lambda x: (-x[0], -x[1], x[2]))[:5]  # 按分数、金币数和时间排序，取前5名
    except FileNotFoundError:
        return []

# 保存分数到排行榜
def save_score(score, coins, time):
    try:
        with open(LEADERBOARD_FILE, "a") as f:
            f.write(f"{int(score)},{coins},{time}\n")
    except Exception as e:
        print(f"保存分数时出错: {e}")

# 游戏变量
player = Player()
obstacles = []
coins = []
items = []
score = 0
coins_collected = 0
game_over = False
frame_count = 0
active_item = None  # 当前激活的道具
game_time = 0  # 游戏时间（秒）
show_leaderboard = False  # 是否显示排行榜
leaderboard = []  # 排行榜数据
last_item_score = 0  # 上一个道具生成时的分数

def update():
    global score, game_over, frame_count, coins_collected, active_item, game_time, show_leaderboard, leaderboard, last_item_score
    
    if game_over and not show_leaderboard:
        # 保存分数并加载排行榜
        save_score(score, coins_collected, int(game_time))
        leaderboard = load_leaderboard()
        show_leaderboard = True
        return
        
    if game_over:
        return
        
    # 更新游戏时间
    if frame_count % 60 == 0:  # 每60帧增加1秒
        game_time += 1
        
    # 更新玩家
    player.update()
    
    # 生成障碍物
    if frame_count % OBSTACLE_FREQUENCY == 0:
        lane = random.randint(0, 2)
        obstacles.append(Obstacle(lane))
    
    # 生成金币
    if frame_count % COIN_FREQUENCY == 0:
        lane = random.randint(0, 2)
        coins.append(Coin(lane))
    
    # 生成道具 - 每100分生成一次
    if int(score) // 100 > last_item_score // 100:
        lane = random.randint(0, 2)
        items.append(Item(lane))
        last_item_score = int(score)
    
    # 更新障碍物并检测碰撞
    for obstacle in obstacles[:]:
        if obstacle.update():
            obstacles.remove(obstacle)
            score += 1
        elif obstacle.collides_with(player):
            # 如果有激活的道具，不会game over
            if active_item is None:
                game_over = True
            else:
                obstacles.remove(obstacle)
                score += 1
    
    # 更新金币并检测收集
    for coin in coins[:]:
        if coin.update():
            coins.remove(coin)
        elif coin.collides_with(player):
            coins.remove(coin)
            coins_collected += 1
            score += 5  # 金币加分
    
    # 更新道具并检测收集
    for item in items[:]:
        if item.update():
            items.remove(item)
        elif item.collides_with(player):
            items.remove(item)
            active_item = item
            active_item.active = True
            active_item.timer = ITEM_DURATION  # 道具持续5秒(300帧)
    
    # 更新激活的道具
    if active_item and active_item.active:
        active_item.timer -= 1
        if active_item.timer <= 0:
            active_item.active = False
            active_item = None
    
    # 增加分数
    score += 0.1
    frame_count += 1

def draw():
    global screen

    screen.clear()
    screen.fill((135, 206, 235))  # 天空蓝背景
    
    # 绘制地面
    screen.draw.filled_rect(Rect((0, HEIGHT - 50), (WIDTH, 50)), (34, 139, 34))
    
    # 绘制跑道线
    for i in range(1, 4):
        x = WIDTH * i // 4
        for y in range(0, HEIGHT, 40):
            if (y + frame_count) % 40 < 20:  # 产生移动效果
                screen.draw.line((x, y), (x, y + 20), (255, 255, 255))
    
    # 绘制玩家
    player_color = (0, 100, 255)  # 正常蓝色
    if active_item:  # 如果有激活的道具，显示为绿色
        player_color = (0, 255, 0)
    screen.draw.filled_rect(Rect((player.x - player.width//2, 
                                 player.y - player.height//2), 
                                (player.width, player.height)), 
                           player_color)
    
    # 绘制障碍物
    for obstacle in obstacles:
        screen.draw.filled_rect(Rect((obstacle.x - obstacle.width//2, 
                                     obstacle.y - obstacle.height//2), 
                                    (obstacle.width, obstacle.height)), 
                               (255, 0, 0))  # 红色
    
    # 绘制金币
    for coin in coins:
        screen.draw.filled_rect(Rect((coin.x - coin.width//2, 
                                     coin.y - coin.height//2), 
                                    (coin.width, coin.height)), 
                               (255, 215, 0))  # 金色
    
    # 绘制道具
    for item in items:
        screen.draw.filled_rect(Rect((item.x - item.width//2, 
                                     item.y - item.height//2), 
                                    (item.width, item.height)), 
                               (0, 255, 0))  # 绿色
    
    # 绘制分数、金币数和时间
    screen.draw.text(f"Score: {int(score)}", (10, 10), fontsize=30, color="white")
    screen.draw.text(f"Coins: {coins_collected}", (10, 45), fontsize=30, color="gold")
    screen.draw.text(f"Time: {int(game_time)}s", (10, 80), fontsize=30, color="cyan")
    
    # 显示激活的道具和剩余时间
    if active_item:
        screen.draw.text("POWER-UP!", (WIDTH - 150, 10), fontsize=25, color="lime")
        screen.draw.text(f"Item: {active_item.timer//60}s", (WIDTH - 150, 40), fontsize=25, color="lime")
    
    # 绘制游戏结束画面和排行榜
    if game_over:
        if show_leaderboard:
            # 显示排行榜
            screen.draw.text("GAME OVER", center=(WIDTH//2, 30), fontsize=50, color="red")
            screen.draw.text("Leaderboard:", center=(WIDTH//2, 100), fontsize=40, color="yellow")
            
            # 显示排行榜内容
            for i, (score_entry, coins_entry, time_entry) in enumerate(leaderboard):
                text = f"{i+1}. Score: {score_entry} Coins: {coins_entry} Time: {time_entry}s"
                screen.draw.text(text, center=(WIDTH//2, 150 + i*40), fontsize=25, color="white")
            
            screen.draw.text("Press R to restart", center=(WIDTH//2, HEIGHT - 50), fontsize=30, color="white")
        else:
            screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=50, color="red")
            screen.draw.text("Saving score...", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30, color="white")
    else:
        # 显示操作提示
        screen.draw.text("SPACE=Jump LEFT/RIGHT=Move", center=(WIDTH//2, HEIGHT - 20), fontsize=20, color="white")

def on_key_down(key):
    global game_over, score, obstacles, player, frame_count, coins, items, coins_collected, active_item, game_time, show_leaderboard, last_item_score
    
    if game_over and key == keys.R:
        # 重启游戏
        game_over = False
        score = 0
        coins_collected = 0
        obstacles = []
        coins = []
        items = []
        player = Player()
        frame_count = 0
        active_item = None
        game_time = 0
        show_leaderboard = False
        last_item_score = 0
    elif not game_over:
        if key == keys.SPACE:
            player.jump()
        elif key == keys.LEFT:
            player.move_left()
        elif key == keys.RIGHT:
            player.move_right()

pgzrun.go()