import pygame
import random
import sys
import math

# 初始化Pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# 创建屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("大鱼吃小鱼 - 三合一合成版")
clock = pygame.time.Clock()

class Fish:
    def __init__(self, x, y, size, color, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.direction = random.uniform(0, 2 * math.pi)
        self.turn_speed = random.uniform(-0.1, 0.1)
        self.eaten = False  # 标记是否被吃掉
        
    def update(self):
        # 随机改变方向
        self.direction += self.turn_speed
        if random.random() < 0.02:
            self.turn_speed = random.uniform(-0.1, 0.1)
            
        # 更新位置
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        
        # 边界检测和反弹
        if self.x < 0 or self.x > WIDTH:
            self.direction = math.pi - self.direction
        if self.y < 0 or self.y > HEIGHT:
            self.direction = -self.direction
            
        # 保持在屏幕内
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))
        
    def draw(self, surface):
        # 绘制鱼的身体
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
        
        # 绘制鱼尾巴
        tail_x = self.x - math.cos(self.direction) * self.size * 1.5
        tail_y = self.y - math.sin(self.direction) * self.size * 1.5
        tail_points = [
            (tail_x, tail_y),
            (tail_x - math.cos(self.direction + 0.5) * self.size, 
             tail_y - math.sin(self.direction + 0.5) * self.size),
            (tail_x - math.cos(self.direction - 0.5) * self.size, 
             tail_y - math.sin(self.direction - 0.5) * self.size)
        ]
        pygame.draw.polygon(surface, self.color, tail_points)
        
        # 绘制鱼眼睛
        eye_x = self.x + math.cos(self.direction) * self.size * 0.5
        eye_y = self.y + math.sin(self.direction) * self.size * 0.5
        pygame.draw.circle(surface, WHITE, (int(eye_x), int(eye_y)), self.size // 3)
        pygame.draw.circle(surface, BLACK, (int(eye_x), int(eye_y)), self.size // 6)
        
    def collides_with(self, other):
        distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return distance < self.size + other.size

class PlayerFish(Fish):
    def __init__(self):
        super().__init__(WIDTH // 2, HEIGHT // 2, 20, BLUE, 3)
        
    def update(self):
        # 玩家控制
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            
        # 保持在屏幕内
        self.x = max(self.size, min(WIDTH - self.size, self.x))
        self.y = max(self.size, min(HEIGHT - self.size, self.y))

def create_fish(size=None):
    # 在屏幕边缘随机生成鱼
    side = random.choice(['top', 'right', 'bottom', 'left'])
    if side == 'top':
        x = random.randint(0, WIDTH)
        y = -20
    elif side == 'right':
        x = WIDTH + 20
        y = random.randint(0, HEIGHT)
    elif side == 'bottom':
        x = random.randint(0, WIDTH)
        y = HEIGHT + 20
    else:  # left
        x = -20
        y = random.randint(0, HEIGHT)
        
    # 随机大小和颜色
    if size is None:
        size = random.randint(5, 35)
    colors = [RED, GREEN, YELLOW, PURPLE, ORANGE]
    color = random.choice(colors)
    speed = random.uniform(0.5, 2.5)
    
    return Fish(x, y, size, color, speed)

def find_fish_group(fishes, target_size):
    """
    查找三个相同大小的鱼
    """
    same_size_fish = [fish for fish in fishes if fish.size == target_size and not fish.eaten]
    if len(same_size_fish) >= 3:
        return same_size_fish[:3]  # 返回前三个
    return None

def main():
    # 创建玩家鱼
    player = PlayerFish()
    
    # 创建初始鱼群
    fishes = []
    for _ in range(15):
        fishes.append(create_fish())
    
    # 游戏变量
    score = 0
    font = pygame.font.SysFont(None, 36)
    game_over = False
    eaten_fish = []  # 已被吃掉但还未移除的鱼
    
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
                    main()
                    return
        
        if not game_over:
            # 更新玩家
            player.update()
            
            # 更新鱼群
            for fish in fishes:
                fish.update()
                
            # 检查玩家是否吃掉小鱼
            for fish in fishes[:]:
                if player.collides_with(fish) and not fish.eaten:
                    if player.size > fish.size:
                        # 玩家吃掉鱼
                        fish.eaten = True
                        eaten_fish.append(fish)
                        player.size += 1
                        score += fish.size
                        
                        # 检查是否可以合成
                        group = find_fish_group(eaten_fish, fish.size)
                        if group:
                            # 合成更大的鱼
                            for f in group:
                                if f in eaten_fish:
                                    eaten_fish.remove(f)
                                if f in fishes:
                                    fishes.remove(f)
                            
                            # 创建一个更大的鱼
                            new_size = int(fish.size * 1.5)
                            new_fish = create_fish(new_size)
                            fishes.append(new_fish)
                    elif fish.size > player.size:
                        # 玩家被吃掉
                        game_over = True
            
            # 移除被吃掉的鱼
            for fish in eaten_fish[:]:
                if fish in fishes:
                    fishes.remove(fish)
            
            # 随机添加新鱼
            if random.random() < 0.03:
                fishes.append(create_fish())
                
            # 保持鱼群数量
            if len(fishes) < 15:
                fishes.append(create_fish())
        
        # 绘制游戏
        screen.fill(BLACK)
        
        # 绘制所有鱼
        for fish in fishes:
            fish.draw(screen)
        player.draw(screen)
        
        # 绘制分数
        score_text = font.render(f"Score: {score}", True, WHITE)
        size_text = font.render(f"Size: {player.size}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(size_text, (10, 50))
        
        # 绘制游戏结束画面
        if game_over:
            game_over_text = font.render("GAME OVER", True, RED)
            restart_text = font.render("Press R to restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 30))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()