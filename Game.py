import test2, test1

matrix = test1.generate_generalized_matrix(8, 15, 7)
board = test2.generate_matrix()
board[7][6] = 2
board[7][8] = 2
board[7][5] = 3
board[7][9] = 4

board[6][6] = 3
board[6][7] = 4

board[8][6] = 4
board[8][7] = 3

board[5][5] = 2
board[5][7] = 2

board[9][5] = 3
board[9][7] = 4

def update_matrix_based_on_board(board, matrix):
    m = len(board[0])
    n = len(matrix[0])

    for i in range(len(board)):
        l = 0
        r = 0
        while l < n and r < m:
            if matrix[i][l] == 0: l+=1
            else:
                matrix[i][l] = board[i][r]
                l += 1
                r += 1


update_matrix_based_on_board(board, matrix)

for row in board:
    print(" ".join(map(str, row)))

print()
print("This is how board looks like:")
print()

for row in matrix:
    print(" ".join(map(str, row)))

while True:
    for i in range(3):
        x, y = map(int, input("Enter Pos: ").split())
        board[x][y] = i + 2
        update_matrix_based_on_board(board, matrix)
        for row in board:
            print(" ".join(map(str, row)))

        print()
        print("This is how board looks like:")
        print()
        for row in matrix:
            print(" ".join(map(str, row)))
