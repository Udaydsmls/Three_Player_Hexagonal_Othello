from RL import QLearningAgent
import numpy as np

class ThreePlayerOthello:
    """
    A class representing the Three-Player Othello game.
    """

    def __init__(self):
        """
        Initialize the Othello game board and players.
        """
        self.board = self.create_board()
        self.players = ["A", "B", "C"]
        self.current_player_index = 0
        self.rl_agent = QLearningAgent(state_size=11*11, action_size=11*11, epsilon=0.1)

    def create_board(self):
        """
        Create and return the initial game board.

        Returns:
            list: A 2D list representing the 11x11 game board with initial piece positions.
        """
        board = [[" " for _ in range(11)] for _ in range(11)]
        board[4][4] = "A" 
        board[4][5] = "C"  
        board[4][6] = "B"  
        board[5][4] = "B"  
        board[5][5] = "A"  
        board[5][6] = "C"  
        board[6][4] = "C"  
        board[6][5] = "B"  
        board[6][6] = "A"  
        return board

    def print_board(self):
        """
        Print the current state of the game board to the console.
        """
        print("   " + " ".join(str(i) for i in range(11)))
        for i, row in enumerate(self.board):
            print(f"{i:2} " + " ".join(row))

    def in_bounds(self, r, c):
        """
        Check if a given position is within the board boundaries.

        Args:
            r (int): Row index.
            c (int): Column index.

        Returns:
            bool: True if the position is within bounds, False otherwise.
        """
        return 0 <= r < 11 and 0 <= c < 11

    def get_opponents(self, current_player):
        """
        Get the list of opponent players for the current player.

        Args:
            current_player (str): The current player's identifier.

        Returns:
            list: A list of opponent player identifiers.
        """
        return [p for p in ["A", "B", "C"] if p != current_player]

    def valid_moves(self, player):
        """
        Get all valid moves for the given player.

        Args:
            player (str): The player's identifier.

        Returns:
            list: A list of tuples representing valid move positions (row, column).
        """
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for r in range(11):
            for c in range(11):
                if self.board[r][c] != " ":
                    continue
                for dr, dc in directions:
                    row, col = r + dr, c + dc
                    found_opponent = False
                    # Need to find any chain of opponents, then the player
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
        Make a move for the given player at the specified position.

        Args:
            r (int): Row index of the move.
            c (int): Column index of the move.
            player (str): The player's identifier.
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
            # If we found a chain and ended on player's disk, flip it
            if chain and self.in_bounds(row, col) and self.board[row][col] == player:
                for rr, cc in chain:
                    self.board[rr][cc] = player

    def game_over(self):
        """
        Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        for p in ["A", "B", "C"]:
            if self.valid_moves(p):
                return False
        return True

    def count_disks(self):
        """
        Count the number of disks for each player.

        Returns:
            dict: A dictionary with player identifiers as keys and disk counts as values.
        """
        counts = {"A": 0, "B": 0, "C": 0}
        for row in self.board:
            for cell in row:
                if cell in counts:
                    counts[cell] += 1
        return counts
    
    def play_game(self):
        while not self.game_over():
            self.print_board()
            player = self.players[self.current_player_index]
            print(f"Player {player}'s turn.")
            moves = self.valid_moves(player)
            
            if player == "C":  # RL agent's turn
                if moves:
                    state = np.array([self.get_numeric_state()])
                    valid_actions = [row * 11 + col for row, col in moves]
                    action = self.rl_agent.get_action(state, valid_actions)
                    row, col = divmod(action, 11)
                    self.make_move(row, col, player)
                    reward = self.get_reward(player)
                    next_state = np.array([self.get_numeric_state()])
                    done = self.game_over()
                    self.rl_agent.update(state, action, reward, next_state, done)
                else:
                    print("Invalid move by RL agent. Skipping turn.")
            else:  # Human player's turn
                if not moves:
                    print(f"No valid moves for {player}, skipping.")
                else:
                    print("Valid moves:", moves)
                    choice = None
                    while choice not in moves:
                        user_input = input("Enter row,col for your move (e.g. 4,5): ")
                        try:
                            r, c = map(int, user_input.split(","))
                            if (r, c) in moves:
                                choice = (r, c)
                            else:
                                print("Invalid move. Try again.")
                        except ValueError:
                            print("Invalid input. Try again.")
                    self.make_move(choice[0], choice[1], player)

            self.current_player_index = (self.current_player_index + 1) % 3

        self.print_board()
        final_counts = self.count_disks()
        print("Game Over!")
        print("Scores:", final_counts)
        winner = max(final_counts, key=final_counts.get)
        print(f"Winner is Player {winner} with {final_counts[winner]} disks!")

    def get_numeric_state(self):
        """
        Convert the current board state to a numeric representation.

        Returns:
            numpy.array: A 2D numpy array representing the board state numerically.
        """
        return np.array([[0 if cell == " " else ord(cell) - ord("A") + 1 for cell in row] for row in self.board])

    def get_reward(self, player):
        """
        Calculate the reward for the given player based on the current board state.

        Args:
            player (str): The player's identifier.

        Returns:
            int: The calculated reward value.
        """
        counts = self.count_disks()
        return counts[player] - max(counts[p] for p in self.players if p != player)

    # def play_game(self):
    #     while not self.game_over():
    #         self.print_board()
    #         player = self.players[self.current_player_index]
    #         print(f"Player {player}'s turn.")
    #         moves = self.valid_moves(player)
    #         if not moves:
    #             print(f"No valid moves for {player}, skipping.")
    #         else:
    #             print("Valid moves:", moves)
    #             choice = None
    #             while choice not in moves:
    #                 user_input = input("Enter row,col for your move (e.g. 4,5): ")
    #                 try:
    #                     r, c = map(int, user_input.split(","))
    #                     if (r, c) in moves:
    #                         choice = (r, c)
    #                     else:
    #                         print("Invalid move. Try again.")
    #                 except ValueError:
    #                     print("Invalid input. Try again.")
    #             self.make_move(choice[0], choice[1], player)
    #         self.current_player_index = (self.current_player_index + 1) % 3

    #     self.print_board()
    #     final_counts = self.count_disks()
    #     print("Game Over!")
    #     print("Scores:", final_counts)
    #     winner = max(final_counts, key=final_counts.get)
    #     print(f"Winner is Player {winner} with {final_counts[winner]} disks!")

if __name__ == "__main__":
    game = ThreePlayerOthello()
    game.play_game()
    