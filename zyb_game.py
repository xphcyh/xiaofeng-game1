"""
最终幸存者 - 类似微信小游戏"咸鱼之王-最终幸存者"
一个生存类roguelike游戏，玩家需要在不断涌来的敌人中生存下来

游戏玩法：
- 角色自动攻击附近的敌人
- 击败敌人获得经验值并升级
- 升级时随机选择技能强化
- 尽可能长时间生存！

控制方式：
- WASD 或 方向键：移动角色
- ESC：暂停/继续游戏
"""

import pygame
import random
import math
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_BLUE = (173, 216, 230)
GOLD = (255, 215, 0)
CYAN = (0, 255, 255)


def get_chinese_font(size):
    """获取中文字体
    尝试在不同操作系统上查找合适的中文字体文件，以确保游戏中能正确显示中文字符
    参数:
        size: 字体大小
    返回:
        pygame.font.Font对象，如果找不到合适的中文字体则返回默认字体
    """
    # 尝试加载系统中文字体，按优先级列出不同操作系统的常见中文字体路径
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",  # Windows系统黑体
        "C:/Windows/Fonts/msyh.ttc",     # Windows系统微软雅黑
        "C:/Windows/Fonts/simsun.ttc",   # Windows系统宋体
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # Linux系统文泉驿字体
        "/System/Library/Fonts/PingFang.ttc",  # macOS系统苹方字体
    ]

    for font_path in font_paths:  # 遍历字体路径列表，尝试加载每一个字体
        try:
            return pygame.font.Font(font_path, size)  # 尝试加载字体文件，如果成功则立即返回
        except:  # 如果当前字体加载失败，继续尝试下一个路径
            continue

    # 如果所有预设路径都失败，返回默认字体作为备选方案
    return pygame.font.Font(None, size)  # 使用pygame的默认字体，确保游戏能正常运行


class Player:
    """玩家角色类"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.speed = 1.5  # 初始移速和敌人一样
        self.max_health = 100
        self.health = 100
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100
        
        # 属性
        self.damage = 10
        self.attack_speed = 1.0  # 每秒攻击次数
        self.attack_range = 100
        self.projectile_speed = 5
        self.projectile_count = 1
        self.piercing = 0  # 穿透次数
        
        # 攻击计时器
        self.last_attack_time = 0
        
        # 特殊能力
        self.has_orbiting_shield = False
        self.shield_count = 0
        self.shield_damage = 5
        self.shield_rotation_speed = 2
        
        self.has_lightning = False
        self.lightning_damage = 15
        self.lightning_interval = 2000  # 毫秒
        
        self.has_explosion = False
        self.explosion_damage = 20
        self.explosion_radius = 80
        self.explosion_interval = 3000
        
        self.health_regen = 0  # 每秒恢复生命值
        
    def move(self, keys):
        """移动玩家"""
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
            
        # 边界检测
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))
    
    def take_damage(self, damage):
        """受到伤害"""
        self.health -= damage
        return self.health <= 0
    
    def gain_exp(self, amount):
        """获得经验值"""
        self.exp += amount
        if self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level_up()
            return True
        return False
    
    def level_up(self):
        """升级"""
        # 保持当前血量比例
        health_ratio = self.health / self.max_health if self.max_health > 0 else 1
        
        self.level += 1
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        self.max_health += 10
        # 按照比例恢复血量,而不是直接回满
        self.health = int(self.max_health * health_ratio)
    
    def heal(self, amount):
        """治疗"""
        self.health = min(self.max_health, self.health + amount)
    
    def draw(self, screen):
        """绘制玩家"""
        # 绘制角色
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)
        
        # 绘制血条
        bar_width = 40
        bar_height = 6
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.radius - 15
        
        # 背景
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # 当前血量
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
        
        # 绘制等级和血量数值
        font = get_chinese_font(20)
        level_text = font.render(f"Lv.{self.level} {self.health}/{self.max_health}", True, GOLD)
        text_rect = level_text.get_rect(centerx=self.x, top=self.y - self.radius - 35)
        screen.blit(level_text, text_rect)


class Enemy:
    """敌人类"""
    
    def __init__(self, x, y, enemy_type="basic", level=1):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.level = level  # 敌人等级
        self.last_attack_time = 0  # 上次攻击时间
        self.attack_cooldown = 1000  # 攻击冷却时间1秒
        self.has_attacked_on_contact = False  # 是否在接触时已攻击过
        
        # 根据类型设置基础属性
        if enemy_type == "basic":
            self.radius = 12
            self.speed = 1.5
            base_health = 20
            base_damage = 2
            self.exp_value = 10
            self.base_color = RED
        elif enemy_type == "fast":
            self.radius = 10
            self.speed = 3
            base_health = 15
            base_damage = 1
            self.exp_value = 15
            self.base_color = ORANGE
        elif enemy_type == "tank":
            self.radius = 18
            self.speed = 0.8
            base_health = 60
            base_damage = 4
            self.exp_value = 25
            self.base_color = PURPLE
        elif enemy_type == "boss":
            self.radius = 30
            self.speed = 1
            base_health = 200
            base_damage = 8
            self.exp_value = 100
            self.base_color = GOLD
        else:
            self.radius = 12
            self.speed = 1.5
            base_health = 20
            base_damage = 2
            self.exp_value = 10
            self.base_color = RED
        
        # 根据等级调整属性
        self.max_health = int(base_health * (1 + (level - 1) * 0.3))  # 每级增加30%血量
        self.health = self.max_health
        self.damage = int(base_damage * (1 + (level - 1) * 0.2))  # 每级增加20%伤害
        
        # 根据等级设置颜色
        self.color = self.get_level_color()
    
    def get_level_color(self):
        """根据等级获取颜色"""
        if self.level == 1:
            return self.base_color
        elif self.level <= 5:
            # 1-5级逐渐变亮
            brightness = min(255, 30 * (self.level - 1))
            return tuple(min(255, c + brightness) for c in self.base_color)
        elif self.level <= 10:
            # 6-10级带金色效果
            intensity = (self.level - 5) / 5.0
            r = int(self.base_color[0] * (1 - intensity) + GOLD[0] * intensity)
            g = int(self.base_color[1] * (1 - intensity) + GOLD[1] * intensity)
            b = int(self.base_color[2] * (1 - intensity) + GOLD[2] * intensity)
            return (r, g, b)
        else:
            # 10级以上高等级敌人带紫色边框效果
            purple_intensity = min(1.0, (self.level - 10) / 10.0)
            r = int(GOLD[0] * (1 - purple_intensity) + PURPLE[0] * purple_intensity)
            g = int(GOLD[1] * (1 - purple_intensity) + PURPLE[1] * purple_intensity)
            b = int(GOLD[2] * (1 - purple_intensity) + PURPLE[2] * purple_intensity)
            return (r, g, b)
    
    def upgrade(self):
        """升级敌人"""
        # 保存旧的最大血量，用于显示提升效果
        old_max_health = self.max_health
        
        self.level += 1
        # 血量提升：每级增加30%
        self.max_health = int(self.max_health * 1.3)
        self.health = self.max_health  # 升级时回满血
        # 攻击力提升：每级增加20%
        self.damage = int(self.damage * 1.2)
        # 经验值提升：每级增加25%，让玩家获得更多奖励
        self.exp_value = int(self.exp_value * 1.25)
        # 更新颜色
        self.color = self.get_level_color()
        
        # 返回升级信息，用于显示
        return {
            'old_max_health': old_max_health,
            'new_max_health': self.max_health,
            'health_increase': self.max_health - old_max_health
        }
    
    def move_towards(self, target_x, target_y):
        """向目标移动"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
    
    def take_damage(self, damage):
        """受到伤害"""
        self.health -= damage
        return self.health <= 0
    
    def draw(self, screen):
        """绘制敌人"""
        # 高等级敌人添加光环效果
        if self.level >= 3:
            glow_radius = self.radius + 5
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*self.color[:3], 80), (glow_radius, glow_radius), glow_radius, 3)
            screen.blit(glow_surface, (int(self.x) - glow_radius, int(self.y) - glow_radius))
        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)
        
        # 绘制血条
        bar_width = self.radius * 2
        bar_height = 4
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.radius - 12
        
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
        
        # 绘制等级和血量数值
        font = get_chinese_font(16)
        level_text = font.render(f"Lv{self.level} {self.health}/{self.max_health}", True, WHITE)
        text_rect = level_text.get_rect(centerx=self.x, top=self.y - self.radius - 28)
        screen.blit(level_text, text_rect)


