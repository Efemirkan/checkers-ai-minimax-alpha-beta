import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from moves import apply_move_to_board, make_move
from board import empty_board
from constants import *


# Test, applying normal move to the board
def test_apply_normal_move():

    board = empty_board()
    board[2][3] = BLACK

    move = make_move([(2, 3), (3, 4)], [])

    new_board = apply_move_to_board(board, move)

    # Moved piece leaves old square
    assert new_board[2][3] == EMPTY

    # Resulting board is correct
    assert new_board[3][4] == BLACK

# Test, applying capture move to the board
def test_apply_capture_move():

    board = empty_board()
    board[2][3] = BLACK
    board[3][4] = WHITE

    move = make_move([(2, 3), (4, 5)], [(3, 4)])

    new_board = apply_move_to_board(board, move)

    # Moved piece leaves old square
    assert new_board[2][3] == EMPTY

    # Captured piece disappears
    assert new_board[3][4] == EMPTY

    # Resulting board is correct
    assert new_board[4][5] == BLACK

# Test, applying promotion move to the board
def test_apply_move_promotion():

    board = empty_board()
    board[6][1] = BLACK

    move = make_move([(6, 1), (7, 0)], [], promotes=True)

    new_board = apply_move_to_board(board, move)

    # Moved piece leaves old square
    assert new_board[6][1] == EMPTY

    # Resulting board is correct with king
    assert new_board[7][0] == BLACK_KING