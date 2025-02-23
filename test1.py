def generate_generalized_matrix(n, h, m0):
    """
    Generate a matrix with a varying alternating block pattern.

    Parameters:
      n  : Number of 1's in the alternating block of the first row
           (the block length in the first row will be 2*n - 1, giving n ones)
      h  : Total number of rows in the matrix
      m0 : Left/right padding (number of zeros) in the first row

    Returns:
      A 2D list (matrix) where each element is an integer (0 or 1)
    """
    # Total width is fixed for all rows:
    width = (2 * n - 1) + 2 * m0
    matrix = []  # This will store the final 2D array

    for i in range(h):
        # Compute a delta for vertical symmetry (distance from top or bottom)
        delta = min(i, h - 1 - i)
        # Adjust margin for the current row (ensuring it doesn't become negative)
        margin = max(m0 - delta, 0)
        # The alternating block length is what remains after subtracting margins
        block_len = width - 2 * margin
        # Create the alternating block starting with 1 (i.e., positions 0,2,4,... are 1's)
        block = [1 if j % 2 == 0 else 0 for j in range(block_len)]
        # Build the full row: left margin zeros + block + right margin zeros
        row = [0] * margin + block + [0] * margin
        matrix.append(row)

    return matrix


# Example usage:
# Let's create a matrix with:
# - 9 ones in the alternating block of the first row,
# - 15 total rows,
# - 6 zeros as padding on each side in the first row.
matrix = generate_generalized_matrix(8, 15, 7)
