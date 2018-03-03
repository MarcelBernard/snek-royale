from enum import Enum
import numpy as np

class BoardMarks(Enum):
    EMPTY = 0
    FOOD = 1
    MY_BODY = 2
    MY_HEAD = 3
    ENEMY_BODY = 4
    ENEMY_HEAD = 5


class SnakeHighCommand:
    def __init__(self, states, board_width, board_height, game_id):
        self.states = states
        self.board = np.zeros((board_width, board_height), dtype=int)
        self.game_id = game_id

    def get_move(self, board_state):
        """Determine next move"""
        self.parse_board_state(board_state)

        highest_eval = -1
        winner_state = None
        for state in self.states:
            evaluation = state.eval(board_state)
            if evaluation > highest_eval:
                highest_eval = evaluation
                winner_state = state

        return winner_state.next_move()

    def parse_board_state(self, board_state):
        """Load board state into numpy array"""
        pass
