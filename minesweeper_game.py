import ttkbootstrap as ttb
import random

ROWS, COLS, MINES = 9, 9, 10

# Configure style for Cell buttons
style = ttb.Style()
style.configure("Cell.TButton", font=("Arial", 10, "bold"))

class Cell(ttb.Button):
    def __init__(self, master, x, y):
        super().__init__(master, width=4, bootstyle="secondary-outline", style="Cell.TButton")
        self.x, self.y = x, y
        self.is_mine = False
        self.is_open = False
        self.is_flag = False
        self.bind('<Button-1>', self.left_click)
        self.bind('<Button-3>', self.right_click)
    def left_click(self, event=None):
        if self.is_flag or self.is_open or game_over[0]: return
        if self.is_mine:
            self.config(text='💣', bootstyle="danger")
            game_over[0] = True
            result.set('游戏失败！')
            show_mines()
        else:
            open_cell(self.x, self.y)
            check_win()
    def right_click(self, event=None):
        if self.is_open or game_over[0]: return
        self.is_flag = not self.is_flag
        self.config(text='🚩' if self.is_flag else '')

def place_mines():
    mines = set()
    while len(mines) < MINES:
        x, y = random.randint(0, ROWS-1), random.randint(0, COLS-1)
        mines.add((x, y))
    for x, y in mines:
        cells[x][y].is_mine = True

def count_mines(x, y):
    return sum(0 <= nx < ROWS and 0 <= ny < COLS and cells[nx][ny].is_mine
               for nx in range(x-1, x+2) for ny in range(y-1, y+2) if (nx, ny) != (x, y))

def open_cell(x, y):
    cell = cells[x][y]
    if cell.is_open or cell.is_flag: return
    cell.is_open = True
    mines_around = count_mines(x, y)
    cell.config(bootstyle="light", relief='sunken')
    if mines_around:
        # Add color coding for numbers
        colors = ['', 'blue', 'green', 'red', 'purple', 'maroon', 'cyan', 'black', 'gray']
        cell.config(text=str(mines_around), foreground=colors[mines_around] if mines_around < len(colors) else 'black')
    else:
        for nx in range(x-1, x+2):
            for ny in range(y-1, y+2):
                if 0 <= nx < ROWS and 0 <= ny < COLS:
                    open_cell(nx, ny)

def show_mines():
    for row in cells:
        for cell in row:
            if cell.is_mine:
                cell.config(text='💣', bootstyle="danger")

def check_win():
    for row in cells:
        for cell in row:
            if not cell.is_mine and not cell.is_open:
                return
    result.set('恭喜你，胜利！')
    game_over[0] = True

def restart():
    global cells, game_over
    for widget in frame.winfo_children():
        widget.destroy()
    cells = [[Cell(frame, x, y) for y in range(COLS)] for x in range(ROWS)]
    for x in range(ROWS):
        for y in range(COLS):
            cells[x][y].grid(row=x, column=y, padx=1, pady=1)
    place_mines()
    result.set('')
    game_over[0] = False

root = ttb.Window()
root.title('扫雷游戏')

frame = ttb.Frame(root)
frame.pack()

result = ttb.StringVar()
ttb.Label(root, textvariable=result, font=("Arial", 16), foreground='blue').pack(pady=5)
ttb.Button(root, text='重新开始', command=restart).pack(pady=5)

cells = []
game_over = [False]
restart()
root.mainloop()
import random

ROWS, COLS, MINES = 9, 9, 10

class Cell(tk.Button):
    def __init__(self, master, x, y):
        super().__init__(master, width=2, height=1, font=("Arial", 14))
        self.x, self.y = x, y
        self.is_mine = False
        self.is_open = False
        self.is_flag = False
        self.bind('<Button-1>', self.left_click)
        self.bind('<Button-3>', self.right_click)
    def left_click(self, event=None):
        if self.is_flag or self.is_open or game_over[0]: return
        if self.is_mine:
            self.config(text='💣', bg='red')
            game_over[0] = True
            result.set('游戏失败！')
            show_mines()
        else:
            open_cell(self.x, self.y)
            check_win()
    def right_click(self, event=None):
        if self.is_open or game_over[0]: return
        self.is_flag = not self.is_flag
        self.config(text='🚩' if self.is_flag else '')

def place_mines():
    mines = set()
    while len(mines) < MINES:
        x, y = random.randint(0, ROWS-1), random.randint(0, COLS-1)
        mines.add((x, y))
    for x, y in mines:
        cells[x][y].is_mine = True

def count_mines(x, y):
    return sum(0 <= nx < ROWS and 0 <= ny < COLS and cells[nx][ny].is_mine
               for nx in range(x-1, x+2) for ny in range(y-1, y+2) if (nx, ny) != (x, y))

def open_cell(x, y):
    cell = cells[x][y]
    if cell.is_open or cell.is_flag: return
    cell.is_open = True
    mines_around = count_mines(x, y)
    cell.config(relief='sunken', bg='#ddd')
    if mines_around:
        cell.config(text=str(mines_around))
    else:
        for nx in range(x-1, x+2):
            for ny in range(y-1, y+2):
                if 0 <= nx < ROWS and 0 <= ny < COLS:
                    open_cell(nx, ny)

def show_mines():
    for row in cells:
        for cell in row:
            if cell.is_mine:
                cell.config(text='💣', bg='red')

def check_win():
    for row in cells:
        for cell in row:
            if not cell.is_mine and not cell.is_open:
                return
    result.set('恭喜你，胜利！')
    game_over[0] = True

def restart():
    global cells, game_over
    for widget in frame.winfo_children():
        widget.destroy()
    cells = [[Cell(frame, x, y) for y in range(COLS)] for x in range(ROWS)]
    for x in range(ROWS):
        for y in range(COLS):
            cells[x][y].grid(row=x, column=y)
    place_mines()
    result.set('')
    game_over[0] = False

root = tk.Tk()
root.title('扫雷游戏')

frame = tk.Frame(root)
frame.pack()

result = tk.StringVar()
tk.Label(root, textvariable=result, font=("Arial", 16), fg='blue').pack(pady=5)
tk.Button(root, text='重新开始', command=restart).pack(pady=5)

cells = []
game_over = [False]
restart()
root.mainloop()
