import tkinter as tk
import random

WIDTH, HEIGHT = 600, 400
PLAYER_SIZE = 40
ENEMY_SIZE = 40
MOVE_STEP = 20
ATTACK_RANGE = 50

class FightingGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='lightgray')
        self.canvas.pack()
        self.player = self.canvas.create_rectangle(100, HEIGHT//2-PLAYER_SIZE//2, 100+PLAYER_SIZE, HEIGHT//2+PLAYER_SIZE//2, fill='blue')
        self.enemy = self.canvas.create_rectangle(WIDTH-140, HEIGHT//2-ENEMY_SIZE//2, WIDTH-140+ENEMY_SIZE, HEIGHT//2+ENEMY_SIZE//2, fill='red')
        self.player_hp = 10
        self.enemy_hp = 10
        self.info = self.canvas.create_text(WIDTH//2, 30, text=self.get_info(), font=('Arial', 16), fill='black', tag='info')
        self.root.bind('<Up>', self.move_up)
        self.root.bind('<Down>', self.move_down)
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        self.root.bind('a', self.attack)
        self.root.bind('l', self.enemy_attack)
    def get_info(self):
        return f'玩家HP: {self.player_hp}  敌人HP: {self.enemy_hp}  [方向键移动，A攻击，L敌人攻击]'
    def move_up(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        if y1 > 0:
            self.canvas.move(self.player, 0, -MOVE_STEP)
        self.update_info()
    def move_down(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        if y2 < HEIGHT:
            self.canvas.move(self.player, 0, MOVE_STEP)
        self.update_info()
    def move_left(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        if x1 > 0:
            self.canvas.move(self.player, -MOVE_STEP, 0)
        self.update_info()
    def move_right(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        if x2 < WIDTH:
            self.canvas.move(self.player, MOVE_STEP, 0)
        self.update_info()
    def attack(self, event):
        px1, py1, px2, py2 = self.canvas.coords(self.player)
        ex1, ey1, ex2, ey2 = self.canvas.coords(self.enemy)
        if abs((px1+px2)//2 - (ex1+ex2)//2) < ATTACK_RANGE and abs((py1+py2)//2 - (ey1+ey2)//2) < ATTACK_RANGE:
            self.enemy_hp -= 1
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text='玩家攻击！', font=('Arial', 20), fill='blue', tag='msg')
            self.root.after(500, lambda: self.canvas.delete('msg'))
            self.check_win()
        self.update_info()
    def enemy_attack(self, event):
        px1, py1, px2, py2 = self.canvas.coords(self.player)
        ex1, ey1, ex2, ey2 = self.canvas.coords(self.enemy)
        if abs((px1+px2)//2 - (ex1+ex2)//2) < ATTACK_RANGE and abs((py1+py2)//2 - (ey1+ey2)//2) < ATTACK_RANGE:
            self.player_hp -= 1
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text='敌人攻击！', font=('Arial', 20), fill='red', tag='msg')
            self.root.after(500, lambda: self.canvas.delete('msg'))
            self.check_win()
        self.update_info()
    def update_info(self):
        self.canvas.itemconfig(self.info, text=self.get_info())
    def check_win(self):
        if self.enemy_hp <= 0:
            self.canvas.create_text(WIDTH//2, HEIGHT//2+40, text='玩家胜利！', font=('Arial', 24), fill='blue')
            self.root.unbind('<Up>'); self.root.unbind('<Down>'); self.root.unbind('<Left>'); self.root.unbind('<Right>'); self.root.unbind('a'); self.root.unbind('l')
        elif self.player_hp <= 0:
            self.canvas.create_text(WIDTH//2, HEIGHT//2+40, text='敌人胜利！', font=('Arial', 24), fill='red')
            self.root.unbind('<Up>'); self.root.unbind('<Down>'); self.root.unbind('<Left>'); self.root.unbind('<Right>'); self.root.unbind('a'); self.root.unbind('l')

def main():
    root = tk.Tk()
    root.title('格斗小游戏')
    FightingGame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
