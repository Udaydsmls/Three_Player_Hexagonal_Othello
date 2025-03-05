def generate_generalized_matrix(n: int, h: int, m0: int) -> list[list[str]]:
    width = n + 2 * m0
    matrix = []

    for i in range(h):
        delta = min(i, h - 1 - i)
        margin = max(m0 - delta, 0)
        block_len = width - 2 * margin
        block = ["  " for _ in range(block_len)]
        row = ["X "] * margin + block + ["X "] * margin
        matrix.append(row)

    return matrix

