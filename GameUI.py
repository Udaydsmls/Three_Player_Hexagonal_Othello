import tkinter as tk
from tkinter import messagebox
import test1
import test2

# Initialize matrices
matrix = test1.generate_generalized_matrix(8, 15, 7)
board = test2.generate_matrix()

# Predefined board modifications
preset_positions = {
    (7, 6): 2, (7, 8): 2, (7, 5): 3, (7, 9): 4,
    (6, 6): 3, (6, 7): 4, (8, 6): 4, (8, 7): 3,
    (5, 5): 2, (5, 7): 2, (9, 5): 3, (9, 7): 4
}
for (x, y), val in preset_positions.items():
    board[x][y] = val

# Update function


def update_matrix_based_on_board():
    m = len(board[0])
    n = len(matrix[0])
    for i in range(len(board)):
        l = 0
        r = 0
        while l < n and r < m:
            if matrix[i][l] == 0:
                l += 1
            else:
                matrix[i][l] = board[i][r]
                l += 1
                r += 1


def on_cell_click(row, col):
    board[row][col] = (board[row][col] % 4) + \
        2  # Rotate through values 2,3,4,5
    update_matrix_based_on_board()
    update_ui()


def update_ui():
    for r in range(len(board)):
        for c in range(len(board[0])):
            buttons[r][c].config(text=str(board[r][c]),
                                 bg=color_map.get(board[r][c], "white"))


root = tk.Tk()
root.title("Game Board")

color_map = {0: "white", 2: "lightblue",
             3: "lightgreen", 4: "lightcoral", 5: "lightyellow"}
buttons = []

for r in range(len(board)):
    row_buttons = []
    for c in range(len(board[0])):
        btn = tk.Button(root, text=str(board[r][c]), width=3, height=1,
                        bg=color_map.get(board[r][c], "white"),
                        command=lambda x=r, y=c: on_cell_click(x, y))
        btn.grid(row=r, column=c)
        row_buttons.append(btn)
    buttons.append(row_buttons)

update_matrix_based_on_board()
update_ui()

root.mainloop()
