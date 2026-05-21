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
# Direction represents changes in rows and cols (row,col)
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
def find_piece_normal_moves(board, move):

    row, col = move["path"][-1] # Current position of the piece
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

        # Create new move and append the possible moves in the 'move' list
        new_move = make_move(move["path"] + [(new_row, new_col)], move["captures"], promotes=promotes)

        moves.append(new_move)

    return moves

# To find all CAPTUREmoves for one piece
def find_piece_captures(board, move):

    row, col = move["path"][-1] # Current position of the piece
    piece = board[row][col] # Determine the piece
    path = move["path"]
    captures = move["captures"]
    player = piece_owner(piece) # Determine the player

    moves = [] # To store moves

    # Iterate over movement directions for the piece to generate possible capture moves
    for row_change, col_change in movement_directions(piece):
        
        # Compute jumped row and col, and landing rown and col after possible capturing
        jumped_row = row + row_change # for opponent piece
        jumped_col = col + col_change # for opponent piece

        landing_row = row + (2 * row_change) # for moving piece
        landing_col = col + (2 * col_change) # for moving  piece
        
        # Check whether landing point is inside the board
        if not inside_board(landing_row, landing_col):
            continue

        # Determine opponent piece and landing point for the moving piece
        jumped_piece = board[jumped_row][jumped_col] 
        landing_piece = board[landing_row][landing_col]

        # Check if capturing opponent piece or landing point is empty
        if piece_owner(jumped_piece) != -player or landing_piece != EMPTY:
            continue

        # New board state after capturing     
        new_board = [row[:] for row in board] # Copy the board

        new_board[row][col] = EMPTY # Empty the starting point
        new_board[jumped_row][jumped_col] = EMPTY # Empty the captured piece
        new_board[landing_row][landing_col] = piece # Move the piece to landing point


        # Add new path to path list, and capture moves to capture list
        new_path = path + [(landing_row, landing_col)]
        new_captures = captures + [(jumped_row, jumped_col)]

        # Check if capturing lead to 'regicide'
        # IF it is a normal piece, and capturing a king 
        normal_piece_to_regicide = abs(piece) == 1 and abs(jumped_piece) == 2

        # if normal piece reach the king row during a capture
        normal_piece_to_promote = check_promote(piece, landing_row)

        # If 'regicide' occurs, create the new move and append to 'moves' list
        # Stop capturing 
        if normal_piece_to_regicide:
            moves.append(make_move(new_path, new_captures, regicide=True, promotes=True))
            continue

        # If 'promote' occurs, create the new move and append to 'moves' list
        # Stop capturing 
        if normal_piece_to_promote:
            moves.append(make_move(new_path, new_captures, regicide=False, promotes=True))
            continue
        
        new_move = make_move(new_path, new_captures)
        
        # Check if there anymore possible capturing recursively
        # Every time the piece capturing, continue searching from the new landing point     
        continue_moves = find_piece_captures(new_board, new_move)

        # IF another captures available, extend the 'moves' list for every possible capturing
        if continue_moves:
            moves.extend(continue_moves)
        # Otherwise, only append the capture to the 'moves' list
        else:
            moves.append(new_move)

    return moves

# Returns all legal moves for a player
def all_legal_moves(board, player):

    capture_moves = [] # To store capture moves
    normal_moves = [] # To store normal moves

    # Iterate through the board rows and cols
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            piece = board[row][col] # Determine the possible piece

            # Check if piece belongs to player
            if piece_owner(piece) != player:
                continue
            
            start_move = make_move([(row, col)], [])

            # Find possible capture moves
            captures = find_piece_captures(board, start_move)

            # If any possible capture, extend 'capture_moves' list
            if captures:
                capture_moves.extend(captures)
            # Otherwise find normal moves and extend 'normal_moves' list
            else:
                normal_moves.extend(find_piece_normal_moves(board, start_move))

    # If at least one capture exists, only return 'capture_moves' list
    if capture_moves:
        return capture_moves

    # Otherwise return 'normal_moves' list
    return normal_moves

# Define apply_move_to_board function
# To apply the move into board to return the new board
def apply_move_to_board(board, move):
    
    # Copy to board
    new_board = [row[:] for row in board]

    # Extract start and end, rows and cols
    start_row, start_col = move["path"][0]
    end_row, end_col = move["path"][-1]

    # Create the piece and find the player
    piece = new_board[start_row][start_col]
    player = piece_owner(piece)

    # Remove the moving piece from starting point
    new_board[start_row][start_col] = EMPTY

    # Remove all captured enemies
    for captured_row, captured_col in move["captures"]:      
        new_board[captured_row][captured_col] = EMPTY

    # If the move promotion, upgrade the piece with a king
    # This covers promotion and the regicide
    if move["promotes"]:
        piece = 2 * player

    # Put the piece on end point
    new_board[end_row][end_col] = piece

    return new_board

# Returns successors pair (move, state)
# To determine what board state that move creates
def compute_successor_pairs(state):

    board, player = state # Unpack board and player

    # Compute all possible legal moves
    legal_moves = all_legal_moves(board, player)

    successor_pairs = [] # To store pairs

    # Iterate over legal_moves
    for move in legal_moves:

        new_board = apply_move_to_board(board, move) # Determine new board after move
        next_player = -player # Change the plater
        new_state = (new_board, next_player) # Determine new state

        # Append (move, new_state) pairs to 'successor_pairs' list
        successor_pairs.append((move, new_state))

    return successor_pairs