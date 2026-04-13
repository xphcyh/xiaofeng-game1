import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 1000, 700
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
LIGHT_BLUE = (173, 216, 230)
PINK = (255, 192, 203)
DARK_GREEN = (0, 100, 0)

# 创建屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("大富翁游戏")
clock = pygame.time.Clock()

class Property:
    def __init__(self, name, price, rent, color, x, y, width, height):
        self.name = name
        self.price = price
        self.rent = rent
        self.color = color
        self.owner = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_special = False
        
    def draw(self, surface):
        # 绘制地产
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2)
        
        # 绘制地产名称
        font = pygame.font.SysFont("simhei", 14)
        name_text = font.render(self.name, True, BLACK)
        surface.blit(name_text, (self.x + 5, self.y + 5))
        
        # 绘制价格
        price_text = font.render(f"¥{self.price}", True, BLACK)
        surface.blit(price_text, (self.x + 5, self.y + 25))
        
        # 如果有所有者，绘制所有者标记
        if self.owner:
            owner_color = self.owner.color
            pygame.draw.circle(surface, owner_color, (self.x + self.width - 15, self.y + 15), 8)
            pygame.draw.circle(surface, BLACK, (self.x + self.width - 15, self.y + 15), 8, 2)

class SpecialProperty(Property):
    def __init__(self, name, price, rent, color, x, y, width, height, special_type):
        super().__init__(name, price, rent, color, x, y, width, height)
        self.special_type = special_type  # "start", "jail", "parking", "goto_jail", "tax"
        self.is_special = True
        
    def draw(self, surface):
        super().draw(surface)
        
        # 绘制特殊地块标记
        font = pygame.font.SysFont("simhei", 12)
        if self.special_type == "start":
            text = font.render("起点", True, BLACK)
            surface.blit(text, (self.x + 5, self.y + 40))
        elif self.special_type == "jail":
            text = font.render("监狱", True, BLACK)
            surface.blit(text, (self.x + 5, self.y + 40))
        elif self.special_type == "parking":
            text = font.render("停车场", True, BLACK)
            surface.blit(text, (self.x + 5, self.y + 40))
        elif self.special_type == "goto_jail":
            text = font.render("入狱", True, BLACK)
            surface.blit(text, (self.x + 5, self.y + 40))
        elif self.special_type == "tax":
            text = font.render("税款", True, BLACK)
            surface.blit(text, (self.x + 5, self.y + 40))

class Player:
    def __init__(self, name, color, x, y):
        self.name = name
        self.color = color
        self.money = 2000  # 增加起始资金到2000
        self.position = 0  # 在地产列表中的位置
        self.x = x
        self.y = y
        self.radius = 15
        self.in_jail = False
        self.jail_turns = 0
        self.properties = []
        
    def move(self, steps, board):
        if self.in_jail:
            self.jail_turns += 1
            if self.jail_turns >= 3 or steps == 6:  # 三次机会或掷出6点可出狱
                self.in_jail = False
                self.jail_turns = 0
                if steps == 6:
                    self.position = (self.position + steps) % len(board)
            return
            
        self.position = (self.position + steps) % len(board)
        
        # 检查是否经过起点，给予工资
        if self.position < steps % len(board):  # 说明经过了起点
            self.money += 300  # 增加每次经过起点的奖励到300
            
        # 检查特殊地块
        current_property = board[self.position]
        if isinstance(current_property, SpecialProperty):
            if current_property.special_type == "goto_jail":
                self.in_jail = True
                # 移动到监狱位置
                for i, prop in enumerate(board):
                    if isinstance(prop, SpecialProperty) and prop.special_type == "jail":
                        self.position = i
                        break
            elif current_property.special_type == "tax":
                # 支付税款
                if self.money >= 200:
                    self.money -= 200
                else:
                    # 如果钱不够，就支付所有剩余资金
                    self.money = 0
        
    def buy_property(self, property):
        if self.money >= property.price and property.owner is None:
            self.money -= property.price
            property.owner = self
            self.properties.append(property)
            return True
        return False
        
    def pay_rent(self, property, opponent):
        rent = property.rent
        if self.money >= rent:
            self.money -= rent
            opponent.money += rent
            return True
        return False
        
    def draw(self, surface):
        # 绘制玩家
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius, 2)
        
        # 绘制玩家名称首字母
        font = pygame.font.SysFont("simhei", 16)
        name_text = font.render(self.name[0], True, BLACK)
        text_rect = name_text.get_rect(center=(self.x, self.y))
        surface.blit(name_text, text_rect)
        
        # 如果在监狱，绘制标记
        if self.in_jail:
            pygame.draw.line(surface, RED, (self.x-10, self.y-10), (self.x+10, self.y+10), 3)
            pygame.draw.line(surface, RED, (self.x-10, self.y+10), (self.x+10, self.y-10), 3)

