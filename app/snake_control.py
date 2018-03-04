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
    def __init__(self, TileType, snakeID, weight, position):
        # The type of tile
        self.type = TileType
        # ID of the snake.  If not applicable, ID will be ""
        self.snakeID = snakeID
        # Weight of the tile used by a path finding algorithm
        self.weight = weight
        # position = (x,y) on game board
        self.position = position

    def clear_node(self):
        self.type = TileType.EMPTY
        self.snakeID = ''
        self.weight = 0

# Contains information about our snake
class MySnake:
    def __init__(self, positions, health, previous_move, snake_id, length, name, taunt):
        # Position of the head with x, y coord
        self.head = positions[0]
        # List of positions with x, y coords
        self.positions = positions
        # Health of our snake, max is 100 and 0 is dead
        self.health = health
        # Previous move : 'up' 'down' 'left' 'right'
        self.previous_move = previous_move
        self.snake_id = snake_id
        self.length = length
        self.name = name
        self.taunt = taunt


# Controls processing move requests and returning a move
class SnakeHighCommand:
    def __init__(self, states, board_width, board_height, game_id):
        self.states = states
        self.game_id = game_id
        self.turn_num = 0
        self.my_snake = MySnake([0], None, None, None, None, None, None)
        self.other_snakes = None
        self.food_positions = []

        # 2D array of nodes representing the board # TODO: Add nodes, not ints
        self.board = np.empty((board_width, board_height), dtype=object)
        for i in range(board_width):
            for j in range(board_height):
                self.board[i][j] = TileNode(TileType.EMPTY, 0, 0, (0, 0))

    # Gets the next move (200 ms max response)
    def get_move(self, data):
        self.parse_board_state(data)

        highest_eval = -1
        winner_state = None

        # Ask each state for its evaluation value, tracking the state with the highest value
        for state in self.states:
            evaluation = state.eval(snake_high_command=self)
            if evaluation > highest_eval:
                highest_eval = evaluation
                winner_state = state

        return winner_state.next_move()

    # Populates the board with node information
    def parse_board_state(self, data):
        """Load board state into numpy array"""
        self.turn_num = data['turn']

        my_snake = data['you']
        self.my_snake.health = my_snake['health']
        self.my_snake.id = my_snake['id']
        self.my_snake.length = my_snake['length']
        self.my_snake.name = my_snake['name']
        self.my_snake.taunt = my_snake['taunt']
        self.my_snake.positions = [(my_pos['x'], my_pos['y']) for my_pos in my_snake['body']['data']]
        self.my_snake.head = self.my_snake.positions[0]

        self.other_snakes = self.get_other_snakes(data['snakes']['data'])
        self.food_positions = [(food_pos['x'], food_pos['y']) for food_pos in data['food']['data']]
        self.fill_board()

    def get_other_snakes(self, snakes):
        other_snakes = {}
        for snake_data in snakes:
            positions = [(body_pos['x'], body_pos['y']) for body_pos in snake_data['body']['data']]
            new_snake = OtherSnake(snake_data['id'],
                                   snake_data['health'],
                                   snake_data['length'],
                                   snake_data['name'],
                                   snake_data['taunt'],
                                   positions)

            other_snakes[new_snake.snake_id] = new_snake

        return other_snakes

    def fill_board(self):
        board = self.board
        for (x, y), tile in np.ndenumerate(board):
            tile.clear_node()

        for food in self.food_positions:
            board[food[0], food[1]].type = TileType.FOOD

        for snake in self.other_snakes.values():
            for position in snake.positions:
                tile = board[position[0], position[1]]
                tile.type = TileType.ENEMY_BODY
                tile.snakeID = snake.snake_id
                tile.weight = 100

        my_snake = self.my_snake
        for position in my_snake.positions:
            tile = board[position[0], position[1]]
            tile.type = TileType.MY_BODY
            tile.snakeID = my_snake.snake_id
            tile.weight = 100


class OtherSnake:
    def __init__(self, snake_id, health, length, name, taunt, positions):
        self.snake_id = snake_id
        self.health = health
        self.length = length
        self.name = name
        self.taunt = taunt
        self.positions = positions