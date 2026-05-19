import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from moves import all_legal_moves, find_piece_captures, make_move
from constants import *

# Test single capture
def test_single_capture():

    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    board[2][3] = BLACK
    board[3][4] = WHITE

    start_move = make_move([(2, 3)], [])

    moves = find_piece_captures(board, start_move)
    paths = [m["path"] for m in moves]
    captures = [m["captures"] for m in moves]

    assert [(2, 3), (4, 5)] in paths
    assert [(3, 4)] in captures


# Test forced capture
def test_forced_capture():

    board = initial_board

    board[2][3] = BLACK
    board[3][4] = WHITE
    board[3][2] = EMPTY

    moves = all_legal_moves(board, BLACK)

    paths = [m["path"] for m in moves]

    assert [(2, 3), (4, 5)] in paths

    # Normal moves should not be returned if capture exists
    assert [(2, 3), (3, 2)] not in paths


# Test alternative captures
def test_alternative_captures():

    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    board[2][3] = BLACK
    board[3][2] = WHITE
    board[3][4] = WHITE

    start_move = make_move([(2, 3)], [])

    moves = find_piece_captures(board, start_move)
    paths = [m["path"] for m in moves]

    assert [(2, 3), (4, 1)] in paths
    assert [(2, 3), (4, 5)] in paths

    assert len(moves) == 2


# Test multi-capture path generation
def test_multi_capture_path_generation():

    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    board[2][3] = BLACK
    board[3][4] = WHITE
    board[5][6] = WHITE

    start_move = make_move([(2, 3)], [])

    moves = find_piece_captures(board, start_move)
    paths = [m["path"] for m in moves]
    captures = [m["captures"] for m in moves]

    assert [(2, 3), (4, 5), (6, 7)] in paths
    assert [(3, 4), (5, 6)] in captures