import tkinter as tk
from tkinter import messagebox
from Othello import ThreePlayerOthello

CELL_SIZE = 40

class OthelloGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Three-Player Othello")
        self.game = ThreePlayerOthello()

        self.canvas = tk.Canvas(self.master, width=11*CELL_SIZE, height=11*CELL_SIZE)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        self.status_label = tk.Label(self.master, text="", font=("Arial", 14))
        self.status_label.pack()

        self.draw_board()
        self.update_status()

    def update_status(self):
        player = self.game.players[self.game.current_player_index]
        self.status_label.config(text=f"Player {player}'s turn")

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(11):
            for c in range(11):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")

                piece = self.game.board[r][c]
                if piece != " ":
                    color = "black"
                    if piece == "A":
                        color = "blue"
                    elif piece == "B":
                        color = "red"
                    elif piece == "C":
                        color = "yellow"
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill=color)

    def handle_click(self, event):
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE

        current_player = self.game.players[self.game.current_player_index]
        moves = self.game.valid_moves(current_player)

        if (r, c) in moves:
            self.game.make_move(r, c, current_player)
            self.game.current_player_index = (self.game.current_player_index + 1) % 3
            if self.game.game_over():
                self.end_game()
            else:
                # Skip players with no moves
                while not self.game.valid_moves(self.game.players[self.game.current_player_index]) \
                      and not self.game.game_over():
                    self.game.current_player_index = (self.game.current_player_index + 1) % 3
                if self.game.game_over():
                    self.end_game()
        else:
            print("Invalid move. Please try again.")

        self.draw_board()
        if not self.game.game_over():
            self.update_status()

    def end_game(self):
        counts = self.game.count_disks()
        winner = max(counts, key=counts.get)
        messagebox.showinfo("Game Over", f"Player {winner} wins with {counts[winner]} disks!")

def main():
    root = tk.Tk()
    OthelloGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    