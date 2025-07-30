import pgzrun

WIDTH = 600
HEIGHT = 600
GRID_SIZE = 15
CELL_SIZE = WIDTH // GRID_SIZE

board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = 1  # 1: 黑子, 2: 白子
winner = 0

def draw():
    screen.fill((128,128,128))
    # 画棋盘格
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (x + y) % 2 == 0:
                screen.draw.filled_rect(Rect((x*CELL_SIZE, y*CELL_SIZE), (CELL_SIZE, CELL_SIZE)), (240,240,240))
    # 画棋盘线（让线条正好在格子边界上）
    for i in range(GRID_SIZE+1):
        # 横线.,m.m ..ijjil;;./?
        screen.draw.line((0, i*CELL_SIZE), (WIDTH, i*CELL_SIZE), 'black')
        # 竖线
        screen.draw.line((i*CELL_SIZE, 0), (i*CELL_SIZE, HEIGHT), 'black')
    # 画棋子
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] == 1:
                screen.draw.filled_circle((x*CELL_SIZE+CELL_SIZE//2, y*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//2-2, 'black')
            elif board[y][x] == 2:
                screen.draw.filled_circle((x*CELL_SIZE+CELL_SIZE//2, y*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//2-2, 'green')
    # 显示胜负
    if winner:
        msg = '黑子胜利!' if winner == 1 else '白子胜利!'
        screen.draw.text(msg, center=(WIDTH//2, 30), fontsize=40, color='red', fontname="simhei.ttf")

def on_mouse_down(pos):
    global current_player, winner
    if winner:
        return
    x = (pos[0] - CELL_SIZE//2) // CELL_SIZE
    y = (pos[1] - CELL_SIZE//2) // CELL_SIZE
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and board[y][x] == 0:
        board[y][x] = current_player
        if check_win(x, y, current_player):
            winner = current_player
        else:
            current_player = 2 if current_player == 1 else 1

def check_win(x, y, player):
    directions = [(1,0), (0,1), (1,1), (1,-1)]
    for dx, dy in directions:
        count = 1
        for d in [1, -1]:
            nx, ny = x, y
            while True:
                nx += dx * d
                ny += dy * d
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and board[ny][nx] == player:
                    count += 1
                else:
                    break
        if count >= 5:
            return True
    return False

pgzrun.go()
