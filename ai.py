from constants import *
from rules import game_ending
import random

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

# To scores the move by importance of the move
def score_moves(move):

    score = 0 # Initialize the score

    # Add 100 times length of captures in the move
    score += len(move["captures"]) * 100

    # Iff move include regicide add 200
    if move["regicide"]:
        score += 200

    # Iff move include promotes add 80
    if move["promotes"]:
        score += 80

    return score

# Make descending order by score for successor_pairs
# To put most important moves first such as captues, regicide, promotes
def order_successor_pairs(successor_pairs):

    scored_pairs = [] # To store pairs

    # Iterate over successor_pairs to compute score for each
    for pair in successor_pairs:

        move = pair[0] # Unpack move

        # Append successor pair and the score of the move to leads that state
        scored_pairs.append((score_moves(move), pair)) 

    # Order the pairs by descending
    scored_pairs.sort(reverse=True, key=lambda item: item[0])

    ordered_pairs = [] # To store pairs

    # Iterate over scored_pairs to remove the score after ordering
    for item in scored_pairs:
        ordered_pairs.append(item[1])

    return ordered_pairs

def minimax(state, depth, depth_limit, alpha, beta, no_capture_counter=0):

    board, player = state  # Unpack board and player

    game_winner = game_ending(state, no_capture_counter)  # Determine winner
      
    # Stop if maximum depth is reached or the game is finished
    if depth == depth_limit or game_winner is not None:
        if game_winner == 0:
            return 0, None
        return heuristic(state), None

    # Compute all successor pairs
    successor_pairs = compute_successor_pairs(state)

    # If there are no legal moves, means terminal state and return evaluation
    if len(successor_pairs) == 0:
        return heuristic(state), None

    # Order successor pairs by moves score
    successor_pairs = order_successor_pairs(successor_pairs)

    # BLACK is maximizing player
    if player == BLACK:

        
        best_score = -INF # Initialize best score for maximizing player
        best_moves = [] # To store best moves

        # Iterate over for all successor_pairs and resulting states
        for move, child_state in successor_pairs:

            new_counter = 0 if move["captures"] else no_capture_counter + 1

            # Recursively evaluate the child state
            score, _ = minimax(child_state, depth + 1, depth_limit, alpha, beta, new_counter)

            # If this move has better score, update best_score and reset best_move
            if score > best_score:
                best_score = score
                best_moves = [move]

            # If this move has the same score as best_score, store as alternative
            elif score == best_score:
                best_moves.append(move)

            # Update alpha
            alpha = max(alpha, best_score)

            # If alpha is greater than or equal to beta, no need to explore further, prune branch
            if alpha >= beta:
                break
        
        # If no valid moves, return current best_score
        if len(best_moves) == 0:
            return best_score, None

        # Otherwise randomly choose one of the best moves
        return best_score, random.choice(best_moves)

    # WHITE is minimizing player
    best_score = INF # Initialize best score for minimizing player
    best_moves = [] # To store best moves

    # Iterate over for all successor_pairs and resulting states
    for move, child_state in successor_pairs:

        new_counter = 0 if move["captures"] else no_capture_counter + 1

        # Recursively evaluate the child state
        score, _ = minimax(child_state, depth + 1, depth_limit, alpha, beta, new_counter)

        # If this move has smaller score, update best_score and reset best_move
        if score < best_score:
            best_score = score
            best_moves = [move]

        # If this move has the same score as best_score, store as alternative
        elif score == best_score:
            best_moves.append(move)

        # Update beta
        beta = min(beta, best_score)

        # If alpha is greater than or equal to beta, no need to explore further, prune branch
        if alpha >= beta:
            break
    
    # Otherwise randomly choose one of the best moves
    return best_score, random.choice(best_moves)