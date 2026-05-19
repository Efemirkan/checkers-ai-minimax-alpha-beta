import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from moves import find_piece_normal_moves, make_move
from constants import *

# Test; Black opening moves
def test_black_opening_moves():

    board = initial_board
    board[2][3] = BLACK  # Start position

    start_move = make_move([(2, 3)], [])

    moves = find_piece_normal_moves(board, start_move)
    paths = [m["path"] for m in moves]

    # Black moves down
    assert [(2, 3), (3, 2)] in paths
    assert [(2, 3), (3, 4)] in paths

    # Check Not backward
    for move in moves:
        start = move["path"][0]
        end = move["path"][1] 

        # End row greater number
        assert end[0] > start[0]

# Test; White opening moves
def test_white_opening_moves():
    
    board = initial_board
    board[5][4] = WHITE  # Start position

    start_move = make_move([(5, 4)], [])

    moves = find_piece_normal_moves(board, start_move)
    paths = [m["path"] for m in moves]

    # White moves up
    assert [(5, 4), (4, 3)] in paths
    assert [(5, 4), (4, 5)] in paths

    # Check Not backward
    for move in moves:
        start = move["path"][0]
        end = move["path"][1]

        # Start row greater number
        assert end[0] < start[0]

# Test; Kings moves
def test_king_moves():

    board = initial_board
    board[3][3] = BLACK_KING

    start_move = make_move([(3, 3)], [])
    moves = find_piece_normal_moves(board, start_move)

    directions = []
    for move in moves:
        start = move["path"][0]
        end = move["path"][1]

        # Append difference between end row and start row
        directions.append(end[0] - start[0])

    # King moves both directions
    assert any(d > 0 for d in directions)  # down
    assert any(d < 0 for d in directions)  # up