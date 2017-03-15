from copy import deepcopy

import random

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

S_SHAPE = [
    [
        [0, 1, 1],
        [1, 1, 0]
    ],
    [
        [1, 0],
        [1, 1],
        [0, 1]
    ]
]

L_SHAPE = [
    [
        [0, 0, 1],
        [1, 1, 1]
    ],
    [
        [1, 0],
        [1, 0],
        [1, 1]
    ],
    [
        [1, 1, 1],
        [1, 0, 0]
    ],
    [
        [1, 1],
        [0, 1],
        [0, 1]
    ]
]

O_SHAPE = [
    [
        [1, 1],
        [1, 1]
    ]
]

I_SHAPE = [
    [
        [1, 1, 1, 1]
    ],
    [
        [1],
        [1],
        [1],
        [1]
    ]
]

J_SHAPE = [
    [
        [1, 1, 1],
        [0, 0, 1]
    ],
    [
        [0, 1],
        [0, 1],
        [1, 1]
    ],
    [
        [1, 0 , 0],
        [1, 1 , 1]
    ],
    [
        [1, 1],
        [1, 0],
        [1, 0]
    ]
]

T_SHAPE = [
    [
        [0, 1, 0],
        [1, 1, 1]
    ],
    [
        [1, 0],
        [1, 1],
        [1, 0]
    ],
    [
        [1, 1, 1],
        [0, 1, 0]
    ],
    [
        [0, 1],
        [1, 1],
        [0, 1]
    ]
]

Z_SHAPE = [
    [
        [1, 1, 0],
        [0, 1, 1]
    ],
    [
        [0, 1],
        [1, 1],
        [1, 0]
    ]
]

SHAPES = [S_SHAPE, L_SHAPE, O_SHAPE, I_SHAPE]
SHAPES = [O_SHAPE]


class Piece(object):
    def __init__(self, shape):
        self.shape = shape[0]
        self.rotations = shape
        self.y = 0
        self.x = int(BOARD_WIDTH / 2) - int(len(self.shape) / 2)

    def get_next_rotation(self):
        index = self.rotations.index(self.shape)
        return self.rotations[index - 1]


def get_initial_board():
    global BOARD_WIDTH
    global BOARD_HEIGHT
    return [[0 for _ in range(BOARD_WIDTH)] for __ in range(BOARD_HEIGHT)]


def can_fall(board, piece):
    if len(piece.shape) + piece.y + 1 > len(board):
        return False
    for y in range(len(piece.shape)):
        for x in range(len(piece.shape[y])):
            if board[y + piece.y + 1][x + piece.x] + piece.shape[y][x] > 1:
                return False

    return True


def can_fit(board, piece, dy=0, dx=0, rotated=False):
    try:
        shape = piece.get_next_rotation() if rotated else piece.shape
        if len(shape) + piece.y + 1 > len(board):
            return False
        for y in range(len(shape)):
            for x in range(len(shape[y])):
                if board[y + piece.y + dy][x + piece.x + dx] + shape[y][x] > 1:
                    return False

        return True
    except IndexError:
        return False


def check_lines(board):
    reward = 0
    new_board = deepcopy(board)
    for row in range(len(board)):
        if _check_row(board[row]):
            new_board = clear_row(board, row)
            reward += 1

    return new_board, reward


def _check_row(board_row):
    for block in board_row:
        if block == 0:
            return False
    return True


def clear_row(board, row):
    new_board = deepcopy(board)
    for i in reversed(range(1, row + 1)):
        new_board[i] = board[i-1]
    new_board[0] = [0] * len(board[0])

    return new_board


def add_to_board(board, piece):
    new_board = deepcopy(board)
    for y in range(len(piece.shape)):
        for x in range(len(piece.shape[y])):
            new_board[y + piece.y][x + piece.x] = board[y + piece.y][x + piece.x] + piece.shape[y][x]

    return new_board


def get_new_piece():
    global SHAPES
    pick = random.choice(SHAPES)
    piece = Piece(pick)

    return piece


def print_board(board):
    for i in board:
        print(i)
    print('#----------------#')


def test():
    board = \
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
        ]

    piece = Piece(S_SHAPE)
    piece.y = 17

    final_board = add_to_board(board, piece)

    print_board(final_board)


def main():
    board = get_initial_board()

    for i in range(7):
        piece = get_new_piece()

        while can_fall(board, piece):
            piece.y += 1

            temp_board = add_to_board(board, piece)
            print_board(temp_board)

        board = add_to_board(board, piece)

    print_board(board)
    print('final board')


if __name__ == '__main__':
    pass
