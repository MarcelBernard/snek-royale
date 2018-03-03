from enum import Enum
import numpy as np

# Types of board tiles
class TileType(Enum):
    EMPTY = 0
    FOOD = 1
    MY_BODY = 2
    MY_HEAD = 3
    ENEMY_BODY = 4
    ENEMY_HEAD = 5

# Available moves for the snake
class Moves(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

# Contains information about a tile on the board
class TileNode:
    def __init__(self, TileType, snakeID, weight):
        # The type of tile
        self.type = TileType
        # ID of the snake.  If not applicable, ID will be ""
        self.snakeID = snakeID
        # Weight of the tile used by a path finding algorithm
        self.weight = weight

# Contains information about our snake
class MySnake:
    def __init(self, positions, health, previous_move):
        # Position of the head with x, y coord
        self.head = positions[0]
        # List of positions with x,y coords
        self.positions = positions
        # Health of our snake
        self.health = health
        # Previous move
        self.previous_move = previous_move

# Controls processing move requests and returning a move
class SnakeHighCommand:
    def __init__(self, states, board_width, board_height, game_id):
        # List of states we will be using 
        self.states = states
        # 2D array of nodes representing the board # TODO: Add nodes, not ints
        self.board = np.zeros((board_width, board_height), dtype=int)
        # ID of this game
        self.game_id = game_id

    # Gets the next move (200 ms max response)
    def get_move(self, board_state):
        # parse the board state
        self.parse_board_state(board_state)

        # Tracks the highest evaluation value
        highest_eval = -1
        # Tracks the state with the highest evaluation value
        winner_state = None

        # Ask each state for its evaluation value, tracking the state with the highest value
        for state in self.states:
            evaluation = state.eval(board_state)
            if evaluation > highest_eval:
                highest_eval = evaluation
                winner_state = state

        # Based on the winning state, get the next move from that state
        return winner_state.next_move()

    # Populates the board with node information
    def parse_board_state(self, board_state):
        """Load board state into numpy array"""
        pass
