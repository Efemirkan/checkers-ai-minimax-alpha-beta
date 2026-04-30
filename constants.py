# Assign constant variables
EMPTY = 0
BLACK = 1
BLACK_KING = 2
WHITE = -1
WHITE_KING = -2
BOARD_SIZE = 8
INF = 1000000  # Large constant, initial value for alpha-beta pruning

# Initialise the board 
initial_board = [[0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [-1, 0, -1, 0, -1, 0, -1, 0],
                 [0, -1, 0, -1, 0, -1, 0, -1],
                 [-1, 0, -1, 0, -1, 0, -1, 0]]

# Initialise the state
# (board, player_to_move)
# BLACK starts first
initial_state = (initial_board, BLACK)