from HexBoard import generate_generalized_matrix


class ThreePlayerOthello:
    def __init__(self):
        self.board = self.create_board()
        self.players = ["A ", "B ", "C "]
        self.current_player_index = 0

    def create_board(self):
        board = generate_generalized_matrix(8, 15, 7)
        board[7][12] = "A "
        board[7][10] = "C "
        board[7][11] = "B "
        board[6][12] = "B "
        board[6][10] = "A "
        board[6][11] = "C "
        board[8][12] = "C "
        board[8][10] = "B "
        board[8][11] = "A "
        return board

    def print_board(self):
        print("   0 ",  "  ".join(str(i) for i in range(1, 11)),"" + " ".join(str(i) for i in range(11, 22)), sep=" ")
        for i, row in enumerate(self.board):
            print(f"{i:2} " + " ".join(row))

    def in_bounds(self, r, c):
        return 0 <= r < 15 and 0 <= c < 22

    def get_opponents(self, current_player):
        # For flipping, all disks that are not current_player are flippable
        return [p for p in ["A ", "B ", "C "] if p != current_player]

    def valid_moves(self, player):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for r in range(15):
            for c in range(22):
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
            # If we found a chain and ended on player's disk, flip it
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

    def play_game(self):
        while not self.game_over():
            self.print_board()
            player = self.players[self.current_player_index]
            print(f"Player {player}'s turn.")
            moves = self.valid_moves(player)
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

if __name__ == "__main__":
    game = ThreePlayerOthello()
    game.play_game()
    