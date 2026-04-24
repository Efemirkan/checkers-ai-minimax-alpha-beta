from constants import *

### INITIALISE BOARD AND STATE ###
initial_board = [[0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [-1, 0, -1, 0, -1, 0, -1, 0],
                 [0, -1, 0, -1, 0, -1, 0, -1],
                 [-1, 0, -1, 0, -1, 0, -1, 0]]

# The state stores:
# (board, player_to_move)
# BLACK starts first
initial_state = (initial_board, BLACK)


# To check row and column are on the board
def inside_board(row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


# Returns piece owner
def piece_owner(piece):

    if piece > 0:
        return BLACK
    if piece < 0:
        return WHITE
    return EMPTY


# To count how many pieces a player has left
def count_player_pieces(board, player):

    count = 0  # Initialize count as 0

    # Iterate through the board rows and cols
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            # Check if piece belongs the player
            if piece_owner(board[row][col]) == player:
                count += 1  # Increase by one
    return count

# To check the piece to be promoted on the row
def check_promote(piece, row):
    # If is not a normal piece, Not promote
    if not abs(piece) == 1:
        return False

    # Determine the plater
    player = piece_owner(piece)

    # Check if piece and player in specific row, Tp promote
    if (player == BLACK and row == BOARD_SIZE - 1) or (player == WHITE and row == 0):
        return True

    return False