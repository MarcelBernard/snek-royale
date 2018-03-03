import bottle
import os
import pprint

from .snake_control import SnakeHighCommand
from .states import FeedingState


snake_commanders = dict()


@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    print('STARTING++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print()
    print()
    print(data)

    global snake_commanders
    snake_commanders[int(data.get('game_id'))] = SnakeHighCommand([FeedingState],
                                                             data.get('width'),
                                                             data.get('height'),
                                                             data.get('game_id'))
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(snake_commanders)

    head_url = 'https://github.com/sendwithus/battlesnake-server/blob/master/assets/static/images/snake/head/tongue.svg'
    print()
    print()
    print('END STARTING++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    return {
        'color': '#00FF00',
        'taunt': 'AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH!',
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    print('SNAKE COMMANDERS++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    data = bottle.request.json
    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(snake_commanders)
    print(snake_commanders)
    print('JEFFO DAVO STEPH MARCEL')
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    for item in data.items():
        print(item)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    global snake_commanders
    snake_commander = snake_commanders[int(data.get('id'))]
    next_move = snake_commander.get_move(data)

    return {
        'move': next_move,
        'taunt': 'AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH'
    }


# @bottle.post('/end')
# def death_log():
#     data = bottle.request.json
#     with open('death_log.txt', 'a') as f:
#         f.write(data)
#
#     del snake_commanders[data.get('game_id')]


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=True)

    # start_data = {
    #     "game_id": 1,
    #     "width": 20,
    #     "height": 20
    # }
    #
    # start(start_data)
    # import json
    #
    # with open('test_input.json') as f:
    #     # data = f.read()
    #     move_data = json.load(f)

    # move(move_data)
