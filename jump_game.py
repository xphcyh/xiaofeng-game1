import pygame
import random
import sys
import math

# 设置编码
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 初始化Pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# 创建屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("跳一跳")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT - 150
        self.radius = 20
        self.velocity_y = 0
        self.velocity_x = 0  # 添加水平速度
        self.is_jumping = False
        self.jump_power = -22  # 增加跳跃力度
        self.gravity = 0.8
        self.color = BLUE
        self.trail = []  # 跳跃轨迹
        
    def update(self):
        # 应用重力
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        self.x += self.velocity_x  # 更新水平位置
        
        # 地面摩擦力
        self.velocity_x *= 0.8
        if abs(self.velocity_x) < 0.1:
            self.velocity_x = 0
            
        # 地面碰撞检测
        if self.y > HEIGHT - 150:
            self.y = HEIGHT - 150
            self.velocity_y = 0
            self.is_jumping = False
            
        # 更新轨迹（最多保存10个点）
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
            
    def jump(self, power_ratio):
        if not self.is_jumping:
            # 根据力度计算跳跃速度
            self.velocity_y = self.jump_power * (0.5 + power_ratio * 0.5)
            # 添加水平速度使角色能够跳跃到其他平台，增加跳跃距离
            self.velocity_x = 12 * power_ratio  # 增加水平速度
            self.is_jumping = True
            
    def draw(self, surface):
        # 绘制轨迹
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = i / len(self.trail)
            radius = int(self.radius * alpha)
            if radius > 0:
                # 创建带透明度的颜色
                trail_color = (self.color[0], self.color[1], self.color[2])
                pygame.draw.circle(surface, trail_color, (int(trail_x), int(trail_y)), radius)
        
        # 绘制玩家
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # 绘制眼睛
        pygame.draw.circle(surface, WHITE, (int(self.x + 5), int(self.y - 5)), 5)
        pygame.draw.circle(surface, BLACK, (int(self.x + 6), int(self.y - 5)), 2)

class Platform:
    def __init__(self, x, y, width, height, color=GREEN):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.perfect_zone = width // 3  # 中间区域为完美着陆区
        
    def draw(self, surface):
        # 绘制平台
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        # 绘制边框
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2)
        
        # 绘制完美着陆区（中间区域）
        perfect_x = self.x + (self.width - self.perfect_zone) // 2
        pygame.draw.rect(surface, YELLOW, (perfect_x, self.y, self.perfect_zone, self.height), 2)
        
    def check_landing(self, player):
        # 检查玩家是否着陆在平台上
        if (player.y + player.radius >= self.y and 
            player.y + player.radius <= self.y + 10 and
            player.x >= self.x and 
            player.x <= self.x + self.width and
            player.velocity_y > 0):
            
            # 检查是否在完美着陆区
            perfect_x = self.x + (self.width - self.perfect_zone) // 2
            if player.x >= perfect_x and player.x <= perfect_x + self.perfect_zone:
                return "perfect"
            else:
                return "normal"
        return None

class PowerBar:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.width = 200
        self.height = 20
        self.power = 0
        self.max_power = 100
        self.increasing = True
        
    def update(self):
        if self.increasing:
            self.power += 2
            if self.power >= self.max_power:
                self.increasing = False
        else:
            self.power -= 2
            if self.power <= 0:
                self.increasing = True
                
    def draw(self, surface):
        # 绘制背景
        pygame.draw.rect(surface, GRAY, (self.x, self.y, self.width, self.height))
        # 绘制能量条
        power_width = int(self.width * self.power / self.max_power)
        color = GREEN if self.power < 70 else YELLOW if self.power < 90 else RED
        pygame.draw.rect(surface, color, (self.x, self.y, power_width, self.height))
        # 绘制边框
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2)
        
    def get_power_ratio(self):
        return self.power / self.max_power

def generate_platforms():
    platforms = []
    # 第一个平台（起始平台）
    platforms.append(Platform(50, HEIGHT - 150, 100, 20, GREEN))
    
    # 生成随机平台，减小平台间距离使游戏更容易
    for i in range(1, 20):
        prev_platform = platforms[-1]
        # 平台之间的水平距离（减小距离）
        gap = random.randint(60, 150)  # 减小了最大距离
        platform_width = random.randint(70, 130)  # 增加最小宽度
        x = prev_platform.x + prev_platform.width + gap
        y = HEIGHT - 150 - random.randint(0, 80)  # 减小垂直高度差
        platforms.append(Platform(x, y, platform_width, 20))
        
    return platforms

