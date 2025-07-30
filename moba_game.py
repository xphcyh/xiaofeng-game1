import tkinter as tk
import random

WIDTH, HEIGHT = 800, 500
PLAYER_SIZE = 40
MOVE_STEP = 20
ATTACK_RANGE = 80
MAX_HP = 10
ENEMY_COUNT = 3

class MOBAHero:
    def __init__(self, canvas, name, color, x, y, keyset):
        self.canvas = canvas
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.hp = MAX_HP
        self.rect = canvas.create_rectangle(x, y, x+PLAYER_SIZE, y+PLAYER_SIZE, fill=color)
        self.keyset = keyset
        self.skill_cd = 0
    def move(self, dx, dy):
        nx, ny = self.x+dx, self.y+dy
        if 0 <= nx <= WIDTH-PLAYER_SIZE and 0 <= ny <= HEIGHT-PLAYER_SIZE:
            self.canvas.move(self.rect, dx, dy)
            self.x, self.y = nx, ny
    def attack(self, enemies):
        for e in enemies:
            if e.hp > 0 and abs((self.x+PLAYER_SIZE//2)-(e.x+PLAYER_SIZE//2)) < ATTACK_RANGE and abs((self.y+PLAYER_SIZE//2)-(e.y+PLAYER_SIZE//2)) < ATTACK_RANGE:
                e.hp -= 1
                self.canvas.create_text(self.x+PLAYER_SIZE//2, self.y-20, text=f'{self.name}攻击!', font=('Arial', 12), fill=self.color, tag='msg')
                self.canvas.after(400, lambda: self.canvas.delete('msg'))
    def skill(self, enemies):
        if self.skill_cd > 0: return
        for e in enemies:
            if e.hp > 0 and abs((self.x+PLAYER_SIZE//2)-(e.x+PLAYER_SIZE//2)) < ATTACK_RANGE*2 and abs((self.y+PLAYER_SIZE//2)-(e.y+PLAYER_SIZE//2)) < ATTACK_RANGE*2:
                e.hp -= 2
                self.canvas.create_text(self.x+PLAYER_SIZE//2, self.y-40, text=f'{self.name}技能!', font=('Arial', 12), fill='purple', tag='msg')
                self.canvas.after(400, lambda: self.canvas.delete('msg'))
        self.skill_cd = 10
    def update_cd(self):
        if self.skill_cd > 0:
            self.skill_cd -= 1

class MOBA:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='lightgreen')
        self.canvas.pack()
        self.hero = MOBAHero(self.canvas, '主角', 'blue', 100, HEIGHT//2, {'up':'w','down':'s','left':'a','right':'d','atk':'j','skill':'k'})
        self.enemies = []
        for i in range(ENEMY_COUNT):
            x = random.randint(400, WIDTH-PLAYER_SIZE)
            y = random.randint(50, HEIGHT-PLAYER_SIZE)
            color = random.choice(['red','orange','purple'])
            enemy = MOBAHero(self.canvas, f'敌人{i+1}', color, x, y, {})
            self.enemies.append(enemy)
        self.info = self.canvas.create_text(WIDTH//2, 30, text=self.get_info(), font=('Arial', 16), fill='black', tag='info')
        self.root.bind('<Key>', self.handle_key)
        self.update_info()
        self.update_cd_loop()
    def get_info(self):
        return f"主角HP:{self.hero.hp} 技能CD:{self.hero.skill_cd} | " + ' '.join([f"{e.name}HP:{e.hp}" for e in self.enemies]) + '  [WASD移动，J攻击，K技能]'
    def handle_key(self, event):
        k = event.keysym.lower()
        ks = self.hero.keyset
        if k == ks['left']:
            self.hero.move(-MOVE_STEP, 0)
        elif k == ks['right']:
            self.hero.move(MOVE_STEP, 0)
        elif k == ks['up']:
            self.hero.move(0, -MOVE_STEP)
        elif k == ks['down']:
            self.hero.move(0, MOVE_STEP)
        elif k == ks['atk']:
            self.hero.attack(self.enemies)
        elif k == ks['skill']:
            self.hero.skill(self.enemies)
        self.update_info()
        self.check_win()
    def update_info(self):
        self.canvas.itemconfig(self.info, text=self.get_info())
    def update_cd_loop(self):
        self.hero.update_cd()
        self.root.after(500, self.update_cd_loop)
        self.update_info()
    def check_win(self):
        if self.hero.hp <= 0:
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text='你失败了！', font=('Arial', 32), fill='red')
            self.root.unbind('<Key>')
        elif all(e.hp <= 0 for e in self.enemies):
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text='你胜利了！', font=('Arial', 32), fill='blue')
            self.root.unbind('<Key>')

def main():
    root = tk.Tk()
    root.title('简易王者荣耀小游戏')
    MOBA(root)
    root.mainloop()

if __name__ == '__main__':
    main()
