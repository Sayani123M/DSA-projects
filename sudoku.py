import tkinter as tk
from tkinter import messagebox
import random
import time

# Function to check if a number is valid in a given position
def is_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    for i in range(9):
        if num in [board[i][col]]:
            return False
    
    # Check 3x3 sub-grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    
    return True


# Function to generate a complete Sudoku grid
def generate_full_grid():
    board = [[0 for j in range(9)] for i in range(9)]
    def solve():
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if solve():
                                return True
                            board[row][col] = 0
                    return False
        return True
    solve()
    return board

# Function to remove numbers from the grid based on difficulty
def remove_numbers(board, difficulty):
    if difficulty == "Easy":
        cells_to_remove = random.randint(35, 50)
    elif difficulty == "Intermediate":
        cells_to_remove = random.randint(30, 35)
    else:  # Hard
        cells_to_remove = random.randint(25, 30)
    puzzle = [row[:] for row in board]
    while cells_to_remove > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            cells_to_remove -= 1
    return puzzle

# Sudoku Application
class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.entries = [[None for j in range(9)] for i in range(9)] #all cells are empty
        self.hint_count = 3
        self.start_time = None
        self.timer_label = None
        self.current_puzzle = []
        self.solution = []
        self.create_widgets()
        self.start_timer()
        
    def create_widgets(self):
        # Difficulty level selector
        tk.Label(self.root, text="Select Difficulty:", font=("Arial", 12)).grid(row=0, column=0, columnspan=9, pady=5)
        difficulties = ["Easy", "Intermediate", "Hard"]
        for i, level in enumerate(difficulties):
            tk.Button(self.root, text=level, command=lambda lvl=level: self.load_puzzle(lvl), font=("Arial", 10)).grid(row=1, column=i * 3, columnspan=3, pady=5, sticky="ew")

        # Timer
        self.timer_label = tk.Label(self.root, text="Time: 00:00", font=("Arial", 12))
        self.timer_label.grid(row=2, column=0, columnspan=9, pady=5)

        # Sudoku board
        for row in range(9):
            for col in range(9):
                frame = tk.Frame(
                    self.root,
                    width=50,
                    height=50,
                    highlightbackground="black",
                    highlightthickness=1,
                )
                frame.grid(row=row + 3, column=col, padx=1, pady=1, sticky="nsew")
                self.root.grid_rowconfigure(row + 3, weight=1, minsize=50)  # Set consistent row size
                self.root.grid_columnconfigure(col, weight=1, minsize=50)   # Set consistent column size

                entry = tk.Entry(frame, justify="center", font=("Arial", 18))
                self.entries[row][col] = entry
                entry.pack(expand=True, fill="both")

        # Control buttons
        tk.Button(self.root, text="Hint (3)", command=self.give_hint, font=("Arial", 10)).grid(
            row=12, column=0, columnspan=4, pady=10, sticky="ew"
        )
        tk.Button(self.root, text="Check Solution", command=self.check_solution, font=("Arial", 10)).grid(
            row=12, column=5, columnspan=4, pady=10, sticky="ew"
        )

    def load_puzzle(self, level):
        full_grid = generate_full_grid()
        self.current_puzzle = remove_numbers(full_grid, level)
        self.solution = full_grid
        self.hint_count = 3
        self.update_hint_button()
        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                value = self.current_puzzle[row][col]
                if value != 0:
                    entry.insert(0, str(value))
                    entry.config(state="disabled", disabledforeground="black")
        self.start_time = time.time()

    def give_hint(self):
        if not hasattr(self, "hint_count"):  # Debug check
            messagebox.showerror("Error", "Hints are not initialized!")
            return

        if self.hint_count == 0:
            messagebox.showerror("No Hints", "No hints remaining!")
            return

        empty_cells = [(r, c) for r in range(9) for c in range(9) if not self.entries[r][c].get()]
        if not empty_cells:
            messagebox.showinfo("Hints", "No empty cells left to hint!")
            return

        row, col = random.choice(empty_cells)
        self.entries[row][col].insert(0, str(self.solution[row][col]))
        self.entries[row][col].config(state="disabled", disabledforeground="blue")
        self.hint_count -= 1
        self.update_hint_button()


    def check_solution(self):
        for row in range(9):
            for col in range(9):
                entry_value = self.entries[row][col].get()
                if not entry_value.isdigit() or int(entry_value) != self.solution[row][col]:
                    messagebox.showerror("Incorrect Solution", "The solution is incorrect!")
                    return
        messagebox.showinfo("Congratulations!", "You solved the Sudoku!")
        # Reset the timer
        self.start_time = None
        self.timer_label.config(text="Time: 00:00")

    def update_hint_button(self):
        hint_button = self.root.grid_slaves(row=12, column=0)[0]
        hint_button.config(text=f"Hint ({self.hint_count})")

    def start_timer(self):
        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            self.timer_label.config(text=f"Time: {minutes:02}:{seconds:02}")
        self.root.after(1000, self.start_timer)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
