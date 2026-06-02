import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from constants import *
from board import *
from moves import all_legal_moves


# Test, ownership is correctly identified
def test_piece_owner():

    assert piece_owner(BLACK) == BLACK
    assert piece_owner(BLACK_KING) == BLACK

    assert piece_owner(WHITE) == WHITE
    assert piece_owner(WHITE_KING) == WHITE

    assert piece_owner(EMPTY) == EMPTY


# Test, pieces count
def test_count_player_pieces():

    board = empty_board()

    board[0][1] = BLACK
    board[1][2] = BLACK_KING
    board[6][1] = WHITE

    assert count_player_pieces(board, BLACK) == 2
    assert count_player_pieces(board, WHITE) == 1

# Test, king count
def test_count_player_kings():

    board = empty_board()

    board[1][2] = BLACK_KING
    board[6][1] = WHITE_KING
    board[0][1] = BLACK

    assert count_player_kings(board, BLACK) == 1
    assert count_player_kings(board, WHITE) == 1

# Test, if white has no remaining pieces, black wins
def test_winner_no_pieces():

    board = empty_board()

    board[0][1] = BLACK

    assert count_player_pieces(board, WHITE) == 0


# Test, If White has no legal moves, black wins
def test_winner_no_legal_moves():

    board = empty_board()

    board[0][1] = WHITE
    board[1][0] = BLACK
    board[1][2] = BLACK

    moves = all_legal_moves(board, WHITE)

    assert moves == []