def create_board():
    # 创建地产列表
    board = []
    
    # 上边 - 从右到左 (增加地产数量)
    board.append(SpecialProperty("起点", 0, 0, LIGHT_BLUE, 800, 0, 80, 100, "start"))
    board.append(Property("广州", 60, 20, BROWN, 720, 0, 80, 100))
    board.append(Property("深圳", 80, 30, BROWN, 640, 0, 80, 100))
    board.append(SpecialProperty("社区基金", 0, 0, GRAY, 560, 0, 80, 100, "parking"))
    board.append(Property("上海", 100, 40, LIGHT_BLUE, 480, 0, 80, 100))
    board.append(Property("杭州", 100, 40, LIGHT_BLUE, 400, 0, 80, 100))
    board.append(Property("苏州", 120, 50, LIGHT_BLUE, 320, 0, 80, 100))
    board.append(SpecialProperty("所得税", 200, 0, GRAY, 240, 0, 80, 100, "tax"))
    board.append(Property("南京", 140, 60, PURPLE, 160, 0, 80, 100))
    board.append(Property("无锡", 140, 60, PURPLE, 80, 0, 80, 100))
    board.append(Property("合肥", 160, 70, PURPLE, 0, 0, 80, 100))
    
    # 左边 - 从上到下
    board.append(Property("武汉", 160, 70, ORANGE, 0, 100, 80, 100))
    board.append(Property("长沙", 180, 80, ORANGE, 0, 200, 80, 100))
    board.append(Property("郑州", 180, 80, ORANGE, 0, 300, 80, 100))
    board.append(Property("电力公司", 150, 70, WHITE, 0, 400, 80, 100))
    board.append(Property("石家庄", 200, 90, RED, 0, 500, 80, 100))
    board.append(Property("天津", 200, 90, RED, 0, 600, 80, 100))
    
    # 下边 - 从左到右
    board.append(SpecialProperty("监狱", 0, 0, RED, 80, 600, 80, 100, "jail"))
    board.append(Property("济南", 220, 100, YELLOW, 160, 600, 80, 100))
    board.append(Property("青岛", 220, 100, YELLOW, 240, 600, 80, 100))
    board.append(Property("太原", 240, 110, YELLOW, 320, 600, 80, 100))
    board.append(Property("自来水公司", 150, 70, WHITE, 400, 600, 80, 100))
    board.append(Property("沈阳", 240, 110, GREEN, 480, 600, 80, 100))
    board.append(Property("长春", 260, 120, GREEN, 560, 600, 80, 100))
    board.append(Property("哈尔滨", 260, 120, GREEN, 640, 600, 80, 100))
    board.append(Property("大连", 280, 130, DARK_GREEN, 720, 600, 80, 100))
    board.append(Property("西安", 280, 130, DARK_GREEN, 800, 600, 80, 100))
    board.append(Property("成都", 300, 140, DARK_GREEN, 880, 600, 80, 100))
    
    # 右边 - 从下到上
    board.append(Property("重庆", 300, 140, PINK, 920, 500, 80, 100))
    board.append(Property("昆明", 320, 150, PINK, 920, 400, 80, 100))
    board.append(Property("贵阳", 320, 150, PINK, 920, 300, 80, 100))
    board.append(Property("邮电公司", 150, 70, WHITE, 920, 200, 80, 100))
    board.append(Property("福州", 350, 160, BLUE, 920, 100, 80, 100))
    board.append(SpecialProperty("入狱", 0, 0, RED, 920, 0, 80, 100, "goto_jail"))
    
    return board

