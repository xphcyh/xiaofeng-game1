import tkinter as tk
import random

WIDTH, HEIGHT = 500, 500
PLAYER_SIZE = 40
HIDER_SIZE = 40
MOVE_STEP = 20

class HideAndSeekGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='lightgreen')
        self.canvas.pack()
        self.player = self.canvas.create_rectangle(20, 20, 20+PLAYER_SIZE, 20+PLAYER_SIZE, fill='blue')
        self.hider = self.canvas.create_rectangle(WIDTH-60, HEIGHT-60, WIDTH-60+HIDER_SIZE, HEIGHT-60+HIDER_SIZE, fill='orange')
        self.found = False
        self.root.bind('<Up>', self.move_up)
        self.root.bind('<Down>', self.move_down)
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        self.canvas.create_text(WIDTH//2, 20, text='用方向键移动，找到橙色小人！', font=('Arial', 14), fill='black', tag='tip')
    def move_up(self, event):
        if self.found: return
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        if y1 > 0:
            self.canvas.move(self.player, 0, -MOVE_STEP)
        self.check_found()
    def move_down(self, event):
        if self.found: return
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        if y2 < HEIGHT:
            self.canvas.move(self.player, 0, MOVE_STEP)
        self.check_found()
    def move_left(self, event):
        if self.found: return
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        if x1 > 0:
            self.canvas.move(self.player, -MOVE_STEP, 0)
        self.check_found()
    def move_right(self, event):
        if self.found: return
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        if x2 < WIDTH:
            self.canvas.move(self.player, MOVE_STEP, 0)
        self.check_found()
    def check_found(self):
        px1, py1, px2, py2 = self.canvas.coords(self.player)
        hx1, hy1, hx2, hy2 = self.canvas.coords(self.hider)
        if px1 < hx2 and px2 > hx1 and py1 < hy2 and py2 > hy1:
            self.found = True
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text='你找到小伙伴啦！', font=('Arial', 24), fill='red')

def main():
    root = tk.Tk()
    root.title('躲猫猫小游戏')
    HideAndSeekGame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
