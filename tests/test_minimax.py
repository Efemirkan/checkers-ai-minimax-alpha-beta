import sys
import os
import copy

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from constants import *
from board import *
from ai import *
from moves import compute_successor_pairs

def test_minimax_returns_legal_move():
  
    board =  empty_board()

    # Place a black piece
    board[2][1] = BLACK
    board[5][4] = WHITE

    state = (board, BLACK)

    pairs= compute_successor_pairs(state)
    legal_moves = [move for move, _ in pairs]

    assert legal_moves

    _, selected_move = minimax(state=state, depth=0, depth_limit=3, alpha=-INF, beta=INF)


    assert selected_move is not None
    assert selected_move in legal_moves

def test_minimax_does_not_change_original_board():
    
    board =  empty_board()

    # Place a black piece
    board[2][1] = BLACK
    board[5][4] = WHITE

    state = (board, BLACK)

    original_board = copy.deepcopy(state[0])
    original_player = state[1]

    minimax(state=state, depth=0, depth_limit=3, alpha=-INF, beta=INF)

    assert state[0] == original_board

    assert state[1] == original_player