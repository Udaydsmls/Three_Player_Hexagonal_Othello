import math

def generate_generalized_matrix(n: int, h: int, m0: int) -> list[list[str]]:
    width = n + 2 * m0
    matrix = []
    nonzero_coords = []

    for i in range(h):
        delta = min(i, h - 1 - i)
        margin = max(m0 - delta, 0)
        block_len = width - 2 * margin
        row = [0] * margin + [1] * block_len + [0] * margin
        for j in range(margin, margin + block_len):
            nonzero_coords.append((i, j))
        matrix.append(row)

    vertices = []
    if h > 0 and n > 0:
        vertices.append((0, m0))
        vertices.append((0, m0 + n - 1))
        vertices.append((h - 1, m0))
        vertices.append((h - 1, m0 + n - 1))
        if h > 2 * m0:
            vertices.append((m0, 0))
            vertices.append((m0, width - 1))

    vertices_set = set(vertices)

    for (i, j) in vertices_set:
        if 0 <= i < h and 0 <= j < width and matrix[i][j] == 1:
            matrix[i][j] = 100

    def get_adjacent_neighbors(i: int, j: int) -> list[tuple[int, int]]:
        candidates = [
            (i - 1, j),
            (i + 1, j),
            (i, j - 1),
            (i, j + 1),
            (i - 1, j - 1),
            (i - 1, j + 1),
            (i + 1, j - 1),
            (i + 1, j + 1)
        ]
        neighbors = []
        for (ai, aj) in candidates:
            if 0 <= ai < h and 0 <= aj < width and matrix[ai][aj] == 1:
                neighbors.append((ai, aj))
            if len(neighbors) == 4:
                break
        return neighbors

    for (i, j) in vertices_set:
        adj = get_adjacent_neighbors(i, j)
        for (ai, aj) in adj:
            matrix[ai][aj] = -2

    center_row = h // 2
    center_col = width // 2
    d_max = 0
    for (i, j) in nonzero_coords:
        if matrix[i][j] == 1:
            d = math.sqrt((i - center_row) ** 2 + (j - center_col) ** 2)
            d_max = max(d_max, d)
    if d_max == 0:
        d_max = 1

    for (i, j) in nonzero_coords:
        if matrix[i][j] == 1:
            d = math.sqrt((i - center_row) ** 2 + (j - center_col) ** 2)
            new_val = 2 * (d / d_max)
            matrix[i][j] = new_val

    matrix_str = [[f"{val:.2f}" for val in row] for row in matrix]
    return matrix_str

# matrix = generate_generalized_matrix(8, 15, 7)
# for row in matrix:
#     print(" ".join(map(str, row)))