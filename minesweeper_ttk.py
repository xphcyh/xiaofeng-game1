import ttkbootstrap as ttb
from ttkbootstrap.constants import *
import random

class MinesweeperGame:
    def __init__(self):
        # Game configuration
        self.rows = 9
        self.cols = 9
        self.mines = 10
        self.cells = []
        self.game_over = False
        self.first_click = True
        
        # Create main window
        self.root = ttb.Window(themename="litera")
        self.root.title("扫雷游戏")
        self.root.resizable(False, False)
        
        # Create style for cells
        self.style = ttb.Style()
        self.style.configure("Mine.TButton", font=("Arial", 10, "bold"), width=3)
        self.style.configure("Revealed.TButton", font=("Arial", 10, "bold"), width=3)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create top frame for controls
        top_frame = ttb.Frame(self.root)
        top_frame.pack(pady=10)
        
        # Create restart button
        self.restart_btn = ttb.Button(
            top_frame, 
            text="😊", 
            command=self.restart_game,
            style="Primary.TButton",
            width=3
        )
        self.restart_btn.pack()
        
        # Create mine count label
        self.mine_count_var = ttb.StringVar(value=f"💣: {self.mines}")
        mine_label = ttb.Label(
            top_frame, 
            textvariable=self.mine_count_var,
            font=("Arial", 12, "bold")
        )
        mine_label.pack(pady=5)
        
        # Create game status label
        self.status_var = ttb.StringVar(value="点击任意格子开始游戏")
        self.status_label = ttb.Label(
            top_frame,
            textvariable=self.status_var,
            font=("Arial", 10)
        )
        self.status_label.pack()
        
        # Create game frame
        self.game_frame = ttb.Frame(self.root)
        self.game_frame.pack(padx=10, pady=(0, 10))
        
        # Create cells
        self.create_cells()
        
    def create_cells(self):
        self.cells = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                cell = ttb.Button(
                    self.game_frame,
                    style="Mine.TButton",
                    command=lambda x=i, y=j: self.left_click(x, y)
                )
                cell.grid(row=i, column=j, padx=1, pady=1)
                cell.bind("<Button-3>", lambda e, x=i, y=j: self.right_click(x, y))
                
                # Add properties to cell
                cell.x = i
                cell.y = j
                cell.is_mine = False
                cell.is_revealed = False
                cell.is_flagged = False
                cell.adjacent_mines = 0
                
                row.append(cell)
            self.cells.append(row)
            
    def place_mines(self, first_x, first_y):
        """Place mines randomly, avoiding the first clicked cell and its neighbors"""
        # Generate all possible positions
        positions = [(i, j) for i in range(self.rows) for j in range(self.cols)]
        
        # Remove first clicked cell and its neighbors
        safe_positions = []
        for i in range(max(0, first_x-1), min(self.rows, first_x+2)):
            for j in range(max(0, first_y-1), min(self.cols, first_y+2)):
                safe_positions.append((i, j))
                
        for pos in safe_positions:
            if pos in positions:
                positions.remove(pos)
                
        # Randomly select mine positions
        mine_positions = random.sample(positions, self.mines)
        
        # Place mines
        for x, y in mine_positions:
            self.cells[x][y].is_mine = True
            
        # Calculate adjacent mines for each cell
        self.calculate_adjacent_mines()
        
    def calculate_adjacent_mines(self):
        """Calculate number of adjacent mines for each cell"""
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.cells[i][j].is_mine:
                    count = 0
                    for x in range(max(0, i-1), min(self.rows, i+2)):
                        for y in range(max(0, j-1), min(self.cols, j+2)):
                            if self.cells[x][y].is_mine:
                                count += 1
                    self.cells[i][j].adjacent_mines = count
                    
    def left_click(self, x, y):
        """Handle left click on a cell"""
        cell = self.cells[x][y]
        
        # Ignore if game is over, cell is flagged, or cell is already revealed
        if self.game_over or cell.is_flagged or cell.is_revealed:
            return
            
        # Place mines on first click
        if self.first_click:
            self.place_mines(x, y)
            self.first_click = False
            self.status_var.set("游戏进行中...")
            
        # Handle mine click
        if cell.is_mine:
            self.reveal_mines()
            cell.configure(text="💥", style="Danger.TButton")
            self.game_over = True
            self.status_var.set("游戏失败!")
            self.restart_btn.configure(text="😵")
            return
            
        # Reveal cell
        self.reveal_cell(x, y)
        
        # Check for win
        self.check_win()
        
    def right_click(self, x, y):
        """Handle right click on a cell (flag placement)"""
        cell = self.cells[x][y]
        
        # Ignore if game is over or cell is already revealed
        if self.game_over or cell.is_revealed:
            return
            
        # Toggle flag
        if not cell.is_flagged:
            cell.configure(text="🚩", style="Warning.TButton")
            cell.is_flagged = True
        else:
            cell.configure(text="", style="Mine.TButton")
            cell.is_flagged = False
            
    def reveal_cell(self, x, y):
        """Reveal a cell and adjacent cells if no adjacent mines"""
        cell = self.cells[x][y]
        
        # Ignore if cell is already revealed or flagged
        if cell.is_revealed or cell.is_flagged:
            return
            
        # Mark as revealed
        cell.is_revealed = True
        
        # Update appearance
        cell.configure(style="Revealed.TButton", relief="sunken")
        
        # Show adjacent mine count if greater than 0
        if cell.adjacent_mines > 0:
            colors = ["", "blue", "green", "red", "purple", "maroon", "cyan", "black", "gray"]
            color = colors[cell.adjacent_mines] if cell.adjacent_mines < len(colors) else "black"
            cell.configure(text=str(cell.adjacent_mines), foreground=color)
        else:
            # Reveal adjacent cells if no adjacent mines
            for i in range(max(0, x-1), min(self.rows, x+2)):
                for j in range(max(0, y-1), min(self.cols, y+2)):
                    if not self.cells[i][j].is_revealed:
                        self.reveal_cell(i, j)
                        
    def reveal_mines(self):
        """Reveal all mines when game is lost"""
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.cells[i][j]
                if cell.is_mine:
                    if not cell.is_flagged:
                        cell.configure(text="💣", style="Danger.TButton")
                elif cell.is_flagged and not cell.is_mine:
                    cell.configure(text="❌", style="Info.TButton")
                    
    def check_win(self):
        """Check if player has won the game"""
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.cells[i][j]
                # If there's a non-mine cell that hasn't been revealed, game is not won
                if not cell.is_mine and not cell.is_revealed:
                    return
                    
        # All non-mine cells have been revealed - player wins
        self.game_over = True
        self.status_var.set("恭喜你，胜利了!")
        self.restart_btn.configure(text="😎")
        
        # Flag all mines
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.cells[i][j]
                if cell.is_mine and not cell.is_flagged:
                    cell.configure(text="🚩", style="Warning.TButton")
                    
    def restart_game(self):
        """Restart the game"""
        # Reset game state
        self.game_over = False
        self.first_click = True
        self.status_var.set("点击任意格子开始游戏")
        self.restart_btn.configure(text="😊")
        
        # Clear game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy()
            
        # Recreate cells
        self.create_cells()

    def run(self):
        """Start the game"""
        self.root.mainloop()

if __name__ == "__main__":
    game = MinesweeperGame()
    game.run()