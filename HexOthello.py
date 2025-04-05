from HexBoard import generate_generalized_matrix
import numpy as np

class ThreePlayerOthello:
    def __init__(self):
        self.board = self.create_board()
        self.players = ["A ", "B ", "C "]
        self.current_player_index = 0

    def create_board(self):
        board = generate_generalized_matrix(7, 13, 6)
        board[5][8] = "A "
        board[5][9] = "C "
        board[5][10] = "B "
        board[6][8] = "B "
        board[6][9] = "A "
        board[6][10] = "C "
        board[7][8] = "C "
        board[7][9] = "B "
        board[7][10] = "A "
        return board

    def print_board(self):
        print("   0 ", "  ".join(str(i) for i in range(1, 11)), "" + " ".join(str(i) for i in range(11, 19)), sep=" ")
        for i, row in enumerate(self.board):
            print(f"{i:2} " + " ".join(row))

    def in_bounds(self, r, c):
        return 0 <= r < 13 and 0 <= c < 19

    def get_opponents(self, current_player):
        return [p for p in ["A ", "B ", "C "] if p != current_player]

    def valid_moves(self, player):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for r in range(13):
            for c in range(19):
                if self.board[r][c] != "  ":
                    continue
                for dr, dc in directions:
                    row, col = r + dr, c + dc
                    found_opponent = False
                    while self.in_bounds(row, col) and self.board[row][col] in self.get_opponents(player):
                        found_opponent = True
                        row += dr
                        col += dc
                    if found_opponent and self.in_bounds(row, col) and self.board[row][col] == player:
                        moves.append((r, c))
                        break
        return moves

    def make_move(self, r, c, player):
        self.board[r][c] = player
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            row, col = r + dr, c + dc
            chain = []
            while self.in_bounds(row, col) and self.board[row][col] in self.get_opponents(player):
                chain.append((row, col))
                row += dr
                col += dc
            if chain and self.in_bounds(row, col) and self.board[row][col] == player:
                for rr, cc in chain:
                    self.board[rr][cc] = player

    def game_over(self):
        for p in ["A ", "B ", "C "]:
            if self.valid_moves(p):
                return False
        return True

    def count_disks(self):
        counts = {"A ": 0, "B ": 0, "C ": 0}
        for row in self.board:
            for cell in row:
                if cell in counts:
                    counts[cell] += 1
        return counts
    
    def reset(self):
        self.board = self.create_board()
        self.players = ["A ", "B ", "C "]
        self.current_player_index = 0

    def get_numeric_state(self, player):
        return np.array(
            [[1 if cell == player else (0 if cell == "  " else (3 if cell == "X " else 2)) for cell in row] for row in self.board]
        )

    def get_reward(self, player):
        counts = self.count_disks()
        disk_reward = counts[player] - max(counts[p] for p in self.players if p != player)

        if self.game_over() and counts[player] == max(counts.values()):
            win_reward = 100
        else:
            win_reward = 0
        
        if self.game_over() and counts[player] != max(counts.values()):
            loss_penalty = -50 
        else:
            loss_penalty = 0
        
        return disk_reward + win_reward + loss_penalty