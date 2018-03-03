# Handles getting food for the snake
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

    def eval(self, my_snake, other_snakes, board):
        pass

    def next_move(self): return self._next_move


class KillState:
    """hasta la vista, baby"""
    def __init__(self):
        self._next_move = None

    def eval(self, my_snake, other_snakes, board):
        pass

    def next_move(self): return self._next_move
