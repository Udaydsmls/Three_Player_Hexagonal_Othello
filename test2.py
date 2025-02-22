def generate_matrix():
    rows = 15
    cols = 15
    matrix = []
    for i in range(rows):
        # For rows 0-7, ones count = i + 8.
        # For rows 8-14, ones count decreases: 15 - (i - 7)
        if i < 8:
            ones_count = i + 8
        else:
            ones_count = 15 - (i - 7)
        # Create the row: ones_count ones followed by the rest zeros.
        row = [1] * ones_count + [0] * (cols - ones_count)
        matrix.append(row)
    return matrix
