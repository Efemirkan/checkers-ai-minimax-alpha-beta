from constants import *
from rules import game_ending

# To score the player using piece values
# Normal pieces 100, Kings 175
def evaluate_board(board):

    score = 0 # Initialize the score

    # Iterate through the board rows and cols
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            # Determine the piece
            piece = board[row][col]

            # Check the piece and score
            if piece == BLACK:
                score += 100
            elif piece == BLACK_KING:
                score += 175

            # Negative scores for whites
            elif piece == WHITE:
                score -= 100
            elif piece == WHITE_KING:
                score -= 175

    return score

# Reward normal pieces for moving towards promotion use positional feature 
def evaluate_positional_feature(board):

    score = 0

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            piece = board[row][col]

            if piece == BLACK:

                # Reward pieces moving towards promotion
                score += row * 6

                # Keep back row protected
                if row == 0:
                    score += 30

            elif piece == WHITE:

                # Reward pieces moving towards promotion
                score -= (BOARD_SIZE - 1 - row) * 6

                # Keep back row protected
                if row == BOARD_SIZE - 1:
                    score -= 30

    return score

# Compute total heuristic score to estimate how good a board position is
def heuristic(state):

    # Find the winner of the state
    game_winner = game_ending(state)

    # Check if game finish
    # If BLACK is winner return INF
    if game_winner == BLACK:
        return INF

    # If WHITE is winner return -INF
    if game_winner == WHITE:
        return -INF

    # Handle with if both BLACK and WHITE has 1 KING player each
    if game_winner == 0:
        return 0

    board = state[0] # Unpack the board

    # Calculate the total score for four evaluation
    score = 0
    score += evaluate_board(board)
    score += evaluate_positional_feature(board)

    return score