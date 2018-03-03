# Handles getting food for the snake
from snake_control import TileType, TileNode, Moves
import numpy as np


class FeedingState:
    """It's feeding time"""
    def __init__(self):
        self._next_move = None

    def eval(self, my_snake, other_snakes, board):
        eval_val = 0
        eval_val += 100 - my_snake.health

        # TODO: get info about food nearby and add that to the eval
        
        return eval_val

    def next_move(self): return self._next_move


class CircleTailState:
    # TODO: sick movie quote
    def __init__(self):
        self._next_move = None

    def eval(self, my_snake, other_snakes, board):
        pass

    def next_move(self): return self._next_move


class CounterBloodfillState:
    # TODO: sick movie quote
    def __init__(self):
        self._next_move = None

    def eval(self, my_snake, other_snakes, board):
        pass

    def next_move(self): return self._next_move


class BloodfillState:
    """Time to get filled"""
    def __init__(self):
        self._next_move = None
        self._prev_move = None

    def quadrant(self, game_board, start_node, end_node_position):
        visited, queue = set(), [start_node]
        while queue:
            vertex = queue.pop(0)
            if vertex.position not in visited:
                visited.add(vertex.position)
            else:
                continue
            # put neighbours in queue
            if vertex.position[0] < end_node_position[0]:
                # add right neighbour
                right_x = vertex.position[0] + 1
                if right_x < len(game_board):
                    neighbour = game_board[right_x][vertex.position[1]]
                    if (neighbour.type == 0):
                        queue.append(neighbour)
            else:
                # add left neighbour
                left_x = vertex.position[0] - 1
                if left_x >= 0:
                    neighbour = game_board[left_x][vertex.position[1]]
                    if (neighbour.type == 0):
                        queue.append(neighbour)
            if vertex.position[1] < end_node_position[1]:
                # add bottom neighbour
                down_y = vertex.position[1]  + 1
                if down_y < len(game_board[0]):
                    neighbour = game_board[vertex.position[0]][down_y]
                    if (neighbour.type == 0):
                        queue.append(neighbour)
            else:
                # add top neighbour
                up_y = vertex.position[1] - 1
                if up_y >= 0:
                    neighbour = game_board[vertex.position[0]][up_y]
                    if (neighbour.type == 0):
                        queue.append(neighbour)
        return len(visited)


    def eval(self, MySnake, game_board):
        if MySnake.previous_move is None:
            return 0

        # check which quadrant has the most open space
        upper_left = self.quadrant(game_board, MySnake.head, (0,0))
        upper_right = self.quadrant(game_board, MySnake.head, ((len(game_board) - 1),0))
        lower_left = self.quadrant(game_board, MySnake.head, (0, (len(game_board[0]) - 1)))
        lower_right = self.quadrant(game_board, MySnake.head, ((len(game_board) - 1), (len(game_board[0]) - 1)))
        left = upper_left + lower_left
        right = upper_right + lower_right
        up = upper_left + upper_right
        down = lower_left + lower_right
        direction_values = [left, right, up, down]
        directions = [Moves.LEFT, Moves.RIGHT, Moves.UP, Moves.DOWN]
        self._next_move = directions[np.argmax(direction_values)]

        if MySnake.length < 5:
            return 50
        else:
            val = (MySnake.length * 5) + 50
            if val > 99:
                return 99
            else:
                return val

    def next_move(self): return self._next_move


class KillState:
    """hasta la vista, baby"""
    def __init__(self):
        self._next_move = None

    def eval(self, my_snake, other_snakes, board):
        pass

    def next_move(self): return self._next_move
