import pgzrun
import random

# Game constants
WIDTH = 400
HEIGHT = 500
CELL_SIZE = 40
ROWS = 9
COLS = 9
MINES = 10

# Colors
BACKGROUND_COLOR = (200, 200, 200)
GRID_COLOR = (150, 150, 150)
CELL_COLOR = (100, 100, 200)
REVEALED_COLOR = (200, 200, 200)
TEXT_COLORS = {
    1: (0, 0, 255),      # Blue
    2: (0, 128, 0),      # Green
    3: (255, 0, 0),      # Red
    4: (75, 0, 130),     # Purple
    5: (139, 0, 0),      # Dark Red
    6: (0, 255, 255),    # Cyan
    7: (0, 0, 0),        # Black
    8: (128, 128, 128)   # Gray
}

# Game state
game_over = False
game_won = False

# Create the grid
grid = []
for row in range(ROWS):
    grid.append([])
    for col in range(COLS):
        grid[row].append({
            'is_mine': False,
            'is_revealed': False,
            'is_flagged': False,
            'neighbor_mines': 0,
            'x': col * CELL_SIZE + (WIDTH - COLS * CELL_SIZE) // 2,
            'y': row * CELL_SIZE + 100
        })

# Place mines randomly
def place_mines():
    mines_placed = 0
    while mines_placed < MINES:
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        if not grid[row][col]['is_mine']:
            grid[row][col]['is_mine'] = True
            mines_placed += 1

# Count neighboring mines for each cell
def count_neighbor_mines():
    for row in range(ROWS):
        for col in range(COLS):
            if not grid[row][col]['is_mine']:
                count = 0
                for i in range(max(0, row-1), min(ROWS, row+2)):
                    for j in range(max(0, col-1), min(COLS, col+2)):
                        if grid[i][j]['is_mine']:
                            count += 1
                grid[row][col]['neighbor_mines'] = count

# Reveal a cell
def reveal_cell(row, col):
    cell = grid[row][col]
    if cell['is_revealed'] or cell['is_flagged'] or game_over or game_won:
        return
    
    cell['is_revealed'] = True
    
    if cell['is_mine']:
        global game_over
        game_over = True
        reveal_all_mines()
        return
    
    # If cell has no neighboring mines, reveal neighbors
    if cell['neighbor_mines'] == 0:
        for i in range(max(0, row-1), min(ROWS, row+2)):
            for j in range(max(0, col-1), min(COLS, col+2)):
                if not grid[i][j]['is_revealed']:
                    reveal_cell(i, j)

# Reveal all mines when game is over
def reveal_all_mines():
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col]['is_mine']:
                grid[row][col]['is_revealed'] = True

# Flag a cell
def flag_cell(row, col):
    if grid[row][col]['is_revealed'] or game_over or game_won:
        return
    
    grid[row][col]['is_flagged'] = not grid[row][col]['is_flagged']

# Check if player has won
def check_win():
    global game_won
    for row in range(ROWS):
        for col in range(COLS):
            cell = grid[row][col]
            # If there's a non-mine cell that hasn't been revealed, player hasn't won yet
            if not cell['is_mine'] and not cell['is_revealed']:
                return
    
    game_won = True

# Draw the game
def draw():
    screen.clear()
    screen.fill(BACKGROUND_COLOR)
    
    # Draw title
    screen.draw.text("MINESWEEPER", center=(WIDTH//2, 30), fontsize=40, color="black")
    
    # Draw grid
    for row in range(ROWS):
        for col in range(COLS):
            cell = grid[row][col]
            x = cell['x']
            y = cell['y']
            
            # Draw cell background
            if cell['is_revealed']:
                color = REVEALED_COLOR
            else:
                color = CELL_COLOR
            
            screen.draw.filled_rect(Rect((x, y), (CELL_SIZE, CELL_SIZE)), color)
            screen.draw.rect(Rect((x, y), (CELL_SIZE, CELL_SIZE)), GRID_COLOR)
            
            # Draw cell content
            if cell['is_revealed']:
                if cell['is_mine']:
                    screen.draw.text("M", center=(x + CELL_SIZE//2, y + CELL_SIZE//2), 
                                   fontsize=20, color="black")
                elif cell['neighbor_mines'] > 0:
                    color = TEXT_COLORS.get(cell['neighbor_mines'], "black")
                    screen.draw.text(str(cell['neighbor_mines']), 
                                   center=(x + CELL_SIZE//2, y + CELL_SIZE//2),
                                   fontsize=20, color=color)
            elif cell['is_flagged']:
                screen.draw.text("F", center=(x + CELL_SIZE//2, y + CELL_SIZE//2), 
                               fontsize=20, color="red")
    
    # Draw game status
    if game_over:
        screen.draw.text("GAME OVER! Click to restart", center=(WIDTH//2, HEIGHT-30), 
                       fontsize=30, color="red")
    elif game_won:
        screen.draw.text("YOU WIN! Click to restart", center=(WIDTH//2, HEIGHT-30), 
                       fontsize=30, color="green")

# Handle mouse clicks
def on_mouse_down(pos, button):
    global game_over, game_won
    
    # Handle restart
    if game_over or game_won:
        restart_game()
        return
    
    # Check which cell was clicked
    for row in range(ROWS):
        for col in range(COLS):
            cell = grid[row][col]
            x = cell['x']
            y = cell['y']
            
            if x <= pos[0] <= x + CELL_SIZE and y <= pos[1] <= y + CELL_SIZE:
                if button == mouse.LEFT:
                    reveal_cell(row, col)
                    if not game_over:
                        check_win()
                elif button == mouse.RIGHT:
                    flag_cell(row, col)
                return

# Restart the game
def restart_game():
    global game_over, game_won
    
    # Reset game state
    game_over = False
    game_won = False
    
    # Reset grid122334567
    for row in range(ROWS):
        for col in range(COLS):
            grid[row][col] = {
                'is_mine': False,
                'is_revealed': False,
                'is_flagged': False,
                'neighbor_mines': 0,
                'x': col * CELL_SIZE + (WIDTH - COLS * CELL_SIZE) // 2,
                'y': row * CELL_SIZE + 100
            }
    
    # Place mines and count neighbors
    place_mines()
    count_neighbor_mines()

# Initialize the game
place_mines()
count_neighbor_mines()

pgzrun.go()