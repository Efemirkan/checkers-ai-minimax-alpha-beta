from constants import *
from board import *
from moves import all_legal_moves

### GAME ENDING ###

# To check whether game ending or continue
def game_ending(state, no_capture_counter=0):

    board = state[0] # Unpack the board

    if no_capture_counter >= 40:
        return 0

    # Count each player pieces
    black_pieces = count_player_pieces(board, BLACK)
    white_pieces = count_player_pieces(board, WHITE)
    black_kings= count_player_kings(board, BLACK)
    white_kings= count_player_kings(board, WHITE)

    # If one of them does not have any piece, opponent win
    if black_pieces == 0:
        return WHITE
    if white_pieces == 0:
        return BLACK
          
    # Check if both BLACK and WHITE has 1 player each and if these are kings, DRAW
    if black_pieces == 1 and white_pieces == 1 and black_kings == 1 and white_kings == 1:
        return 0
    
    # Check if one of the player does not have legal moves, opponent win
    if not all_legal_moves(board, BLACK):
        return WHITE
    if not all_legal_moves(board, WHITE):
        return BLACK

    # Otherwise game continue
    return None