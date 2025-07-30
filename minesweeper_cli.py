import random

ROWS, COLS, MINES = 9, 9, 10

def place_mines():
    mines = set()
    while len(mines) < MINES:
        x, y = random.randint(0, ROWS-1), random.randint(0, COLS-1)
        mines.add((x, y))
    return mines

def count_mines(board, x, y):
    return sum((nx, ny) in board['mines']
               for nx in range(x-1, x+2)
               for ny in range(y-1, y+2)
               if 0 <= nx < ROWS and 0 <= ny < COLS and (nx, ny) != (x, y))

def show_board(board, reveal=False):
    print('   ' + ' '.join(str(i) for i in range(COLS)))
    for x in range(ROWS):
        row = []
        for y in range(COLS):
            if (x, y) in board['opened']:
                if (x, y) in board['mines']:
                    row.append('X')
                else:
                    m = count_mines(board, x, y)
                    row.append(str(m) if m else '.')
            elif (x, y) in board['flags']:
                row.append('F')
            elif reveal and (x, y) in board['mines']:
                row.append('X')
            else:
                row.append('#')
        print(f'{x:2} ' + ' '.join(row))

def open_cell(board, x, y):
    if (x, y) in board['opened'] or (x, y) in board['flags']:
        return
    board['opened'].add((x, y))
    if (x, y) in board['mines']:
        board['game_over'] = True
        return
    m = count_mines(board, x, y)
    if m == 0:
        for nx in range(x-1, x+2):
            for ny in range(y-1, y+2):
                if 0 <= nx < ROWS and 0 <= ny < COLS:
                    open_cell(board, nx, ny)

def check_win(board):
    return all((x, y) in board['opened'] or (x, y) in board['mines']
               for x in range(ROWS) for y in range(COLS))

def main():
    board = {
        'mines': place_mines(),
        'opened': set(),
        'flags': set(),
        'game_over': False
    }
    while True:
        show_board(board)
        if board['game_over']:
            print('游戏失败！')
            show_board(board, reveal=True)
            break
        if check_win(board):
            print('恭喜你，胜利！')
            show_board(board, reveal=True)
            break
        cmd = input('输入操作（o x y 开格，f x y 插旗）：').strip().split()
        if len(cmd) != 3: continue
        op, x, y = cmd[0], int(cmd[1]), int(cmd[2])
        if not (0 <= x < ROWS and 0 <= y < COLS): continue
        if op == 'o':
            open_cell(board, x, y)
        elif op == 'f':
            if (x, y) in board['flags']:
                board['flags'].remove((x, y))
            else:
                board['flags'].add((x, y))

if __name__ == '__main__':
    main()
