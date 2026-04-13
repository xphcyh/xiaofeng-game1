import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.8
JUMP_SPEED = -15
SCROLL_SPEED = 5
OBSTACLE_FREQUENCY = 60  # 每60帧生成一次障碍物
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)

# 创建屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Subway Surfers")
clock = pygame.time.Clock()

# 玩家类
class Player:
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 150
        self.velocity_y = 0
        self.is_jumping = False
        self.lane = 1  # 0=左, 1=中, 2=右
        self.lanes_x = [WIDTH // 4 - self.width // 2, WIDTH // 2 - self.width // 2, WIDTH * 3 // 4 - self.width // 2]
        self.x = self.lanes_x[self.lane]
        
    def update(self):
        # 更新垂直速度
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        
        # 地面碰撞检测
        if self.y > HEIGHT - 150:
            self.y = HEIGHT - 150
            self.velocity_y = 0
            self.is_jumping = False
            
        # 更新水平位置
        target_x = self.lanes_x[self.lane]
        if self.x < target_x:
            self.x += 15
            if self.x > target_x:
                self.x = target_x
        elif self.x > target_x:
            self.x -= 15
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
            
    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height))
        # 绘制玩家的头部
        pygame.draw.circle(surface, BLUE, (self.x + self.width // 2, self.y - 10), 15)

# 障碍物类
class Obstacle:
    def __init__(self, lane):
        self.width = 40
        self.height = 40
        self.lane = lane
        self.lanes_x = [WIDTH // 4 - self.width // 2, WIDTH // 2 - self.width // 2, WIDTH * 3 // 4 - self.width // 2]
        self.x = self.lanes_x[lane]
        self.y = -self.height
        
    def update(self):
        self.y += SCROLL_SPEED
        return self.y > HEIGHT
        
    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))
        
    def collides_with(self, player):
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        obstacle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(obstacle_rect)

# 游戏变量
player = Player()
obstacles = []
score = 0
game_over = False
frame_count = 0
font = pygame.font.SysFont(None, 36)

# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                # 重启游戏
                game_over = False
                score = 0
                obstacles = []
                player = Player()
                frame_count = 0
            elif not game_over:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()
    
    if not game_over:
        # 更新玩家
        player.update()
        
        # 生成障碍物
        frame_count += 1
        if frame_count >= OBSTACLE_FREQUENCY:
            frame_count = 0
            lane = random.randint(0, 2)
            obstacles.append(Obstacle(lane))
        
        # 更新障碍物并检测碰撞
        for obstacle in obstacles[:]:
            if obstacle.update():
                obstacles.remove(obstacle)
                score += 1
            elif obstacle.collides_with(player):
                game_over = True
        
        # 增加分数
        score += 0.1
    
    # 绘制游戏
    screen.fill(SKY_BLUE)  # 天空蓝背景
    
    # 绘制地面
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - 50, WIDTH, 50))
    
    # 绘制跑道线
    for i in range(1, 4):
        x = WIDTH * i // 4
        for y in range(0, HEIGHT, 40):
            if (y + frame_count * 2) % 40 < 20:  # 产生移动效果
                pygame.draw.line(screen, WHITE, (x, y), (x, y + 20), 3)
    
    # 绘制玩家
    player.draw(screen)
    
    # 绘制障碍物
    for obstacle in obstacles:
        obstacle.draw(screen)
    
    # 绘制分数
    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # 绘制游戏结束画面
    if game_over:
        game_over_text = font.render("GAME OVER", True, RED)
        restart_text = font.render("Press R to restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 30))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()