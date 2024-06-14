import tkinter as tk
from tkinter import messagebox
import random

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def generate_puzzle():
    board = [[0] * 9 for _ in range(9)]
    solve_sudoku(board)

    removed_count = 0
    while removed_count < 40:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            num = board[row][col]
            board[row][col] = 0

            test_board = [row[:] for row in board]
            if solve_sudoku(test_board):
                removed_count += 1
            else:
                board[row][col] = num

    return board

def create_board():
    return [[0] * 9 for _ in range(9)]

def solve():
    update_board()
    if solve_sudoku(puzzle):
        for i in range(9):
            for j in range(9):
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, str(puzzle[i][j]))
    else:
        messagebox.showinfo("Sudoku Solver", "No solution exists")

def clear():
    if user_entries:
        row, col, val = user_entries.pop()
        entries[row][col].delete(0, tk.END)

def hint():
    global puzzle, solution
    update_board()
    empty_cells = [(i, j) for i in range(9) for j in range(9) if puzzle[i][j] == 0]
    if empty_cells:
        row, col = random.choice(empty_cells)
        valid_numbers = [num for num in range(1, 10) if is_valid(puzzle, row, col, num)]
        if valid_numbers:
            num = random.choice(valid_numbers)
            entries[row][col].delete(0, tk.END)
            entries[row][col].insert(0, str(num))
            entries[row][col].config(state="disabled")
            user_entries.append((row, col, num))

def reset():
    global puzzle, user_entries
    puzzle = generate_puzzle()
    user_entries = []
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, str(puzzle[i][j]))
                entries[i][j].config(state="disabled")
            else:
                entries[i][j].delete(0, tk.END)
                entries[i][j].config(state="normal")

def update_board():
    global user_entries
    for i in range(9):
        for j in range(9):
            try:
                num = int(entries[i][j].get())
                if 1 <= num <= 9:
                    user_entries.append((i, j, num))
                else:
                    user_entries.append((i, j, 0))
            except ValueError:
                pass

def on_entry_change(event, row, col):
    def reset_color():
        entries[row][col].config(bg="white")

    entry_value = entries[row][col].get()

    if entry_value.isdigit() and 1 <= int(entry_value) <= 9:
        entries[row][col].config(bg="yellow")
        entries[row][col].after(500, reset_color)  # Change back to white after 500ms
    else:
        entries[row][col].delete(0, tk.END)  # Clear invalid input

puzzle = generate_puzzle()
solution = [row[:] for row in puzzle]
user_entries = []

root = tk.Tk()
root.title("Sudoku Solver")

entries = [[None for _ in range(9)] for _ in range(9)]
for i in range(9):
    for j in range(9):
        entries[i][j] = tk.Entry(root, width=2, font=('Arial', 18), borderwidth=1, relief="solid", justify='center')
        entries[i][j].grid(row=i, column=j, padx=5, pady=5)
        if puzzle[i][j] != 0:
            entries[i][j].insert(0, str(puzzle[i][j]))
            entries[i][j].config(state="disabled")
        else:
            entries[i][j].bind("<KeyRelease>", lambda event, row=i, col=j: on_entry_change(event, row, col))

solve_button = tk.Button(root, text="Solve", command=solve)
solve_button.grid(row=10, column=0, columnspan=2, pady=10)

clear_button = tk.Button(root, text="Clear", command=clear)
clear_button.grid(row=10, column=2, columnspan=2, pady=10)

hint_button = tk.Button(root, text="Hint", command=hint)
hint_button.grid(row=10, column=4, columnspan=2, pady=10)

reset_button = tk.Button(root, text="Reset", command=reset)
reset_button.grid(row=10, column=6, columnspan=3, pady=10)

root.mainloop()

#pip install matplotlib
