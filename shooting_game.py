import tkinter as tk
import random

WIDTH, HEIGHT = 500, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 40
BULLET_WIDTH, BULLET_HEIGHT = 6, 16
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 40
ENEMY_SPEED = 5
BULLET_SPEED = 15

class ShootingGame:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack()
        self.player_count = 5
        self.player_spacing = (WIDTH - self.player_count * PLAYER_WIDTH) // (self.player_count + 1)
        self.players = []
        for i in range(self.player_count):
            x = self.player_spacing + i * (PLAYER_WIDTH + self.player_spacing)
            y = HEIGHT - PLAYER_HEIGHT - 10
            player_rect = self.canvas.create_rectangle(x, y, x+PLAYER_WIDTH, y+PLAYER_HEIGHT, fill='green')
            self.players.append(player_rect)
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.running = True
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        self.root.bind('<space>', self.shoot)
        self.spawn_enemy()
        self.update()
    def move_left(self, event):
        for player in self.players:
            x1, y1, x2, y2 = self.canvas.coords(player)
            if x1 > 0:
                self.canvas.move(player, -40, 0)
    def move_right(self, event):
        for player in self.players:
            x1, y1, x2, y2 = self.canvas.coords(player)
            if x2 < WIDTH:
                self.canvas.move(player, 40, 0)
    def shoot(self, event):
        for player in self.players:
            x1, y1, x2, y2 = self.canvas.coords(player)
            bullet = self.canvas.create_rectangle((x1+x2)//2-BULLET_WIDTH//2, y1-BULLET_HEIGHT,
                                                 (x1+x2)//2+BULLET_WIDTH//2, y1, fill='yellow')
            self.bullets.append(bullet)
    def spawn_enemy(self):
        x = random.randint(0, WIDTH-ENEMY_WIDTH)
        enemy = self.canvas.create_rectangle(x, 0, x+ENEMY_WIDTH, ENEMY_HEIGHT, fill='red')
        self.enemies.append(enemy)
    def update(self):
        if not self.running:
            return
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, -BULLET_SPEED)
            _, y1, _, y2 = self.canvas.coords(bullet)
            if y2 < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
        for enemy in self.enemies[:]:
            self.canvas.move(enemy, 0, ENEMY_SPEED)
            _, y1, _, y2 = self.canvas.coords(enemy)
            if y1 > HEIGHT:
                self.canvas.delete(enemy)
                self.enemies.remove(enemy)
                self.game_over()
        self.check_collision()
        if random.randint(1, 30) == 1:
            self.spawn_enemy()
        self.root.after(50, self.update)
    def check_collision(self):
        for bullet in self.bullets[:]:
            bx1, by1, bx2, by2 = self.canvas.coords(bullet)
            for enemy in self.enemies[:]:
                ex1, ey1, ex2, ey2 = self.canvas.coords(enemy)
                if bx1 < ex2 and bx2 > ex1 and by1 < ey2 and by2 > ey1:
                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)
                    self.canvas.delete(enemy)
                    self.enemies.remove(enemy)
                    self.score += 1
        self.canvas.delete('score')
        self.canvas.create_text(60, 20, text=f'得分: {self.score}', fill='white', font=('Arial', 16), tag='score')
    def game_over(self):
        self.running = False
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text=f'游戏结束! 得分:{self.score}', font=('Arial', 24), fill='yellow')

def main():
    root = tk.Tk()
    root.title('枪战小游戏')
    ShootingGame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