def update_player_positions(players, board):
    # 根据玩家在地产列表中的位置更新玩家坐标
    # 总共34个地产位置 (0-33)
    for player in players:
        pos = player.position
        if 0 <= pos <= 10:  # 上边 (0-10) - 11个位置
            x = 840 - pos * 80
            player.x, player.y = x, 50
        elif 11 <= pos <= 16:  # 左边 (11-16) - 6个位置
            y = 150 + (pos - 11) * 100
            player.x, player.y = 40, y
        elif 17 <= pos <= 27:  # 下边 (17-27) - 11个位置
            x = 120 + (pos - 17) * 80
            player.x, player.y = x, 650
        elif 28 <= pos <= 33:  # 右边 (28-33) - 6个位置
            y = 550 - (pos - 28) * 100
            player.x, player.y = 960, y

def draw_dice(surface, dice_value, x, y):
    # 绘制骰子
    pygame.draw.rect(surface, WHITE, (x, y, 50, 50))
    pygame.draw.rect(surface, BLACK, (x, y, 50, 50), 2)
    
    # 绘制点数
    font = pygame.font.SysFont("simhei", 30)
    dice_text = font.render(str(dice_value), True, BLACK)
    text_rect = dice_text.get_rect(center=(x + 25, y + 25))
    surface.blit(dice_text, text_rect)

