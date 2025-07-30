 import tkinter as tk

WIDTH, HEIGHT = 800, 500
PLAYER_SIZE = 40
MOVE_STEP = 20
ATTACK_RANGE = 60
JUMP_HEIGHT = 80

class SmashGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='lightblue')
        self.canvas.pack()
        # 多角色：马里奥、皮卡丘、路易吉、库巴
        self.chars = [
            {'name': '马里奥', 'color': 'red', 'x': 100, 'y': HEIGHT-PLAYER_SIZE-20, 'hp': 10, 'keyset': {'up':'w','down':'s','left':'a','right':'d','atk':'j','jump':'k'}},
            {'name': '皮卡丘', 'color': 'yellow', 'x': 300, 'y': HEIGHT-PLAYER_SIZE-20, 'hp': 10, 'keyset': {'up':'i','down':'k','left':'j','right':'l','atk':'u','jump':'o'}},
            {'name': '路易吉', 'color': 'green', 'x': 500, 'y': HEIGHT-PLAYER_SIZE-20, 'hp': 10, 'keyset': {'up':'t','down':'g','left':'f','right':'h','atk':'r','jump':'y'}},
            {'name': '库巴', 'color': 'orange', 'x': 700, 'y': HEIGHT-PLAYER_SIZE-20, 'hp': 10, 'keyset': {'up':'up','down':'down','left':'left','right':'right','atk':'m','jump':'n'}}
        ]
        self.players = []
        for c in self.chars:
            rect = self.canvas.create_rectangle(c['x'], c['y'], c['x']+PLAYER_SIZE, c['y']+PLAYER_SIZE, fill=c['color'])
            c['rect'] = rect
            c['jumping'] = False
            c['jump_base'] = c['y']
            self.players.append(c)
        self.info = self.canvas.create_text(WIDTH//2, 30, text=self.get_info(), font=('Arial', 16), fill='black', tag='info')
        self.root.bind('<Key>', self.handle_key)
        self.update_info()
    def get_info(self):
        return ' | '.join([f"{c['name']}HP:{c['hp']}" for c in self.players]) + '  [WASD/IJKL/TFGH/方向键移动，J/U/R/M攻击，K/O/Y/N跳]'
    def handle_key(self, event):
        for c in self.players:
            k = event.keysym.lower()
            ks = c['keyset']
            if k == ks['left']:
                self.move(c, -MOVE_STEP, 0)
            elif k == ks['right']:
                self.move(c, MOVE_STEP, 0)
            elif k == ks['up']:
                self.move(c, 0, -MOVE_STEP)
            elif k == ks['down']:
                self.move(c, 0, MOVE_STEP)
            elif k == ks['atk']:
                self.attack(c)
            elif k == ks['jump']:
                self.jump(c)
    def move(self, c, dx, dy):
        x1, y1, x2, y2 = self.canvas.coords(c['rect'])
        nx1, ny1, nx2, ny2 = x1+dx, y1+dy, x2+dx, y2+dy
        if 0 <= nx1 < WIDTH and 0 <= nx2 <= WIDTH and 0 <= ny1 < HEIGHT and 0 <= ny2 <= HEIGHT:
            self.canvas.move(c['rect'], dx, dy)
            c['x'] += dx
            c['y'] += dy
            if not c['jumping']:
                c['jump_base'] = c['y']
        self.update_info()
    def attack(self, c):
        cx1, cy1, cx2, cy2 = self.canvas.coords(c['rect'])
        for other in self.players:
            if other is c or other['hp'] <= 0:
                continue
            ox1, oy1, ox2, oy2 = self.canvas.coords(other['rect'])
            if abs((cx1+cx2)//2 - (ox1+ox2)//2) < ATTACK_RANGE and abs((cy1+cy2)//2 - (oy1+oy2)//2) < ATTACK_RANGE:
                other['hp'] -= 1
                self.canvas.create_text((cx1+cx2)//2, cy1-20, text=f'{c["name"]}攻击!', font=('Arial', 12), fill=c['color'], tag='msg')
                self.root.after(400, lambda: self.canvas.delete('msg'))
                self.check_win()
        self.update_info()
    def jump(self, c):
        if c['jumping']: return
        c['jumping'] = True
        self._jump(c, -JUMP_HEIGHT//4, 0)
    def _jump(self, c, dy, step):
        if step < 4:
            self.move(c, 0, dy)
            self.root.after(50, lambda: self._jump(c, dy, step+1))
        elif step < 8:
            self.move(c, 0, -dy)
            self.root.after(50, lambda: self._jump(c, -dy, step+1))
        else:
            c['jumping'] = False
            self.move(c, 0, c['jump_base']-c['y'])
    def update_info(self):
        self.canvas.itemconfig(self.info, text=self.get_info())
    def check_win(self):
        alive = [c for c in self.players if c['hp'] > 0]
        if len(alive) == 1:
            winner = alive[0]['name']
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text=f'{winner}胜利！', font=('Arial', 32), fill='purple')
            self.root.unbind('<Key>')

def main():
    root = tk.Tk()
    root.title('简易大乱斗小游戏')
    SmashGame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
