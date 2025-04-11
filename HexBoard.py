"""
HexBoard.py

Module Description:
This module provides functionality for generating a 2D matrix representation of a hexagonal board.
It allows customization of the board's dimensions and margins.
"""

def generate_generalized_matrix(n: int, h: int, m0: int) -> list[list[str]]:
    """
    Generates a 2D matrix representation of a hexagonal board with customizable dimensions and margins.

    Parameters:
        n (int): The base width of the hexagonal board.
        h (int): The height of the hexagonal board.
        m0 (int): The margin width around the hexagonal board.

    Returns:
        list[list[str]]: A 2D list representing the hexagonal board, where 'X ' represents the margin and ' ' represents the empty spaces within the board.
    """

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

