import tkinter as tk
from tkinter import messagebox
from HexOthello import ThreePlayerOthello
import numpy as np
import random
from RL_train import OthelloQLearningAgent

CELL_SIZE = 40

class OthelloGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Three-Player Othello")
        self.game = ThreePlayerOthello()
        self.game.rl_agent_c = OthelloQLearningAgent(state_size=13 * 19, action_size=13 * 19, epsilon=0.1, decay_rate=0.999, gamma=0.9)
        self.game.rl_agent_c.load_q_table("othello_q_table.pickle")

        self.canvas = tk.Canvas(self.master, width=19 * CELL_SIZE, height=13 * CELL_SIZE)
        self.canvas.pack()

        self.status_label = tk.Label(self.master, text="", font=("Arial", 14))
        self.status_label.pack()

        self.draw_board()
        self.update_status()
        self.master.after(1000, self.auto_play)

    def update_status(self):
        player = self.game.players[self.game.current_player_index]
        self.status_label.config(text=f"Player {player}'s turn")

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(13):
            for c in range(19):
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

    def handle_random_player_turn(self):
        moves = self.game.valid_moves("A ")
        if moves:
            move = random.choice(moves)
            self.game.make_move(move[0], move[1], "A ")
        self.game.current_player_index = (self.game.current_player_index + 1) % 3

    def handle_rl_agent_turn(self, player):
        if player != "C ":
            return
            
        moves = self.game.valid_moves(player)
        if not moves:
            self.game.current_player_index = (self.game.current_player_index + 1) % 3
            return
        
        state = np.array([self.game.get_numeric_state("C ")])
        valid_actions = [row * 19 + col for row, col in moves]
        action = self.game.rl_agent_c.get_action(state, valid_actions)
        row, col = divmod(action, 19)    
        self.game.make_move(row, col, player)
        self.game.current_player_index = (self.game.current_player_index + 1) % 3

    # def handle_hardcoded_player_turn(self):
    #     moves = self.game.valid_moves("B ")
    #     if moves:
    #         move = moves[0]
    #         self.game.make_move(move[0], move[1], "B ")
    #     self.game.current_player_index = (self.game.current_player_index + 1) % 3

    def handle_greedy_player_turn(self):
        moves = self.game.valid_moves("B ")
        if moves:
            best_move = None
            max_flips = -1

            for move in moves:
                r, c = move
                temp_board = [row[:] for row in self.game.board]
                self.game.make_move(r, c, "B ")  
                flipped_pieces = sum(row.count("B ") for row in self.game.board) - sum(row.count("B ") for row in temp_board)

                self.game.board = temp_board

                if flipped_pieces > max_flips:
                    max_flips = flipped_pieces
                    best_move = move

            if best_move:
                self.game.make_move(best_move[0], best_move[1], "B ")

        self.game.current_player_index = (self.game.current_player_index + 1) % 3

    def auto_play(self):
        if self.game.game_over():
            self.end_game()
            return
        
        current_player = self.game.players[self.game.current_player_index]
        
        if current_player == "A ":
            self.handle_random_player_turn()
        elif current_player == "B ":
            self.handle_greedy_player_turn()
        else:
            self.handle_rl_agent_turn(current_player)
        
        self.draw_board()
        self.update_status()
        
        if not self.game.game_over():
            self.master.after(600, self.auto_play)
        else:
            self.end_game()

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