class Projectile:
    """投射物类"""
    
    def __init__(self, x, y, target_x, target_y, damage, speed, piercing=0):
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = speed
        self.piercing = piercing
        self.hit_enemies = set()
        self.radius = 5
        
        # 计算方向
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.vx = (dx / distance) * speed
            self.vy = (dy / distance) * speed
        else:
            self.vx = 0
            self.vy = 0
    
    def update(self):
        """更新位置"""
        self.x += self.vx
        self.y += self.vy
    
    def is_off_screen(self):
        """检查是否离开屏幕"""
        return (self.x < 0 or self.x > SCREEN_WIDTH or 
                self.y < 0 or self.y > SCREEN_HEIGHT)
    
    def draw(self, screen):
        """绘制投射物"""
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius, 2)


class ExperienceGem:
    """经验宝石类"""
    
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.radius = 6
        self.magnet_range = 100
        self.speed = 4
    
    def update(self, player_x, player_y):
        """更新位置（被玩家吸引）"""
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < self.magnet_range and distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        
        return distance < self.radius + 15  # 被玩家收集
    
    def draw(self, screen):
        """绘制经验宝石"""
        color = GREEN if self.value < 20 else GOLD
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 1)


class VisualEffect:
    """视觉特效类"""
    
    def __init__(self, x, y, effect_type, **kwargs):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.start_time = pygame.time.get_ticks()
        self.lifetime = kwargs.get('lifetime', 500)  # 默认500ms
        self.size = kwargs.get('size', 50)
        self.color = kwargs.get('color', YELLOW)
        self.max_alpha = kwargs.get('max_alpha', 255)
        
        # 闪电特效属性
        if effect_type == 'lightning':
            self.target_x = kwargs.get('target_x', x)
            self.target_y = kwargs.get('target_y', y)
            self.bolts = self.generate_lightning_bolts()
        
        # 爆炸特效属性
        elif effect_type == 'explosion':
            self.particles = []
            for _ in range(20):
                angle = random.uniform(0, 360)
                speed = random.uniform(2, 6)
                self.particles.append({
                    'vx': math.cos(math.radians(angle)) * speed,
                    'vy': math.sin(math.radians(angle)) * speed,
                    'x': x,
                    'y': y,
                    'size': random.randint(3, 8)
                })
    
    def generate_lightning_bolts(self):
        """生成闪电路径"""
        bolts = []
        num_segments = 8
        dx = (self.target_x - self.x) / num_segments
        dy = (self.target_y - self.y) / num_segments
        
        current_x, current_y = self.x, self.y
        for i in range(num_segments):
            next_x = current_x + dx + random.uniform(-20, 20)
            next_y = current_y + dy + random.uniform(-20, 20)
            bolts.append((current_x, current_y, next_x, next_y))
            current_x, current_y = next_x, next_y
        
        return bolts
    
    def update(self):
        """更新特效"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        
        if elapsed >= self.lifetime:
            return False  # 特效结束
        
        # 更新爆炸粒子
        if self.effect_type == 'explosion':
            for particle in self.particles:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vx'] *= 0.95  # 摩擦力
                particle['vy'] *= 0.95
        
        return True  # 特效继续
    
    def draw(self, screen):
        """绘制特效"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        progress = elapsed / self.lifetime
        alpha = int(self.max_alpha * (1 - progress))
        
        if self.effect_type == 'lightning':
            self.draw_lightning(screen, alpha)
        elif self.effect_type == 'explosion':
            self.draw_explosion(screen, alpha)
    
    def draw_lightning(self, screen, alpha):
        """绘制闪电特效"""
        # 确保alpha是整数
        alpha = int(alpha)
        
        # 创建半透明表面
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # 绘制多条闪电
        for bolt in self.bolts:
            # 主闪电
            main_color = (*self.color[:3], max(0, min(255, alpha)))
            pygame.draw.line(surface, main_color, 
                           (bolt[0], bolt[1]), (bolt[2], bolt[3]), 4)
            # 闪光效果
            flash_color = (255, 255, 255, max(0, min(255, alpha // 2)))
            pygame.draw.line(surface, flash_color, 
                           (bolt[0], bolt[1]), (bolt[2], bolt[3]), 8)
        
        screen.blit(surface, (0, 0))
        
        # 在目标位置添加闪光
        flash_radius = int(30 * (1 - (pygame.time.get_ticks() - self.start_time) / self.lifetime))
        if flash_radius > 0:
            flash_surface = pygame.Surface((flash_radius * 2, flash_radius * 2), pygame.SRCALPHA)
            flash_color = (*self.color[:3], max(0, min(255, alpha // 2)))
            pygame.draw.circle(flash_surface, flash_color, 
                             (flash_radius, flash_radius), flash_radius)
            screen.blit(flash_surface, (self.target_x - flash_radius, self.target_y - flash_radius))
    
    def draw_explosion(self, screen, alpha):
        """绘制爆炸特效"""
        # 计算进度
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        progress = elapsed / self.lifetime
        
        # 确保alpha是整数
        alpha = int(alpha)
        
        # 绘制爆炸波纹
        wave_radius = int(self.size * (1 + progress * 2))
        wave_surface = pygame.Surface((wave_radius * 2, wave_radius * 2), pygame.SRCALPHA)
        wave_color = (*self.color[:3], max(0, min(255, alpha // 3)))
        pygame.draw.circle(wave_surface, wave_color, 
                         (wave_radius, wave_radius), wave_radius, 3)
        screen.blit(wave_surface, (self.x - wave_radius, self.y - wave_radius))
        
        # 绘制粒子
        for particle in self.particles:
            particle_alpha = int(alpha * (1 - abs(particle['vx']) / 6))
            particle_alpha = max(0, min(255, particle_alpha))
            if particle_alpha > 0:
                particle_color = (*self.color[:3], particle_alpha)
                pygame.draw.circle(screen, particle_color, 
                                 (int(particle['x']), int(particle['y'])), 
                                 particle['size'])


class SkillOption:
    """技能选项类"""
    
    def __init__(self, x, y, width, height, skill_data):
        self.rect = pygame.Rect(x, y, width, height)
        self.skill_data = skill_data
        self.hovered = False
    
    def check_hover(self, mouse_pos):
        """检查鼠标悬停"""
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered
    
    def draw(self, screen, font, small_font):
        """绘制技能选项"""
        # 背景
        color = LIGHT_BLUE if self.hovered else DARK_GRAY
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 3)
        
        # 文本
        title = font.render(self.skill_data['name'], True, WHITE)
        desc = small_font.render(self.skill_data['description'], True, WHITE)
        
        title_rect = title.get_rect(centerx=self.rect.centerx, top=self.rect.top + 10)
        desc_rect = desc.get_rect(centerx=self.rect.centerx, top=title_rect.bottom + 10)
        
        screen.blit(title, title_rect)
        screen.blit(desc, desc_rect)


class Game:
    """游戏主类"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("最终幸存者 - Survivors")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.game_over = False
        
        # 游戏对象
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = []
        self.projectiles = []
        self.exp_gems = []
        
        # 游戏状态
        self.score = 0
        self.wave = 1
        self.enemies_spawned = 0
        self.enemies_per_wave = 35  # 增加初始敌人数量从20到35
        self.spawn_timer = 0
        self.spawn_interval = 600  # 加快生成速度从1000ms到600ms
        
        # 敌人升级系统
        self.enemy_upgrade_timer = 0
        self.enemy_upgrade_interval = 20000  # 20秒
        self.enemy_level = 1
        self.waiting_for_enemy_upgrade = False
        
        # 技能系统
        self.available_skills = [
            {
                'id': 'damage_up',
                'name': '攻击力提升',
                'description': '伤害 +5',
                'apply': lambda p: setattr(p, 'damage', p.damage + 5)
            },
            {
                'id': 'attack_speed_up',
                'name': '攻击速度提升',
                'description': '攻速 +20%',
                'apply': lambda p: setattr(p, 'attack_speed', p.attack_speed * 1.2)
            },
            {
                'id': 'range_up',
                'name': '攻击范围提升',
                'description': '范围 +20',
                'apply': lambda p: setattr(p, 'attack_range', p.attack_range + 20)
            },
            {
                'id': 'speed_up',
                'name': '移动速度提升',
                'description': '移速 +0.5',
                'apply': lambda p: setattr(p, 'speed', p.speed + 0.5)
            },
            {
                'id': 'health_up',
                'name': '最大生命提升',
                'description': '最大生命 +30',
                'apply': lambda p: (setattr(p, 'max_health', p.max_health + 30), 
                                   setattr(p, 'health', p.health + 30))
            },
            {
                'id': 'projectile_count',
                'name': '多重射击',
                'description': '投射物数量 +1',
                'apply': lambda p: setattr(p, 'projectile_count', p.projectile_count + 1)
            },
            {
                'id': 'piercing',
                'name': '穿透',
                'description': '穿透 +1',
                'apply': lambda p: setattr(p, 'piercing', p.piercing + 1)
            },
            {
                'id': 'orbiting_shield',
                'name': '环绕护盾',
                'description': '获得旋转护盾',
                'apply': lambda p: (setattr(p, 'has_orbiting_shield', True),
                                   setattr(p, 'shield_count', p.shield_count + 1))
            },
            {
                'id': 'lightning',
                'name': '闪电链',
                'description': '周期性释放闪电',
                'apply': lambda p: (setattr(p, 'has_lightning', True),
                                   setattr(p, 'lightning_damage', p.lightning_damage + 5))
            },
            {
                'id': 'explosion',
                'name': '爆炸光环',
                'description': '周期性爆炸伤害',
                'apply': lambda p: setattr(p, 'has_explosion', True)
            },
            {
                'id': 'regen',
                'name': '生命恢复',
                'description': '每秒恢复2点生命',
                'apply': lambda p: setattr(p, 'health_regen', p.health_regen + 2)
            },
            {
                'id': 'full_heal',
                'name': '血量回满',
                'description': '立即恢复全部生命值',
                'apply': lambda p: setattr(p, 'health', p.max_health)
            }
        ]
        
        self.level_up_choices = []
        self.waiting_for_choice = False
        
        # 字体 - 使用中文字体
        self.font_large = get_chinese_font(72)
        self.font_medium = get_chinese_font(48)
        self.font_small = get_chinese_font(36)
        
        # 特效计时器
        self.lightning_timer = 0
        self.explosion_timer = 0
        self.shield_angle = 0
        
        # 特效列表
        self.effects = []  # 存储所有视觉特效
        
        # 伤害数字
        self.damage_numbers = []
    
    def spawn_enemy(self):
        """生成敌人"""
        # 限制最大敌人数量,避免性能问题(增加到200)
        if len(self.enemies) >= 200:
            return
        
        # 在屏幕边缘随机生成
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if side == 'top':
            x = random.randint(0, SCREEN_WIDTH)
            y = -30
        elif side == 'bottom':
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 30
        elif side == 'left':
            x = -30
            y = random.randint(0, SCREEN_HEIGHT)
        else:
            x = SCREEN_WIDTH + 30
            y = random.randint(0, SCREEN_HEIGHT)
        
        # 根据波次决定敌人类型
        enemy_type = "basic"
        rand = random.random()
        
        if self.wave >= 3 and rand < 0.2:
            enemy_type = "fast"
        elif self.wave >= 5 and rand < 0.15:
            enemy_type = "tank"
        elif self.wave >= 10 and rand < 0.05:
            enemy_type = "boss"
        
        # 使用当前全局敌人等级生成新敌人
        self.enemies.append(Enemy(x, y, enemy_type, self.enemy_level))
        self.enemies_spawned += 1
    
    def find_nearest_enemy(self):
        """找到最近的敌人"""
        nearest = None
        min_distance = float('inf')
        
        for enemy in self.enemies:
            dx = enemy.x - self.player.x
            dy = enemy.y - self.player.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < min_distance and distance <= self.player.attack_range:
                min_distance = distance
                nearest = enemy
        
        return nearest
    
    def attack(self):
        """玩家攻击"""
        current_time = pygame.time.get_ticks()
        attack_cooldown = 1000 / self.player.attack_speed
        
        if current_time - self.player.last_attack_time >= attack_cooldown:
            target = self.find_nearest_enemy()
            
            if target:
                # 创建投射物
                for i in range(self.player.projectile_count):
                    # 如果有多个投射物，稍微分散角度
                    angle_offset = (i - self.player.projectile_count // 2) * 10
                    target_x = target.x + math.sin(math.radians(angle_offset)) * 20
                    target_y = target.y + math.cos(math.radians(angle_offset)) * 20
                    
                    projectile = Projectile(
                        self.player.x, self.player.y,
                        target_x, target_y,
                        self.player.damage,
                        self.player.projectile_speed,
                        self.player.piercing
                    )
                    self.projectiles.append(projectile)
                
                self.player.last_attack_time = current_time
    
    def update_lightning(self):
        """更新闪电效果"""
        if not self.player.has_lightning:
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.lightning_timer >= self.player.lightning_interval:
            # 对范围内所有敌人造成伤害并创建闪电特效
            for enemy in self.enemies[:]:
                dx = enemy.x - self.player.x
                dy = enemy.y - self.player.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance <= self.player.attack_range * 1.5:
                    # 创建闪电特效(限制数量)
                    if len(self.effects) < 20:
                        lightning_effect = VisualEffect(
                            self.player.x, self.player.y,
                            'lightning',
                            target_x=enemy.x,
                            target_y=enemy.y,
                            lifetime=300,
                            color=(100, 150, 255),
                            max_alpha=200
                        )
                        self.effects.append(lightning_effect)
                    
                    # 对敌人造成伤害
                    enemy.take_damage(self.player.lightning_damage)
                    # 添加伤害数字
                    self.add_damage_number(enemy.x, enemy.y - enemy.radius, self.player.lightning_damage)
                    
                    # 如果敌人死亡
                    if enemy.health <= 0:
                        self.create_exp_gem(enemy)
                        self.score += 1
                        self.enemies.remove(enemy)
            
            self.lightning_timer = current_time
    
    def update_explosion(self):
        """更新爆炸效果"""
        if not self.player.has_explosion:
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.explosion_timer >= self.player.explosion_interval:
            # 创建爆炸特效(限制数量)
            if len(self.effects) < 20:
                explosion_effect = VisualEffect(
                    self.player.x, self.player.y,
                    'explosion',
                    size=self.player.explosion_radius,
                    lifetime=600,
                    color=(255, 100, 50),
                    max_alpha=220
                )
                self.effects.append(explosion_effect)
            
            # 对范围内所有敌人造成伤害
            for enemy in self.enemies[:]:
                dx = enemy.x - self.player.x
                dy = enemy.y - self.player.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance <= self.player.explosion_radius:
                    # 对敌人造成伤害
                    enemy.take_damage(self.player.explosion_damage)
                    # 添加伤害数字
                    self.add_damage_number(enemy.x, enemy.y - enemy.radius, self.player.explosion_damage)
                    
                    # 如果敌人死亡
                    if enemy.health <= 0:
                        self.create_exp_gem(enemy)
                        self.score += 1
                        self.enemies.remove(enemy)
            
            self.explosion_timer = current_time
    
    def update_shields(self):
        """更新环绕护盾"""
        if self.player.has_orbiting_shield:
            self.shield_angle += self.player.shield_rotation_speed
    
    def check_shield_collision(self):
        """检查护盾碰撞"""
        if not self.player.has_orbiting_shield:
            return
        
        shield_distance = 50
        
        for enemy in self.enemies[:]:
            for i in range(self.player.shield_count):
                angle = math.radians(self.shield_angle + i * (360 / self.player.shield_count))
                shield_x = self.player.x + math.cos(angle) * shield_distance
                shield_y = self.player.y + math.sin(angle) * shield_distance
                
                dx = enemy.x - shield_x
                dy = enemy.y - shield_y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance < enemy.radius + 8:
                    # 对敌人造成伤害
                    enemy.take_damage(self.player.shield_damage)
                    # 添加伤害数字
                    self.add_damage_number(enemy.x, enemy.y - enemy.radius, self.player.shield_damage)
                    
                    # 如果敌人死亡
                    if enemy.health <= 0:
                        self.create_exp_gem(enemy)
                        self.score += 1
                        self.enemies.remove(enemy)
                    break  # 一个敌人一次只被一个护盾击中
    
    def create_exp_gem(self, enemy):
        """创建经验宝石"""
        # 限制经验宝石数量,避免性能问题
        if len(self.exp_gems) < 100:
            gem = ExperienceGem(enemy.x, enemy.y, enemy.exp_value)
            self.exp_gems.append(gem)
    
    def show_level_up_screen(self):
        """显示升级选择界面"""
        self.waiting_for_choice = True
        
        # 暂停敌人升级计时器
        self.enemy_upgrade_paused_time = pygame.time.get_ticks() - self.enemy_upgrade_timer
        
        # 随机选择3个技能
        available = self.available_skills.copy()
        self.level_up_choices = []
        
        for _ in range(min(3, len(available))):
            if available:
                choice = random.choice(available)
                self.level_up_choices.append(choice)
                available.remove(choice)
        
        # 创建技能选项UI
        option_width = 280
        option_height = 150
        spacing = 20
        total_width = 3 * option_width + 2 * spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = SCREEN_HEIGHT // 2 - 100
        
        self.skill_options = []
        for i, skill in enumerate(self.level_up_choices):
            x = start_x + i * (option_width + spacing)
            option = SkillOption(x, start_y, option_width, option_height, skill)
            self.skill_options.append(option)
    
    def apply_skill(self, skill):
        """应用技能"""
        skill['apply'](self.player)
        
        # 升级后朝自身一圈发射子弹
        self.shoot_ring_projectiles()
        
        # 恢复敌人升级计时器
        current_time = pygame.time.get_ticks()
        self.enemy_upgrade_timer = current_time - self.enemy_upgrade_paused_time
        
        self.waiting_for_choice = False
        self.level_up_choices = []
    
    def shoot_ring_projectiles(self):
        """朝自身一圈发射子弹"""
        num_projectiles = 12  # 发射12发子弹形成一圈
        base_damage = self.player.damage * 2  # 伤害是普通攻击的2倍
        
        for i in range(num_projectiles):
            angle = math.radians(i * (360 / num_projectiles))
            # 计算目标位置(从玩家位置向外延伸)
            target_x = self.player.x + math.cos(angle) * 200
            target_y = self.player.y + math.sin(angle) * 200
            
            projectile = Projectile(
                self.player.x, self.player.y,
                target_x, target_y,
                base_damage,
                self.player.projectile_speed * 1.5,  # 速度更快
                self.player.piercing + 2  # 穿透更强
            )
            self.projectiles.append(projectile)
    
    def add_damage_number(self, x, y, damage, color=None):
        """添加伤害数字
        在指定位置创建一个临时显示的伤害数值，用于显示对敌人造成的伤害
        参数:
            x: 伤害数字显示的x坐标
            y: 伤害数字显示的y坐标
            damage: 造成的伤害数值
            color: 伤害数字的颜色，默认为黄色，也可以自定义颜色
        """
        self.damage_numbers.append({
            'x': x,  # 伤害数字的x坐标位置
            'y': y,  # 伤害数字的y坐标位置
            'damage': damage,  # 伤害数值，将作为文本显示
            'time': pygame.time.get_ticks(),  # 当前时间戳，用于计算显示持续时间
            'lifetime': 500,  # 伤害数字的生命周期（毫秒），超过此时间后会被移除
            'color': color if color else YELLOW  # 伤害数字的颜色，默认为黄色，可自定义
        })
    
    def update_damage_numbers(self):
        """更新伤害数字
        更新屏幕上所有伤害数字的状态，移除已经超出生存时间的伤害数字
        通过列表推导式过滤掉超出生命周期的伤害数字，仅保留仍在显示时间内的数字
        """
        current_time = pygame.time.get_ticks()  # 获取当前时间戳，用于计算伤害数字的存活时间
        self.damage_numbers = [
            dn for dn in self.damage_numbers  # 遍历所有伤害数字
            if current_time - dn['time'] < dn['lifetime']  # 检查是否仍在生命周期内，如果是则保留
        ]
    
    def draw_damage_numbers(self, screen):
        """绘制伤害数字
        在屏幕上绘制所有当前存在的伤害数字，并实现向上浮动的动画效果
        参数:
            screen: 游戏屏幕表面，用于绘制伤害数字
        """
        current_time = pygame.time.get_ticks()  # 获取当前时间戳，用于计算伤害数字的显示进度
        font = get_chinese_font(28)  # 获取用于显示伤害数字的字体，大小为28像素

        for dn in self.damage_numbers:  # 遍历所有需要绘制的伤害数字
            elapsed = current_time - dn['time']  # 计算伤害数字已经存在的时间
            progress = elapsed / dn['lifetime']  # 计算伤害数字的存在进度(0.0-1.0)，用于动画效果

            # 向上浮动动画
            y_offset = progress * 30  # 根据存在进度计算y轴偏移量，实现向上浮动效果，最大偏移30像素

            # 使用自定义颜色或默认黄色
            color = dn.get('color', YELLOW)  # 获取伤害数字的颜色，如果未指定则使用默认的黄色

            text = font.render(str(dn['damage']), True, color)  # 将伤害数值渲染为文本表面
            screen.blit(text, (dn['x'] - 10, dn['y'] - y_offset))  # 将伤害数字绘制到屏幕上，位置稍微向左偏移10像素
    
    def check_wave_complete(self):
        """检查波次是否完成
        检查当前波次的所有敌人是否已被消灭，如果已完成则进入下一波次
        并增加敌人的数量和生成速度，同时给玩家提供治疗奖励
        """
        # 检查条件：已生成的敌人数量大于等于本波应生成总数 且 当前场上没有剩余敌人
        if self.enemies_spawned >= self.enemies_per_wave and len(self.enemies) == 0:
            self.wave += 1  # 增加波次数
            self.enemies_spawned = 0  # 重置已生成敌人计数器
            # 增加下一波敌人数量，增长系数从1.3提高到1.4，使敌人数量增长更快
            self.enemies_per_wave = int(self.enemies_per_wave * 1.4)
            # 减少敌人生成间隔时间，加快生成速度，但最小间隔保持在200ms以避免过于密集
            self.spawn_interval = max(200, self.spawn_interval - 100)

            # 波次奖励：为玩家恢复20点生命值
            self.player.heal(20)
    
    def draw_ui(self, screen):
        """绘制游戏UI界面
        在屏幕上显示游戏的各种信息，包括分数、波次、敌人统计、经验条等
        参数:
            screen: 游戏屏幕表面，用于绘制UI元素
        """
        # 绘制分数信息，显示在屏幕左上角
        score_text = self.font_small.render(f"分数: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # 绘制当前波次信息
        wave_text = self.font_small.render(f"波次: {self.wave}", True, WHITE)
        screen.blit(wave_text, (10, 50))

        # 绘制敌人等级和数量统计信息
        if self.enemies:
            # 如果当前有敌人，计算平均等级和最高等级
            avg_enemy_level = sum(e.level for e in self.enemies) / len(self.enemies)  # 计算平均等级
            max_enemy_level = max(e.level for e in self.enemies)  # 计算最高敌人等级
            # 生成包含敌人数量、平均等级和最高等级的文本
            enemy_info_text = self.font_small.render(f"敌人: {len(self.enemies)} | 平均Lv.{avg_enemy_level:.1f} | 最高Lv.{max_enemy_level}", True, RED)
        else:
            # 如果当前没有敌人，显示0个敌人
            enemy_info_text = self.font_small.render(f"敌人: 0", True, RED)
        screen.blit(enemy_info_text, (10, 90))

        # 绘制全局敌人等级信息（用于新生成敌人）
        global_level_text = self.font_small.render(f"新生成敌人等级: {self.enemy_level}", True, ORANGE)
        screen.blit(global_level_text, (10, 130))

        # 绘制敌人升级进度条
        upgrade_bar_width = 300  # 进度条宽度
        upgrade_bar_height = 25  # 进度条高度
        upgrade_bar_x = SCREEN_WIDTH - upgrade_bar_width - 10  # 进度条x坐标，靠右对齐
        upgrade_bar_y = 70  # 进度条y坐标

        current_time = pygame.time.get_ticks()  # 获取当前时间戳
        elapsed = current_time - self.enemy_upgrade_timer  # 计算自上次升级计时开始经过的时间
        progress = min(1.0, elapsed / self.enemy_upgrade_interval)  # 计算升级进度，限制在0.0-1.0之间

        # 绘制进度条背景
        pygame.draw.rect(screen, DARK_GRAY, (upgrade_bar_x, upgrade_bar_y, upgrade_bar_width, upgrade_bar_height))
        # 计算进度条填充宽度
        upgrade_width = int(upgrade_bar_width * progress)
        # 根据进度改变进度条颜色，越接近升级颜色越红
        if progress > 0.8:
            color = RED  # 快要升级时显示红色
        elif progress > 0.5:
            color = ORANGE  # 升级中期显示橙色
        else:
            color = GREEN  # 升级初期显示绿色
        pygame.draw.rect(screen, color, (upgrade_bar_x, upgrade_bar_y, upgrade_width, upgrade_bar_height))
        # 绘制进度条边框
        pygame.draw.rect(screen, WHITE, (upgrade_bar_x, upgrade_bar_y, upgrade_bar_width, upgrade_bar_height), 3)

        # 绘制进度百分比文字
        upgrade_text = self.font_small.render(f"下次升级: {int(progress * 100)}%", True, WHITE)
        text_rect = upgrade_text.get_rect(centerx=upgrade_bar_x + upgrade_bar_width // 2, centery=upgrade_bar_y + upgrade_bar_height // 2)
        screen.blit(upgrade_text, text_rect)

        # 绘制玩家经验条
        exp_bar_width = 300  # 经验条宽度
        exp_bar_height = 25  # 经验条高度
        exp_bar_x = SCREEN_WIDTH - exp_bar_width - 10  # 经验条x坐标，靠右对齐
        exp_bar_y = 110  # 经验条y坐标

        # 绘制经验条背景
        pygame.draw.rect(screen, DARK_GRAY, (exp_bar_x, exp_bar_y, exp_bar_width, exp_bar_height))
        # 计算经验条填充宽度，根据当前经验和升级所需经验的比例
        exp_width = int(exp_bar_width * (self.player.exp / self.player.exp_to_next_level))
        # 绘制金色的经验条填充
        pygame.draw.rect(screen, GOLD, (exp_bar_x, exp_bar_y, exp_width, exp_bar_height))
        # 绘制经验条边框
        pygame.draw.rect(screen, WHITE, (exp_bar_x, exp_bar_y, exp_bar_width, exp_bar_height), 3)

        # 绘制经验数值文本
        exp_text = self.font_small.render(f"EXP: {self.player.exp}/{self.player.exp_to_next_level}", True, WHITE)
        exp_text_rect = exp_text.get_rect(centerx=exp_bar_x + exp_bar_width // 2, centery=exp_bar_y + exp_bar_height // 2)
        screen.blit(exp_text, exp_text_rect)
    
    def draw_pause_screen(self, screen):
        """绘制暂停界面
        在屏幕上显示半透明的覆盖层和暂停信息，提示玩家如何继续游戏
        参数:
            screen: 游戏屏幕表面，用于绘制暂停界面
        """
        # 创建半透明黑色覆盖层，遮挡游戏画面
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # 创建与屏幕同大小的表面
        overlay.set_alpha(128)  # 设置透明度为128（0-255范围）
        overlay.fill(BLACK)  # 填充黑色
        screen.blit(overlay, (0, 0))  # 将覆盖层绘制到屏幕上

        # 绘制"游戏暂停"文本，居中显示
        pause_text = self.font_large.render("游戏暂停", True, WHITE)  # 渲染白色大字体的暂停文本
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # 获取文本矩形并居中定位
        screen.blit(pause_text, text_rect)  # 将暂停文本绘制到屏幕上

        # 绘制操作提示文本
        hint_text = self.font_small.render("按 ESC 继续游戏", True, WHITE)  # 渲染白色小字体的操作提示
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))  # 定位在暂停文本下方
        screen.blit(hint_text, hint_rect)  # 将操作提示绘制到屏幕上
    
    def draw_game_over_screen(self, screen):
        """绘制游戏结束界面
        在屏幕上显示游戏结束信息，包括最终分数、到达波次和重新开始选项
        参数:
            screen: 游戏屏幕表面，用于绘制游戏结束界面
        """
        # 创建不透明的黑色覆盖层，完全遮挡游戏画面
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # 创建与屏幕同大小的表面
        overlay.set_alpha(200)  # 设置较高的透明度（接近不透明）
        overlay.fill(BLACK)  # 填充黑色
        screen.blit(overlay, (0, 0))  # 将覆盖层绘制到屏幕上

        # 绘制"游戏结束"标题文本
        game_over_text = self.font_large.render("游戏结束", True, RED)  # 渲染红色大字体的结束文本
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))  # 居中定位在屏幕上方
        screen.blit(game_over_text, text_rect)  # 将结束文本绘制到屏幕上

        # 绘制最终分数
        score_text = self.font_medium.render(f"最终分数: {self.score}", True, WHITE)  # 渲染白色中等字体的分数文本
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))  # 居中定位在标题下方
        screen.blit(score_text, score_rect)  # 将分数文本绘制到屏幕上

        # 绘制到达波次
        wave_text = self.font_medium.render(f"到达波次: {self.wave}", True, WHITE)  # 渲染白色中等字体的波次文本
        wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))  # 居中定位在分数下方
        screen.blit(wave_text, wave_rect)  # 将波次文本绘制到屏幕上

        # 绘制重新开始和退出操作提示
        restart_text = self.font_small.render("按 R 重新开始 | 按 ESC 退出", True, WHITE)  # 渲染白色小字体的操作提示
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))  # 居中定位在最下方
        screen.blit(restart_text, restart_rect)  # 将操作提示绘制到屏幕上
    
    def draw_level_up_screen(self, screen):
        """绘制升级选择界面
        当玩家获得足够经验值升级时，显示技能选择界面，让玩家选择要提升的技能
        参数:
            screen: 游戏屏幕表面，用于绘制升级选择界面
        """
        # 创建不透明的黑色覆盖层，暂时遮挡游戏画面
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # 创建与屏幕同大小的表面
        overlay.set_alpha(200)  # 设置较高的透明度（接近不透明）
        overlay.fill(BLACK)  # 填充黑色
        screen.blit(overlay, (0, 0))  # 将覆盖层绘制到屏幕上

        # 绘制升级标题文本
        title_text = self.font_large.render("升级! 选择一个技能", True, GOLD)  # 渲染金色大字体的升级标题
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))  # 居中定位在屏幕上方
        screen.blit(title_text, title_rect)  # 将标题文本绘制到屏幕上

        # 绘制所有可用的技能选项
        for option in self.skill_options:  # 遍历所有技能选项
            option.draw(screen, self.font_medium, self.font_small)  # 绘制每个技能选项
    
    def draw_enemy_upgrade_screen(self, screen):
        """绘制敌人升级确认界面
        当敌人升级计时器到达时，显示敌人升级的警告信息和属性提升详情
        参数:
            screen: 游戏屏幕表面，用于绘制敌人升级界面
        """
        # 创建不透明的黑色覆盖层，暂时遮挡游戏画面
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # 创建与屏幕同大小的表面
        overlay.set_alpha(220)  # 设置较高的透明度（接近不透明）
        overlay.fill(BLACK)  # 填充黑色
        screen.blit(overlay, (0, 0))  # 将覆盖层绘制到屏幕上

        # 绘制敌人升级警告文本
        warning_text = self.font_large.render("⚠ 敌人即将升级! ⚠", True, RED)  # 渲染红色大字体的警告文本
        warning_rect = warning_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))  # 居中定位在屏幕上方
        screen.blit(warning_text, warning_rect)  # 将警告文本绘制到屏幕上

        # 绘制敌人等级变化信息
        level_text = self.font_medium.render(f"敌人等级: {self.enemy_level} → {self.enemy_level + 1}", True, ORANGE)  # 渲染橙色中等字体的等级信息
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))  # 居中定位在警告文本下方
        screen.blit(level_text, level_rect)  # 将等级信息绘制到屏幕上

        # 显示升级后的属性变化
        font_small = get_chinese_font(32)  # 获取用于显示属性变化的小字体
        stats_text = [  # 定义升级后属性提升的文本列表
            f"❤️ 生命值提升 30%",
            f"⚔️ 攻击力提升 20%",
            f"✨ 经验掉落提升 25%"
        ]

        # 遍历属性变化列表并绘制到屏幕上
        for i, stat in enumerate(stats_text):  # 遍历属性变化文本列表
            stat_surface = font_small.render(stat, True, YELLOW)  # 渲染黄色字体的属性变化文本
            # 计算每个属性文本的位置，垂直排列
            stat_rect = stat_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20 + i * 45))
            screen.blit(stat_surface, stat_rect)  # 将属性变化文本绘制到屏幕上

        # 绘制确认升级的按键提示
        confirm_text = self.font_small.render("按 SPACE 确认升级", True, WHITE)  # 渲染白色小字体的按键提示
        confirm_rect = confirm_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140))  # 居中定位在属性变化下方
        screen.blit(confirm_text, confirm_rect)  # 将按键提示绘制到屏幕上

        # 绘制倒计时提示，显示剩余时间
        time_left = max(0, int((self.enemy_upgrade_interval - (pygame.time.get_ticks() - self.enemy_upgrade_timer)) / 1000))  # 计算剩余升级时间（秒）
        time_text = font_small.render(f"剩余时间: {time_left} 秒", True, RED)  # 渲染红色字体的倒计时文本
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 190))  # 居中定位在按键提示下方
        screen.blit(time_text, time_rect)  # 将倒计时文本绘制到屏幕上
    
    def reset_game(self):
        """重置游戏
        将游戏状态恢复到初始状态，包括玩家、敌人、子弹、经验宝石、特效等所有游戏元素
        """
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # 创建新的玩家实例，位于屏幕中心
        self.enemies = []  # 清空敌人列表
        self.projectiles = []  # 清空子弹/投射物列表
        self.exp_gems = []  # 清空经验宝石列表
        self.effects = []  # 重置特效列表
        self.score = 0  # 重置分数为0
        self.wave = 1  # 重置波次数为1
        self.enemies_spawned = 0  # 重置已生成敌人计数器
        self.enemies_per_wave = 10  # 重置每波敌人数量为10
        self.spawn_interval = 2000  # 重置敌人生成间隔为2秒
        self.game_over = False  # 重置游戏结束标志
        self.paused = False  # 重置暂停标志
        self.waiting_for_choice = False  # 重置等待选择标志
        self.waiting_for_enemy_upgrade = False  # 重置等待敌人升级标志
        self.damage_numbers = []  # 清空伤害数字列表
        self.lightning_timer = 0  # 重置闪电攻击计时器
        self.explosion_timer = 0  # 重置爆炸效果计时器
        self.enemy_upgrade_timer = 0  # 重置敌人升级计时器
        self.enemy_upgrade_paused_time = 0  # 重置敌人升级暂停时间
        self.enemy_level = 1  # 重置敌人等级为1
        self.enemies_per_wave = 35  # 重置初始敌人数量为35
        self.spawn_interval = 600  # 重置生成间隔为600毫秒
    
    def upgrade_all_enemies(self):
        """升级所有敌人并发射子弹
        将当前所有敌人提升一个等级，增加它们的生命值和攻击力，
        同时播放升级视觉特效并向四周发射子弹
        """
        self.enemy_level += 1  # 提升全局敌人等级

        # 升级所有现存的敌人，并收集升级信息
        upgraded_count = 0  # 记录升级的敌人数量
        total_health_increase = 0  # 记录总生命值增加量

        for enemy in self.enemies:  # 遍历所有当前敌人
            upgrade_info = enemy.upgrade()  # 升级单个敌人，返回升级信息
            upgraded_count += 1  # 增加升级计数
            total_health_increase += upgrade_info['health_increase']  # 累加生命值增加量

            # 为每个升级的敌人创建小型升级特效(限制特效数量)
            if len(self.effects) < 30:  # 检查特效数量限制，避免性能下降
                # 创建金色的升级特效
                upgrade_effect = VisualEffect(
                    enemy.x, enemy.y,  # 特效位置为敌人当前位置
                    'explosion',  # 特效类型为爆炸
                    size=40,  # 特效大小
                    lifetime=500,  # 特效持续时间500毫秒
                    color=(255, 215, 0),  # 金色
                    max_alpha=200  # 最大透明度
                )
                self.effects.append(upgrade_effect)  # 添加到特效列表

        # 向四周发射子弹特效，增加视觉冲击感
        self.shoot_ring_projectiles()

        # 创建全局升级特效(限制特效数量)
        if len(self.effects) < 20:  # 检查特效数量限制
            # 创建大型全局升级特效
            global_upgrade_effect = VisualEffect(
                self.player.x, self.player.y,  # 以玩家为中心
                'explosion',  # 特效类型为爆炸
                size=250,  # 特效大小较大
                lifetime=1000,  # 特效持续时间1秒
                color=(255, 50, 50),  # 红色
                max_alpha=255  # 不透明
            )
            self.effects.append(global_upgrade_effect)  # 添加到特效列表

        # 显示升级统计信息（通过伤害数字显示）
        if upgraded_count > 0:  # 如果有敌人升级
            avg_health_increase = total_health_increase // upgraded_count  # 计算平均生命值增加量
            # 在屏幕中央显示升级信息
            self.add_damage_number(
                SCREEN_WIDTH // 2,  # x坐标为屏幕中心
                SCREEN_HEIGHT // 2 - 50,  # y坐标在屏幕中心偏上
                f"敌人升级! +{avg_health_increase}HP",  # 显示升级信息和平均血量增加
                color=GREEN  # 使用绿色显示升级信息
            )
    
    def run(self):
        """运行游戏主循环
        游戏的主要运行循环，负责处理事件、更新游戏状态和绘制游戏画面
        """
        while self.running:  # 主循环，直到游戏结束
            dt = self.clock.tick(FPS)  # 控制游戏帧率，并获取每帧的时间差

            # 事件处理
            for event in pygame.event.get():  # 遍历所有待处理的事件
                if event.type == pygame.QUIT:  # 检测窗口关闭事件
                    self.running = False  # 设置运行标志为False，退出循环

                if event.type == pygame.KEYDOWN:  # 检测键盘按下事件
                    if event.key == pygame.K_ESCAPE:  # 检测ESC键
                        if self.game_over:  # 如果游戏结束，退出游戏
                            self.running = False
                        elif self.waiting_for_choice:  # 如果等待技能选择，不能暂停
                            pass  # 升级时不能暂停
                        elif self.waiting_for_enemy_upgrade:  # 如果等待敌人升级确认，不能暂停
                            pass  # 敌人升级确认时不能暂停
                        else:
                            self.paused = not self.paused  # 切换暂停状态

                    if event.key == pygame.K_r and self.game_over:  # 检测R键重置游戏
                        self.reset_game()  # 重置游戏到初始状态

                    # 敌人升级确认
                    if event.key == pygame.K_SPACE and self.waiting_for_enemy_upgrade:  # 检测空格键确认敌人升级
                        self.upgrade_all_enemies()  # 升级所有敌人
                        self.waiting_for_enemy_upgrade = False  # 重置等待升级标志
                        self.enemy_upgrade_timer = pygame.time.get_ticks()  # 重置升级计时器

                if event.type == pygame.MOUSEBUTTONDOWN and self.waiting_for_choice:  # 检测鼠标点击事件（技能选择）
                    mouse_pos = pygame.mouse.get_pos()  # 获取鼠标位置
                    for option in self.skill_options:  # 遍历技能选项
                        if option.rect.collidepoint(mouse_pos):  # 检测是否点击了某个选项
                            self.apply_skill(option.skill_data)  # 应用选中的技能
                            break
            
            # 游戏状态更新（仅在非暂停、非游戏结束、非技能选择、非敌人升级确认状态下执行）
            if not self.paused and not self.game_over and not self.waiting_for_choice and not self.waiting_for_enemy_upgrade:
                # 更新玩家状态
                keys = pygame.key.get_pressed()  # 获取当前按键状态
                self.player.move(keys)  # 根据按键状态移动玩家

                # 生命恢复机制
                if self.player.health_regen > 0:  # 如果玩家有生命恢复属性
                    # 按照时间比例恢复生命值
                    self.player.heal(self.player.health_regen * dt / 1000)

                # 生成敌人
                current_time = pygame.time.get_ticks()  # 获取当前时间
                # 检查是否到达生成新敌人的时间
                if current_time - self.spawn_timer >= self.spawn_interval:
                    # 检查当前波次是否还有敌人未生成
                    if self.enemies_spawned < self.enemies_per_wave:
                        self.spawn_enemy()  # 生成一个新敌人
                        self.spawn_timer = current_time  # 重置生成计时器

                # 更新敌人状态
                current_time = pygame.time.get_ticks()
                for enemy in self.enemies[:]:  # 遍历所有敌人
                    enemy.move_towards(self.player.x, self.player.y)  # 敌人朝玩家移动

                    # 检查与玩家碰撞
                    dx = enemy.x - self.player.x  # 计算x轴距离
                    dy = enemy.y - self.player.y  # 计算y轴距离
                    distance = math.sqrt(dx**2 + dy**2)  # 计算实际距离

                    if distance < enemy.radius + self.player.radius:  # 如果发生碰撞
                        # 刚接触时立即攻击,之后每1秒攻击一次
                        should_attack = False

                        if not enemy.has_attacked_on_contact:  # 如果尚未在接触时攻击
                            # 第一次接触,立即攻击
                            should_attack = True
                            enemy.has_attacked_on_contact = True  # 设置已攻击标记
                        elif current_time - enemy.last_attack_time >= enemy.attack_cooldown:  # 检查攻击冷却
                            # 之后每1秒攻击一次
                            should_attack = True

                        if should_attack:  # 如果应该攻击
                            # 对玩家造成伤害，如果玩家死亡则设置游戏结束标志
                            if self.player.take_damage(enemy.damage):
                                self.game_over = True
                            enemy.last_attack_time = current_time  # 更新最后攻击时间
                    else:
                        # 离开接触范围后重置标记
                        enemy.has_attacked_on_contact = False
                
                # 玩家攻击
                self.attack()

                # 更新投射物（子弹等）
                for projectile in self.projectiles[:]:  # 遍历所有投射物
                    projectile.update()  # 更新投射物状态

                    if projectile.is_off_screen():  # 检查投射物是否离开屏幕
                        self.projectiles.remove(projectile)  # 从列表中移除
                        continue

                    # 检查与敌人碰撞(优化:只检查附近的敌人)
                    hit_this_frame = False
                    for enemy in self.enemies[:]:  # 遍历所有敌人
                        if hit_this_frame:  # 如果当前帧已有命中，则跳出循环
                            break

                        # 检查是否已经击中过该敌人（穿透机制）
                        if id(enemy) not in projectile.hit_enemies:
                            dx = enemy.x - projectile.x  # 计算x轴距离
                            dy = enemy.y - projectile.y  # 计算y轴距离
                            distance = math.sqrt(dx**2 + dy**2)  # 计算实际距离

                            # 如果投射物与敌人发生碰撞
                            if distance < enemy.radius + projectile.radius:
                                # 对敌人造成伤害
                                enemy.take_damage(projectile.damage)
                                # 添加伤害数字显示
                                self.add_damage_number(enemy.x, enemy.y - enemy.radius, projectile.damage)

                                # 如果敌人死亡
                                if enemy.health <= 0:
                                    self.create_exp_gem(enemy)  # 生成经验宝石
                                    self.score += 1  # 增加分数
                                    # 敌人死亡后立即从列表中移除
                                    self.enemies.remove(enemy)

                                projectile.hit_enemies.add(id(enemy))  # 记录已击中的敌人

                                # 如果穿透次数已满
                                if len(projectile.hit_enemies) > projectile.piercing:
                                    if projectile in self.projectiles:
                                        self.projectiles.remove(projectile)  # 移除投射物
                                    hit_this_frame = True  # 标记当前帧已有命中
                                    break
                
                # 更新各种特效
                self.update_lightning()  # 更新闪电特效
                self.update_explosion()  # 更新爆炸特效
                self.update_shields()  # 更新护盾状态
                self.check_shield_collision()  # 检查护盾碰撞

                # 更新经验宝石
                for gem in self.exp_gems[:]:  # 遍历所有经验宝石
                    # 检查经验宝石是否被玩家拾取
                    if gem.update(self.player.x, self.player.y):
                        # 玩家获得经验，如果升级则显示升级界面
                        if self.player.gain_exp(gem.value):
                            self.show_level_up_screen()
                        self.exp_gems.remove(gem)  # 从列表中移除已拾取的宝石

                # 更新伤害数字
                self.update_damage_numbers()

                # 更新视觉特效
                self.effects = [effect for effect in self.effects if effect.update()]  # 更新并过滤有效特效

                # 检查波次完成
                self.check_wave_complete()

                # 检查敌人升级
                current_time = pygame.time.get_ticks()
                # 检查是否到达敌人升级时间
                if current_time - self.enemy_upgrade_timer >= self.enemy_upgrade_interval:
                    self.waiting_for_enemy_upgrade = True  # 设置等待敌人升级标志

            # 绘制游戏画面
            self.screen.fill(DARK_GRAY)  # 填充深灰色背景

            # 绘制经验宝石
            for gem in self.exp_gems:
                gem.draw(self.screen)  # 绘制每个经验宝石

            # 绘制敌人
            for enemy in self.enemies:
                enemy.draw(self.screen)  # 绘制每个敌人

            # 绘制投射物
            for projectile in self.projectiles:
                projectile.draw(self.screen)  # 绘制每个投射物
            
            # 绘制特效(在玩家和护盾之下)
            for effect in self.effects:
                effect.draw(self.screen)  # 绘制每个特效

            # 绘制玩家
            if not self.game_over:
                self.player.draw(self.screen)  # 绘制玩家

            # 绘制环绕护盾(带特效)
            if self.player.has_orbiting_shield and not self.game_over:  # 如果玩家有环绕护盾且游戏未结束
                shield_distance = 50  # 护盾距离玩家的距离
                for i in range(self.player.shield_count):  # 遍历所有护盾
                    # 计算护盾角度
                    angle = math.radians(self.shield_angle + i * (360 / self.player.shield_count))
                    # 计算护盾位置
                    shield_x = self.player.x + math.cos(angle) * shield_distance
                    shield_y = self.player.y + math.sin(angle) * shield_distance

                    # 护盾光晕效果
                    glow_radius = 12 + int(3 * math.sin(pygame.time.get_ticks() / 100))  # 让光晕轻微闪烁
                    glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surface, (0, 255, 255, 80), (glow_radius, glow_radius), glow_radius)
                    self.screen.blit(glow_surface, (int(shield_x) - glow_radius, int(shield_y) - glow_radius))

                    # 护盾核心
                    pygame.draw.circle(self.screen, CYAN, (int(shield_x), int(shield_y)), 8)  # 绘制护盾主体
                    pygame.draw.circle(self.screen, WHITE, (int(shield_x), int(shield_y)), 8, 2)  # 绘制护盾边框

                    # 护盾轨迹线（当有多个护盾时连接它们）
                    if self.player.shield_count > 1:  # 只有在有多个护盾时才绘制连线
                        # 计算下一个护盾的角度
                        next_angle = math.radians(self.shield_angle + ((i + 1) % self.player.shield_count) * (360 / self.player.shield_count))
                        # 计算下一个护盾的位置
                        next_x = self.player.x + math.cos(next_angle) * shield_distance
                        next_y = self.player.y + math.sin(next_angle) * shield_distance
                        # 使用正确的RGBA格式绘制连线
                        trail_color = (0, 255, 255, 100)
                        pygame.draw.line(self.screen, trail_color,
                                       (int(shield_x), int(shield_y)),
                                       (int(next_x), int(next_y)), 2)

            # 绘制伤害数字
            self.draw_damage_numbers(self.screen)

            # 绘制UI
            self.draw_ui(self.screen)

            # 绘制特殊界面
            if self.waiting_for_choice:  # 如果等待技能选择
                self.draw_level_up_screen(self.screen)  # 绘制升级界面
            elif self.waiting_for_enemy_upgrade:  # 如果等待敌人升级确认
                self.draw_enemy_upgrade_screen(self.screen)  # 绘制敌人升级界面
            elif self.paused:  # 如果游戏暂停
                self.draw_pause_screen(self.screen)  # 绘制暂停界面
            elif self.game_over:  # 如果游戏结束
                self.draw_game_over_screen(self.screen)  # 绘制游戏结束界面

            pygame.display.flip()  # 更新显示

        pygame.quit()  # 退出Pygame
        sys.exit()  # 退出程序


if __name__ == "__main__":
    game = Game()
    game.run()
