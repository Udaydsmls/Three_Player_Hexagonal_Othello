"""
HexOthello.py

Module Description:
This module implements a three-player version of the Othello game on a hexagonal board.
It includes functionalities for creating the game board, making moves, checking game status, and calculating rewards.
"""

from HexBoard import generate_generalized_matrix
import numpy as np

class ThreePlayerOthello:
    """
    Represents a three-player Othello game on a hexagonal board.

    Attributes:
        board (list[list[str]]): The current state of the game board.
        players (list[str]): List of players in the game.
        current_player_index (int): Index of the current player.
    """
    def __init__(self):
        """
        Initializes the game by creating the board and setting up the players.
        """
        self.board = self.create_board()
        self.players = ["A ", "B ", "C "]
        self.current_player_index = 0

    def create_board(self):
        """
        Initializes the game board with starting positions for players.

        Returns:
            list[list[str]]: The initialized game board.
        """
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
        """
        Prints the current state of the game board.
        """
        print("   0 ", "  ".join(str(i) for i in range(1, 11)), "" + " ".join(str(i) for i in range(11, 19)), sep=" ")
        for i, row in enumerate(self.board):
            print(f"{i:2} " + " ".join(row))

    def in_bounds(self, r, c):
        """
        Checks if a given position is within the board boundaries.

        Parameters:
            r (int): Row index.
            c (int): Column index.

        Returns:
            bool: True if the position is within the board boundaries.
        """
        return 0 <= r < 13 and 0 <= c < 19

    def get_opponents(self, current_player):
        """
        Returns a list of opponents for the given player.

        Parameters:
            current_player (str): The current player.

        Returns:
            list[str]: List of opponents.
        """
        return [p for p in ["A ", "B ", "C "] if p != current_player]

    def valid_moves(self, player):
        """
        Finds all valid moves for the given player.

        Parameters:
            player (str): The player for whom to find valid moves.

        Returns:
            list[tuple[int, int]]: List of valid move positions.
        """
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
        """
        Places a disk on the board at the specified position for the given player.
        It also flips the opponent's disks in all directions if applicable.

        Parameters:
            r (int): Row index of the move.
            c (int): Column index of the move.
            player (str): The player making the move.
        """
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
        """
        Checks if the game is over by verifying if any player has valid moves.

        Returns:
            bool: True if the game is over.
        """
        for p in ["A ", "B ", "C "]:
            if self.valid_moves(p):
                return False
        return True

    def count_disks(self):
        """
        Counts the number of disks for each player on the board.

        Returns:
            dict[str, int]: Dictionary with disk counts for each player.
        """
        counts = {"A ": 0, "B ": 0, "C ": 0}
        for row in self.board:
            for cell in row:
                if cell in counts:
                    counts[cell] += 1
        return counts
    
    def reset(self):
        """
        Resets the game to its initial state.
        """
        self.board = self.create_board()
        self.players = ["A ", "B ", "C "]
        self.current_player_index = 0

    def get_numeric_state(self, player):
        """
        Returns a numeric representation of the board state for the given player.

        Parameters:
            player (str): The player for whom to get the numeric state.

        Returns:
            numpy.ndarray: Numeric representation of the board state.
        """
        return np.array(
            [[1 if cell == player else (0 if cell == "  " else (3 if cell == "X " else 2)) for cell in row] for row in self.board]
        )

    def get_reward(self, player):
        """
        Calculates the reward for the given player based on the current game state.

        Parameters:
            player (str): The player for whom to calculate the reward.

        Returns:
            int: The calculated reward.
        """
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