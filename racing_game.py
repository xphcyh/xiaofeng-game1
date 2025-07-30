import tkinter 
import random
import time

WIDTH, HEIGHT = 400, 600
CAR_WIDTH, CAR_HEIGHT = 40, 60
LANES = [80, 180, 280]
INIT_SPEED = 10
OBSTACLE_COLOR = 'red'
COIN_COLOR = 'gold'
ITEM_COLOR = 'green'
BORDER_COLOR = 'white'
BG_COLOR = '#222244'
SKINS = {'蓝色': 'blue', '红色': 'red', '绿色': 'green', '黄色': 'yellow'}

class Game:
    def __init__(self, root, car_color):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack()
        # 赛道边界
        self.canvas.create_rectangle(60, 0, 340, HEIGHT, outline=BORDER_COLOR, width=6)
        self.car = self.canvas.create_rectangle(180, 500, 180+CAR_WIDTH, 500+CAR_HEIGHT, fill=car_color)
        self.obstacles = []
        self.coins = []
        self.items = []
        self.score = 0
        self.coins_collected = 0
        self.item_active = False
        self.item_timer = 0
        self.running = True
        self.speed = INIT_SPEED
        self.start_time = time.time()
        self.elapsed_time = 0
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        self.spawn_obstacle()
        self.spawn_coin()
        self.spawn_item()
        self.update()

    def move_left(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.car)
        for lane in reversed(LANES):
            if x1 > lane:
                self.canvas.coords(self.car, lane, y1, lane+CAR_WIDTH, y2)
                break

    def move_right(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.car)
        for lane in LANES:
            if x1 < lane:
                self.canvas.coords(self.car, lane, y1, lane+CAR_WIDTH, y2)
                break

    def spawn_obstacle(self):
        lane = random.choice(LANES)
        obs = self.canvas.create_rectangle(lane, 0, lane+CAR_WIDTH, CAR_HEIGHT, fill=OBSTACLE_COLOR)
        self.obstacles.append(obs)

    def spawn_coin(self):
        lane = random.choice(LANES)
        coin = self.canvas.create_oval(lane+10, 10, lane+CAR_WIDTH-10, CAR_HEIGHT-10, fill=COIN_COLOR)
        self.coins.append(coin)

    def spawn_item(self):
        # 随机生成道具（加速或无敌）
        if random.random() < 0.3:
            lane = random.choice(LANES)
            item = self.canvas.create_oval(lane+5, 5, lane+CAR_WIDTH-5, CAR_HEIGHT-5, fill=ITEM_COLOR)
            self.items.append(item)

    def update(self):
        if not self.running:
            return
        # 难度提升
        self.speed = INIT_SPEED + self.score // 10
        # 计时
        self.elapsed_time = int(time.time() - self.start_time)
        # 障碍物移动
        for obs in self.obstacles[:]:
            self.canvas.move(obs, 0, self.speed)
            x1, y1, x2, y2 = self.canvas.coords(obs)
            if y2 > HEIGHT:
                self.canvas.delete(obs)
                self.obstacles.remove(obs)
                self.score += 1
                self.spawn_obstacle()
            # 碰撞检测
            cx1, cy1, cx2, cy2 = self.canvas.coords(self.car)
            if x1 < cx2 and x2 > cx1 and y2 > cy1 and y1 < cy2:
                if not self.item_active:
                    self.running = False
                    self.show_game_over()
        # 金币移动
        for coin in self.coins[:]:
            self.canvas.move(coin, 0, self.speed)
            x1, y1, x2, y2 = self.canvas.coords(coin)
            if y2 > HEIGHT:
                self.canvas.delete(coin)
                self.coins.remove(coin)
                self.spawn_coin()
            # 吃金币
            cx1, cy1, cx2, cy2 = self.canvas.coords(self.car)
            if x1 < cx2 and x2 > cx1 and y2 > cy1 and y1 < cy2:
                self.canvas.delete(coin)
                self.coins.remove(coin)
                self.coins_collected += 1
                self.spawn_coin()
        # 道具移动
        for item in self.items[:]:
            self.canvas.move(item, 0, self.speed)
            x1, y1, x2, y2 = self.canvas.coords(item)
            if y2 > HEIGHT:
                self.canvas.delete(item)
                self.items.remove(item)
                self.spawn_item()
            # 吃道具
            cx1, cy1, cx2, cy2 = self.canvas.coords(self.car)
            if x1 < cx2 and x2 > cx1 and y2 > cy1 and y1 < cy2:
                self.canvas.delete(item)
                self.items.remove(item)
                self.item_active = True
                self.item_timer = 100  # 道具持续时间
        # 道具效果
        if self.item_active:
            self.item_timer -= 1
            self.canvas.itemconfig(self.car, outline='green', width=4)
            if self.item_timer <= 0:
                self.item_active = False
                self.canvas.itemconfig(self.car, outline='', width=1)
        # 信息显示
        self.canvas.delete('score')
        self.canvas.create_text(60, 20, text=f'得分: {self.score}', fill='white', font=('Arial', 16), tag='score')
        self.canvas.create_text(60, 45, text=f'金币: {self.coins_collected}', fill='gold', font=('Arial', 14), tag='score')
        self.canvas.create_text(60, 70, text=f'时间: {self.elapsed_time}s', fill='cyan', font=('Arial', 14), tag='score')
        if self.running:
            self.root.after(30, self.update)

    def show_game_over(self):
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text=f'游戏结束! 得分:{self.score} 金币:{self.coins_collected} 时间:{self.elapsed_time}s', font=('Arial', 18), fill='yellow')
        # 简单排行榜（本地）
        try:
            with open('racing_rank.txt', 'a') as f:
                f.write(f'{self.score},{self.coins_collected},{self.elapsed_time}\n')
        except Exception:
            pass
        self.show_rank()

    def show_rank(self):
        try:
            with open('racing_rank.txt', 'r') as f:
                records = [line.strip().split(',') for line in f if line.strip()]
            records.sort(key=lambda x: (int(x[0]), int(x[1]), int(x[2])), reverse=True)
            rank_text = '排行榜:\n'
            for i, rec in enumerate(records[:5]):
                rank_text += f'{i+1}. 得分:{rec[0]} 金币:{rec[1]} 时间:{rec[2]}s\n'
            self.canvas.create_text(WIDTH//2, HEIGHT//2+60, text=rank_text, font=('Arial', 14), fill='white')
        except Exception:
            pass

def choose_skin():
    def start_game():
        color = SKINS[var.get()]
        skin_win.destroy()
        root = tk.Tk()
        root.title('赛车小游戏')
        Game(root, color)
        root.mainloop()
    skin_win = tk.Tk()
    skin_win.title('选择赛车皮肤')
    tk.Label(skin_win, text='请选择赛车颜色:', font=('Arial', 16)).pack(pady=10)
    var = tk.StringVar(value='蓝色')
    for name in SKINS:
        tk.Radiobutton(skin_win, text=name, variable=var, value=name, font=('Arial', 14)).pack(anchor='w')
    tk.Button(skin_win, text='开始游戏', command=start_game, font=('Arial', 14)).pack(pady=10)
    skin_win.mainloop()

if __name__ == '__main__':
    choose_skin()