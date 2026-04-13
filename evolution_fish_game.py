import pygame
import random
import sys
import math
import json
import os

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
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
GOLD = (255, 215, 0)

# 创建屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("进化大鱼吃小鱼 - 从鱼到龙")
clock = pygame.time.Clock()

class Fish:
    def __init__(self, x, y, size, color, speed, fish_type="small"):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed
        self.direction = random.uniform(0, 2 * math.pi)
        self.turn_speed = random.uniform(-0.1, 0.1)
        self.eaten = False
        self.fish_type = fish_type  # small, medium, large, shrimp
        self.target_x = None
        self.target_y = None
        
    def update(self, target_x=None, target_y=None):
        # 如果有目标点，则向目标点移动
        if target_x is not None and target_y is not None:
            dx = target_x - self.x
            dy = target_y - self.y
            distance = max(0.1, math.sqrt(dx*dx + dy*dy))
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            self.direction = math.atan2(dy, dx)
        else:
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

class PlayerFish:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 20
        self.color = BLUE
        self.speed = 3
        self.direction = 0
        self.evolution_stage = 0  # 0: 小鱼, 1: 中鱼, 2: 大鱼, 3: 龙
        self.eaten_fish_count = 0
        self.evolution_threshold = 3  # 每吃3条鱼进化一次
        
    def update(self):
        # 玩家控制
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            self.direction = math.pi
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            self.direction = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
            self.direction = 3 * math.pi / 2
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            self.direction = math.pi / 2
            
        # 保持在屏幕内
        self.x = max(self.size, min(WIDTH - self.size, self.x))
        self.y = max(self.size, min(HEIGHT - self.size, self.y))
        
        # 根据进化阶段更新外观
        self.update_appearance()
        
    def update_appearance(self):
        # 根据进化阶段改变颜色和大小
        if self.evolution_stage == 0:  # 小鱼
            self.color = BLUE
        elif self.evolution_stage == 1:  # 中鱼
            self.color = GREEN
            self.size = 30
        elif self.evolution_stage == 2:  # 大鱼
            self.color = GOLD
            self.size = 45
        elif self.evolution_stage == 3:  # 龙
            self.color = PURPLE
            self.size = 60
            
    def draw(self, surface):
        # 绘制身体
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
        
        # 绘制尾巴
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
        
        # 绘制眼睛
        eye_x = self.x + math.cos(self.direction) * self.size * 0.5
        eye_y = self.y + math.sin(self.direction) * self.size * 0.5
        pygame.draw.circle(surface, WHITE, (int(eye_x), int(eye_y)), self.size // 3)
        pygame.draw.circle(surface, BLACK, (int(eye_x), int(eye_y)), self.size // 6)
        
        # 如果是龙形态，添加额外装饰
        if self.evolution_stage == 3:
            # 绘制龙角
            horn1_x = self.x + math.cos(self.direction) * self.size * 0.5
            horn1_y = self.y + math.sin(self.direction) * self.size * 0.5 - self.size * 0.5
            horn2_x = self.x + math.cos(self.direction) * self.size * 0.5
            horn2_y = self.y + math.sin(self.direction) * self.size * 0.5 + self.size * 0.5
            pygame.draw.line(surface, GOLD, (self.x, self.y), (horn1_x, horn1_y), 3)
            pygame.draw.line(surface, GOLD, (self.x, self.y), (horn2_x, horn2_y), 3)
            
    def collides_with(self, other):
        distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return distance < self.size + other.size

def create_fish(fish_type=None):
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
    if fish_type is None:
        fish_type = random.choice(['small', 'shrimp'])
        
    if fish_type == 'small':
        size = random.randint(5, 15)
        speed = random.uniform(1.0, 3.0)
        color = random.choice([RED, GREEN, YELLOW, PINK])
    else:  # shrimp
        size = random.randint(3, 10)
        speed = random.uniform(1.5, 3.5)
        color = CYAN
        
    return Fish(x, y, size, color, speed, fish_type)

def load_scores():
    """加载排行榜数据"""
    try:
        with open('fish_scores.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_scores(scores):
    """保存排行榜数据"""
    with open('fish_scores.json', 'w') as f:
        json.dump(scores, f)

def add_score(scores, time_survived, final_stage):
    """添加新分数到排行榜"""
    scores.append({
        'time': time_survived,
        'stage': final_stage,
        'date': pygame.time.get_ticks()
    })
    # 按时间排序，保留前10名
    scores.sort(key=lambda x: x['time'], reverse=True)
    return scores[:10]

def draw_leaderboard(surface, font, scores):
    """绘制排行榜"""
    title = font.render("排行榜 (生存时间)", True, WHITE)
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    for i, score in enumerate(scores[:5]):  # 显示前5名
        stage_names = ['小鱼', '中鱼', '大鱼', '龙']
        stage_name = stage_names[min(score['stage'], 3)]
        text = font.render(f"{i+1}. {score['time']:.1f}秒 - {stage_name}", True, WHITE)
        surface.blit(text, (WIDTH//2 - text.get_width()//2, 100 + i * 40))

def main():
    # 创建玩家鱼
    player = PlayerFish()
    
    # 创建初始鱼群
    fishes = []
    for _ in range(20):  # 增加初始鱼的数量
        fishes.append(create_fish())
    
    # 跟随玩家的小鱼列表
    following_fish = []
    
    # 游戏变量
    score = 0
    start_time = pygame.time.get_ticks()
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)
    game_over = False
    win = False
    scores = load_scores()
    
    # 游戏主循环
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if (game_over or win) and event.key == pygame.K_r:
                    # 重启游戏
                    main()
                    return
        
        if not game_over and not win:
            current_time = (pygame.time.get_ticks() - start_time) / 1000.0  # 转换为秒
            
            # 更新玩家
            player.update()
            
            # 更新普通鱼群
            for fish in fishes:
                fish.update()
                
            # 更新跟随玩家的鱼
            for i, fish in enumerate(following_fish):
                # 让跟随的鱼排成一列跟在玩家后面
                if i == 0:
                    target_x, target_y = player.x - math.cos(player.direction) * (player.size + 20), \
                                        player.y - math.sin(player.direction) * (player.size + 20)
                else:
                    target_x, target_y = following_fish[i-1].x - math.cos(following_fish[i-1].direction) * 20, \
                                        following_fish[i-1].y - math.sin(following_fish[i-1].direction) * 20
                fish.update(target_x, target_y)
                
            # 检查玩家是否吃掉小鱼或小虾
            for fish in fishes[:]:
                if player.collides_with(fish) and not fish.eaten:
                    if player.size > fish.size:
                        # 玩家吃掉鱼
                        fish.eaten = True
                        fishes.remove(fish)
                        player.eaten_fish_count += 1
                        score += fish.size
                        
                        # 被吃掉的鱼加入跟随列表
                        if len(following_fish) < 10:  # 最多跟随10条鱼
                            fish.speed = player.speed * 0.8
                            following_fish.append(fish)
                        
                        # 检查是否达到进化阈值
                        if player.eaten_fish_count >= player.evolution_threshold:
                            player.evolution_stage += 1
                            player.eaten_fish_count = 0
                            player.evolution_threshold += 1  # 下一次需要吃更多的鱼才能进化
                            
                            # 如果进化到龙形态，游戏胜利
                            if player.evolution_stage >= 3:
                                win = True
            
            # 检查跟随鱼是否被吃掉
            for fish in following_fish[:]:
                if player.collides_with(fish) and not fish.eaten:
                    # 玩家吃掉跟随的鱼（为了进化）
                    fish.eaten = True
                    following_fish.remove(fish)
                    player.eaten_fish_count += 1
                    score += fish.size * 2  # 跟随的鱼分数更高
                    
                    # 检查是否达到进化阈值
                    if player.eaten_fish_count >= player.evolution_threshold:
                        player.evolution_stage += 1
                        player.eaten_fish_count = 0
                        player.evolution_threshold += 1
                        
                        # 如果进化到龙形态，游戏胜利
                        if player.evolution_stage >= 3:
                            win = True
            
            # 随机添加新鱼
            if random.random() < 0.05:  # 增加生成频率
                fishes.append(create_fish())
                
            # 保持鱼群数量
            if len(fishes) < 20:
                fishes.append(create_fish())
                
            # 检查玩家是否被更大的鱼吃掉（在龙形态之前）
            if player.evolution_stage < 3:
                for fish in fishes:
                    if fish.size > player.size and fish.collides_with(player):
                        game_over = True
        
        # 绘制游戏
        screen.fill(BLACK)
        
        if not game_over and not win:
            # 绘制所有鱼
            for fish in fishes:
                fish.draw(screen)
                
            # 绘制跟随的鱼
            for fish in following_fish:
                fish.draw(screen)
                
            player.draw(screen)
            
            # 绘制UI信息
            time_text = font.render(f"时间: {((pygame.time.get_ticks() - start_time) / 1000):.1f}秒", True, WHITE)
            score_text = font.render(f"分数: {score}", True, WHITE)
            stage_names = ['小鱼', '中鱼', '大鱼', '龙']
            stage_text = font.render(f"阶段: {stage_names[player.evolution_stage]}", True, WHITE)
            eat_text = font.render(f"吃掉: {player.eaten_fish_count}/{player.evolution_threshold}", True, WHITE)
            
            screen.blit(time_text, (10, 10))
            screen.blit(score_text, (10, 50))
            screen.blit(stage_text, (10, 90))
            screen.blit(eat_text, (10, 130))
        else:
            # 游戏结束或胜利画面
            if win:
                win_text = font.render("恭喜！你进化成了龙！", True, GOLD)
                screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 100))
                
                # 保存分数
                scores = add_score(scores, (pygame.time.get_ticks() - start_time) / 1000.0, player.evolution_stage)
                save_scores(scores)
            else:
                game_over_text = font.render("游戏结束", True, RED)
                screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
            
            restart_text = font.render("按 R 重新开始", True, WHITE)
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 - 50))
            
            # 显示排行榜
            draw_leaderboard(screen, font, scores)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()