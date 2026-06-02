import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from constants import *
from board import empty_board, initial_board
from moves import all_legal_moves, apply_move_to_board


# Test, at starting position black in total of 7 legal moves
def test_starting_black_moves():

    moves = all_legal_moves(initial_board, BLACK)

    # Black should have exactly 7 opening moves
    assert len(moves) == 7

    # No captures should exist in the initial position
    assert all(move["captures"] == [] for move in moves)


# Test, If a capture is available, forced to capture move
def test_forced_capture_moves():

    board = empty_board()

    board[2][1] = BLACK
    board[3][2] = WHITE

    moves = all_legal_moves(board, BLACK)

    # Only one legal move should exist
    assert len(moves) == 1

    # Verify capture path
    assert moves[0]["path"] == [(2, 1), (4, 3)]

    # Verify captured piece
    assert moves[0]["captures"] == [(3, 2)]


# Test, after the first jump another capture must be performed
def test_multi_capture():

    board = empty_board()

    # Place pieces on the board
    board[2][1] = BLACK
    board[3][2] = WHITE
    board[5][4] = WHITE


    moves = all_legal_moves(board, BLACK)

    # Check to forced capture
    assert len(moves) == 1

    # Verify entire jump sequence
    assert moves[0]["path"] == [(2, 1), (4, 3), (6, 5)]

    # Verify both pieces were captured
    assert moves[0]["captures"] == [(3, 2), (5, 4)]


# Test, black piece promoted by reaching row 7
def test_promotion():

    board = empty_board()

    board[6][1] = BLACK

    moves = all_legal_moves(board, BLACK)

    promotion_moves = [move for move in moves if move["promotes"]]

    # At least one promotion move should exist
    assert promotion_moves

    # Verify promotion square
    assert any(move["path"] == [(6, 1), (7, 0)] for move in promotion_moves)

# Test, after promotion, the piece become king
def test_promotion_makes_king():

    board = empty_board()

    board[6][1] = BLACK

    move = {"path": [(6, 1), (7, 0)],
            "captures": [],
            "regicide": False,
            "promotes": True}

    new_board = apply_move_to_board(board, move)

    # Starting square becomes empty
    assert new_board[6][1] == EMPTY

    # Piece becomes king
    assert new_board[7][0] == BLACK_KING

# Test, regicide rule whenb normal piece capture the opponent king, prometed
def test_regicide():

    board = empty_board()

    board[2][1] = BLACK
    board[3][2] = WHITE_KING

    moves = all_legal_moves(board, BLACK)

    assert len(moves) == 1

    move = moves[0]

    # Verify jump path
    assert move["path"] == [(2, 1), (4, 3)]

    # Verify captured king
    assert move["captures"] == [(3, 2)]

    # Regicide should be detected
    assert move["regicide"] is True

    # Piece should be promoted
    assert move["promotes"] is True

# Test, after regicide, the piece become king
def test_regicide_king():

    board = empty_board()

    board[2][1] = BLACK
    board[3][2] = WHITE_KING

    move = all_legal_moves(board, BLACK)[0]

    new_board = apply_move_to_board(board, move)

    # Original piece removed
    assert new_board[2][1] == EMPTY

    # Captured king removed
    assert new_board[3][2] == EMPTY

    # Capturing piece promoted to king
    assert new_board[4][3] == BLACK_KING