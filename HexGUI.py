import tkinter as tk
from tkinter import messagebox
from RL import QLearningAgent
from HexOthello import ThreePlayerOthello
import numpy as np

CELL_SIZE = 40


class OthelloGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Three-Player Othello")
        self.game = ThreePlayerOthello()
        self.game.rl_agent = QLearningAgent(state_size=15 * 22, action_size=15 * 22)

        self.canvas = tk.Canvas(self.master, width=22 * CELL_SIZE, height=15 * CELL_SIZE)
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
        for r in range(15):
            for c in range(22):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")

                piece = self.game.board[r][c]
                if piece == 'X ':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")
                if piece != "  ":
                    color = "black"
                    if piece == "A ":
                        color = "blue"
                    elif piece == "B ":
                        color = "red"
                    elif piece == "C ":
                        color = "yellow"
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=color)

    def handle_click(self, event):
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE

        current_player = self.game.players[self.game.current_player_index]
        moves = self.game.valid_moves(current_player)

        if current_player != "C ":
            if (r, c) in moves:
                self.game.make_move(r, c, current_player)
                self.game.current_player_index = (self.game.current_player_index + 1) % 3
            else:
                print("Invalid move. Please try again.")

        self.handle_rl_agent_turn()
        self.draw_board()


        if not self.game.game_over():
            self.update_status()
        else:
            self.end_game()


    def handle_rl_agent_turn(self):
        while self.game.players[self.game.current_player_index] == "C " and not self.game.game_over():
            moves = self.game.valid_moves("C ")
            if not moves:
                self.game.current_player_index = (self.game.current_player_index + 1) % 3
                break

            state = np.array([self.game.get_numeric_state()])
            valid_actions = [row * 15 + col for row, col in moves]
            action = self.game.rl_agent.get_action(state, valid_actions)
            row, col = divmod(action, 15)

            self.game.make_move(row, col, "C ")
            reward = self.game.get_reward("C ")
            next_state = np.array([self.game.get_numeric_state()])
            done = self.game.game_over()
            self.game.rl_agent.update(state, action, reward, next_state, done)
            self.game.current_player_index = (self.game.current_player_index + 1) % 3
            self.draw_board()
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