def main():
    # 创建游戏对象
    player = Player()
    platforms = generate_platforms()
    power_bar = PowerBar()
    
    # 游戏变量
    score = 0
    perfect_lands = 0
    game_over = False
    camera_x = 0
    font = pygame.font.SysFont("simhei", 36)  # 使用黑体字体
    small_font = pygame.font.SysFont("simhei", 24)  # 使用黑体字体
    charging_jump = False  # 是否正在蓄力跳跃
    
    # 游戏主循环
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player.is_jumping and not game_over:
                    # 开始蓄力跳跃
                    charging_jump = True
                    power_bar.power = 0
                    power_bar.increasing = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and charging_jump and not game_over:
                    # 释放空格键，执行跳跃
                    charging_jump = False
                    power = power_bar.get_power_ratio()
                    player.jump(power)
                    
                elif game_over and event.key == pygame.K_r:
                    # 重启游戏
                    main()
                    return
        
        if not game_over:
            # 更新游戏对象
            player.update()
            if charging_jump:
                power_bar.update()
            
            # 检查着陆
            landed = False
            current_platform = None
            for platform in platforms:
                landing_result = platform.check_landing(player)
                if landing_result:
                    landed = True
                    current_platform = platform
                    if landing_result == "perfect":
                        score += 20
                        perfect_lands += 1
                    else:
                        score += 10
                    player.y = platform.y - player.radius
                    player.velocity_y = 0
                    player.is_jumping = False
                    # 停止水平移动
                    player.velocity_x = 0
                    break
            
            # 如果没有着陆且玩家掉落到屏幕底部，则游戏结束
            if player.y >= HEIGHT - 50:
                game_over = True
                
            # 更新摄像机位置（跟随玩家）
            if player.x > WIDTH // 2:
                camera_x = player.x - WIDTH // 2
                
            # 检查是否到达终点
            last_platform = platforms[-1]
            if player.x > last_platform.x + last_platform.width:
                score += 100  # 到达终点奖励
                game_over = True
                
        # 绘制游戏
        screen.fill(WHITE)
        
        # 绘制平台（考虑摄像机偏移）
        for platform in platforms:
            platform_screen_x = platform.x - camera_x
            if platform_screen_x > -platform.width and platform_screen_x < WIDTH:
                platform_copy = Platform(platform_screen_x, platform.y, platform.width, platform.height, platform.color)
                platform_copy.perfect_zone = platform.perfect_zone
                platform_copy.draw(screen)
        
        # 绘制玩家（考虑摄像机偏移）
        player_screen_x = player.x - camera_x
        player_copy = Player()
        player_copy.x = player_screen_x
        player_copy.y = player.y
        player_copy.radius = player.radius
        player_copy.trail = [(x - camera_x, y) for x, y in player.trail]
        player_copy.draw(screen)
        
        # 绘制UI
        power_bar.draw(screen)
        score_text = font.render(f"分数: {score}", True, BLACK)
        screen.blit(score_text, (WIDTH - 150, 10))
        
        perfect_text = small_font.render(f"完美着陆: {perfect_lands}", True, BLACK)
        screen.blit(perfect_text, (WIDTH - 150, 50))
        
        # 绘制操作提示
        if not player.is_jumping and not game_over:
            if charging_jump:
                hint_text = small_font.render("蓄力中... 松开空格键跳跃", True, BLACK)
            else:
                hint_text = small_font.render("按住空格键蓄力跳跃", True, BLACK)
            screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT - 100))
            
        # 绘制游戏结束画面
        if game_over:
            if player.y >= HEIGHT - 50:
                game_over_text = font.render("游戏结束 - 掉落!", True, RED)
            else:
                game_over_text = font.render("恭喜通关!", True, GREEN)
                
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            
            final_score_text = font.render(f"最终分数: {score}", True, BLACK)
            screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))
            
            restart_text = font.render("按 R 重新开始", True, BLACK)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()