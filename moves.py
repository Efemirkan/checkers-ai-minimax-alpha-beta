from constants import *
from board import *

### DEFINE MOVE AND DIRECTIONS ###

# Define make_move function to create a MOVE
def make_move(path, captures, regicide=False, promotes=False):

    # Move is represented in dictionary
    return {"path": path, # List of (row, col) the piece visit
            "captures": captures, # List of opponents (row, col) the piece capture
            "regicide": regicide, # True if normal piece capture opponent king
            "promotes": promotes, # True if the piece promote
            }

# Returns the directions
# Direction represents changes in rows and cols
def movement_directions(piece):

    # Black moves down
    if piece == BLACK:
        return [(1, -1), (1, 1)]
    # White moves up
    if piece == WHITE:
        return [(-1, -1), (-1, 1)]
    
    # Kings move in both directions
    return [(1, -1), (1, 1), (-1, -1), (-1, 1)]

# To find NORMAL moves for one piece 
def find_piece_normal_moves(board, row, col):

    piece = board[row][col] # Determine the piece
    moves = [] # To store moves

    # Iterate over movement directions for the piece to generate possible moves
    for row_change, col_change  in movement_directions(piece):
        
        # Compute new row and new col after possible move
        new_row = row + row_change
        new_col = col + col_change

        # Check whether ending point is inside the board
        if not inside_board(new_row, new_col):
            continue
        
        # Check whether ending point is empty
        if board[new_row][new_col] != EMPTY:
            continue

        # Check the piece to be promote on the row
        promotes = check_promote(piece, new_row)

        # Append the possibke moves in the 'move' list
        moves.append(make_move([(row, col), (new_row, new_col)], [], promotes=promotes))

    return moves