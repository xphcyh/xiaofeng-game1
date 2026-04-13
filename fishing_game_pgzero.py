# 导入pgzero模块
import pgzrun
import random

# 游戏配置
WIDTH = 800
HEIGHT = 600

# 游戏对象
player = None
fishes = []
score = 0
game_over = False

# 颜色定义
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 初始化游戏
def init_game():
    global player, fishes, score, game_over
    
    # 创建玩家鱼（使用纯色圆表示）
    player = Actor('circle')
    player.center = (WIDTH//2, HEIGHT//2)
    player.size = 30
    player.speed = 5
    player.color = BLUE

    # 创建初始鱼群
    fishes = []
    for i in range(10):
        fish = Actor('circle')
        fish.center = (random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50))
        fish.size = random.randint(10, 50)
        fish.speed_x = random.randint(-3, 3)
        fish.speed_y = random.randint(-3, 3)
        fish.color = random.choice([RED, GREEN, YELLOW, PURPLE])
        fishes.append(fish)

    # 重置游戏变量
    score = 0
    game_over = False

# 初始化游戏
init_game()

def update():
    global score, game_over
    
    if not game_over:
        # 玩家控制
        if keyboard.left or keyboard.a:
            player.x -= player.speed
        if keyboard.right or keyboard.d:
            player.x += player.speed
        if keyboard.up or keyboard.w:
            player.y -= player.speed
        if keyboard.down or keyboard.s:
            player.y += player.speed
            
        # 保持玩家在屏幕内
        player.x = max(player.size, min(WIDTH - player.size, player.x))
        player.y = max(player.size, min(HEIGHT - player.size, player.y))
        
        # 更新鱼群
        for fish in fishes:
            # 鱼的移动
            fish.x += fish.speed_x
            fish.y += fish.speed_y
            
            # 边界反弹
            if fish.x < fish.size or fish.x > WIDTH - fish.size:
                fish.speed_x = -fish.speed_x
            if fish.y < fish.size or fish.y > HEIGHT - fish.size:
                fish.speed_y = -fish.speed_y
                
        # 检查碰撞
        for fish in fishes[:]:
            # 计算距离
            dx = player.x - fish.x
            dy = player.y - fish.y
            distance = (dx**2 + dy**2)**0.5
            
            if distance < player.size + fish.size:
                if player.size > fish.size:
                    # 玩家吃掉鱼
                    fishes.remove(fish)
                    player.size += 1
                    score += fish.size
                    
                    # 创建新鱼
                    new_fish = Actor('circle')
                    side = random.choice(['left', 'right', 'top', 'bottom'])
                    if side == 'left':
                        new_fish.center = (-20, random.randint(0, HEIGHT))
                        new_fish.speed_x = random.randint(1, 3)
                    elif side == 'right':
                        new_fish.center = (WIDTH + 20, random.randint(0, HEIGHT))
                        new_fish.speed_x = random.randint(-3, -1)
                    elif side == 'top':
                        new_fish.center = (random.randint(0, WIDTH), -20)
                        new_fish.speed_y = random.randint(1, 3)
                    else:  # bottom
                        new_fish.center = (random.randint(0, WIDTH), HEIGHT + 20)
                        new_fish.speed_y = random.randint(-3, -1)
                        
                    new_fish.speed_x = random.randint(-3, 3)
                    new_fish.speed_y = random.randint(-3, 3)
                    new_fish.size = random.randint(10, 50)
                    new_fish.color = random.choice([RED, GREEN, YELLOW, PURPLE])
                    fishes.append(new_fish)
                elif fish.size > player.size:
                    # 玩家被吃掉
                    game_over = True

def draw():
    # 绘制背景
    screen.fill((0, 100, 200))  # 蓝色海水背景
    
    if not game_over:
        # 绘制所有鱼
        for fish in fishes:
            screen.draw.filled_circle((fish.x, fish.y), fish.size, fish.color)
        screen.draw.filled_circle((player.x, player.y), player.size, player.color)
        
        # 绘制分数
        screen.draw.text(f"Score: {score}", (10, 10), color=WHITE, fontsize=36)
        screen.draw.text(f"Size: {player.size}", (10, 50), color=WHITE, fontsize=36)
    else:
        # 绘制所有鱼
        for fish in fishes:
            screen.draw.filled_circle((fish.x, fish.y), fish.size, fish.color)
        screen.draw.filled_circle((player.x, player.y), player.size, player.color)
        
        # 绘制分数
        screen.draw.text(f"Score: {score}", (10, 10), color=WHITE, fontsize=36)
        screen.draw.text(f"Size: {player.size}", (10, 50), color=WHITE, fontsize=36)
        
        # 绘制游戏结束画面
        screen.draw.text("GAME OVER", (WIDTH//2 - 100, HEIGHT//2 - 30), color=RED, fontsize=48)
        screen.draw.text("Press R to restart", (WIDTH//2 - 120, HEIGHT//2 + 20), color=WHITE, fontsize=36)

def on_key_down(key):
    global score, game_over
    
    if game_over and key == keys.R:
        # 重启游戏
        init_game()

pgzrun.go()