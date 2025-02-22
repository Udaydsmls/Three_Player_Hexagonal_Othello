def generate_matrix(rows=8, cols=15):
    matrix = []
    for r in range(rows):
        # Determine the number of zeros on the left/right.
        # For rows 0 to 7, the margin is 3,2,1,0,0,1,2,3 respectively.
        margin = 3 - min(r, rows - 1 - r)
        inner_length = cols - 2 * margin

        # For the top half (rows 0-3) start with 1, for bottom half (rows 4-7) start with 2.
        start = 1 if r < rows // 2 else 2

        # Build the inner alternating pattern.
        inner = []
        for i in range(inner_length):
            # Alternate: even indices get 'start', odd get the other number (3 - start)
            inner.append(start if i % 2 == 0 else 3 - start)

        # Build the row: margins filled with 0 and then the inner alternating pattern.
        row_vals = [0] * margin + inner + [0] * margin
        matrix.append(row_vals)
    return matrix


def print_matrix(matrix):
    # Print each number as a negative number, even zeros appear as "-0"
    for row in matrix:
        print(" ".join(f"-{abs(x)}" for x in row))


# Generate and print the matrix.
mat = generate_matrix()
print_matrix(mat)