def main():
    # 创建游戏对象
    board = create_board()
    players = [
        Player("玩家1", RED, 840, 50),
        Player("玩家2", BLUE, 840, 50),
        Player("玩家3", GREEN, 840, 50),
        Player("玩家4", YELLOW, 840, 50)
    ]
    
    # 确保所有玩家位置略微错开
    for i, player in enumerate(players):
        player.x += i * 5
        player.y += i * 5
    
    current_player = 0
    dice_value = 0
    game_state = "waiting"  # waiting, rolling, moving, buying, ended
    message = "玩家1的回合 - 按空格键掷骰子"
    font = pygame.font.SysFont("simhei", 24)
    small_font = pygame.font.SysFont("simhei", 18)
    large_font = pygame.font.SysFont("simhei", 28)  # 更大的字体用于玩家信息
    
    # 游戏主循环
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == "waiting":
                    # 掷骰子
                    dice_value = random.randint(1, 6)
                    game_state = "rolling"
                    message = f"掷出 {dice_value} 点"
                    
                elif event.key == pygame.K_RETURN and game_state == "rolling":
                    # 移动玩家
                    players[current_player].move(dice_value, board)
                    update_player_positions(players, board)
                    game_state = "moving"
                    
                    # 检查是否可以购买地产或支付租金
                    current_property = board[players[current_player].position]
                    if isinstance(current_property, Property) and not current_property.is_special:
                        if current_property.owner is None:
                            message = f"是否购买 {current_property.name}? 价格: ¥{current_property.price} (Y/N)"
                            game_state = "buying"
                        elif current_property.owner != players[current_player]:
                            # 支付租金
                            can_pay = players[current_player].pay_rent(current_property, current_property.owner)
                            if can_pay:
                                message = f"支付 ¥{current_property.rent} 租金给 {current_property.owner.name}"
                            else:
                                message = f"{players[current_player].name} 破产!"
                                # 移除破产玩家
                                for prop in players[current_player].properties:
                                    prop.owner = None
                                players[current_player].properties = []
                                
                            # 切换到下一个玩家
                            current_player = (current_player + 1) % len(players)
                            message = f"{players[current_player].name} 的回合 - 按空格键掷骰子"
                            game_state = "waiting"
                        else:
                            # 自己的地产，直接切换到下一个玩家
                            current_player = (current_player + 1) % len(players)
                            message = f"{players[current_player].name} 的回合 - 按空格键掷骰子"
                            game_state = "waiting"
                    else:
                        # 特殊地块或税款，直接切换到下一个玩家
                        current_player = (current_player + 1) % len(players)
                        message = f"{players[current_player].name} 的回合 - 按空格键掷骰子"
                        game_state = "waiting"
                            
                elif event.key == pygame.K_y and game_state == "buying":
                    # 购买地产
                    current_property = board[players[current_player].position]
                    if players[current_player].buy_property(current_property):
                        message = f"成功购买 {current_property.name}!"
                    else:
                        message = "资金不足，无法购买"
                        
                    # 切换到下一个玩家
                    current_player = (current_player + 1) % len(players)
                    message += f" {players[current_player].name} 的回合 - 按空格键掷骰子"
                    game_state = "waiting"
                    
                elif event.key == pygame.K_n and game_state == "buying":
                    # 放弃购买
                    message = "放弃购买"
                    # 切换到下一个玩家
                    current_player = (current_player + 1) % len(players)
                    message += f" {players[current_player].name} 的回合 - 按空格键掷骰子"
                    game_state = "waiting"
        
        # 绘制游戏
        screen.fill(WHITE)
        
        # 绘制地产
        for property in board:
            property.draw(screen)
        
        # 绘制玩家
        for player in players:
            player.draw(screen)
        
        # 绘制骰子
        draw_dice(screen, dice_value, WIDTH - 100, 50)
        
        # 绘制玩家信息（改进显示效果）
        pygame.draw.rect(screen, GRAY, (WIDTH - 250, 100, 230, 200), 0, 10)  # 背景框
        pygame.draw.rect(screen, BLACK, (WIDTH - 250, 100, 230, 200), 2, 10)  # 边框
        
        title_text = large_font.render("玩家状态", True, BLACK)
        screen.blit(title_text, (WIDTH - 240, 110))
        
        for i, player in enumerate(players):
            # 玩家名称
            name_text = small_font.render(player.name, True, player.color)
            screen.blit(name_text, (WIDTH - 240, 150 + i * 40))
            
            # 玩家资金（使用更大的字体）
            money_text = large_font.render(f"¥{player.money}", True, BLACK)
            screen.blit(money_text, (WIDTH - 150, 150 + i * 40))
            
            # 如果在监狱
            if player.in_jail:
                jail_text = small_font.render("(在监狱)", True, RED)
                screen.blit(jail_text, (WIDTH - 80, 150 + i * 40))
        
        # 绘制当前地产信息
        current_property = board[players[current_player].position]
        if isinstance(current_property, Property):
            property_info = f"当前位置: {current_property.name}"
            info_text = small_font.render(property_info, True, BLACK)
            screen.blit(info_text, (50, HEIGHT - 100))
            
            if current_property.owner:
                owner_info = f"所有者: {current_property.owner.name}"
                owner_text = small_font.render(owner_info, True, current_property.owner.color)
                screen.blit(owner_text, (50, HEIGHT - 70))
            else:
                price_info = f"价格: ¥{current_property.price}"
                price_text = small_font.render(price_info, True, BLACK)
                screen.blit(price_text, (50, HEIGHT - 70))
        
        # 绘制游戏信息
        message_text = font.render(message, True, BLACK)
        screen.blit(message_text, (50, HEIGHT - 40))
        
        # 绘制操作提示
        if game_state == "waiting":
            hint_text = small_font.render("按空格键掷骰子", True, BLACK)
            screen.blit(hint_text, (WIDTH - 200, HEIGHT - 40))
        elif game_state == "rolling":
            hint_text = small_font.render("按回车键移动", True, BLACK)
            screen.blit(hint_text, (WIDTH - 200, HEIGHT - 40))
        elif game_state == "buying":
            hint_text = small_font.render("按 Y 购买, N 放弃", True, BLACK)
            screen.blit(hint_text, (WIDTH - 200, HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()