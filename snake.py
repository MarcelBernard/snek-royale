import bottle
import os


@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }

def process_move(data)
    grid = [[SAFE for col in xrange(data['height'])] for row in xrange(data['width'])]

    for x in xrange(len(grid)):
        grid[x][0] = WALL
        grid[x][len(grid) - 1] = WALL

    for y in xrange(len(grid[0])):
        grid[0][y] = WALL
        grid[len(grid[0]) - 1][y] = WALL

    for snake in data['snakes']:
        if snake['id'] == data['you']:
            mysnake = snake
        for coord in snake['coords']:
            grid[coord[0]][coord[1]] = SNAKE_BODY
            possible_buffer = adjacent_spaces(coord[0],coord[1])
            snake_buffer = []
            for space in possible_buffer:
                if check_if_valid(space[0],space[1],grid):
                    if grid[space[0]][space[1]] < SNAKE_BODY:
                        grid[space[0]][space[1]] = DANGER_ZONE
        snake_head = snake['coords'][0]

        potential_danger = adjacent_spaces(snake_head[0],snake_head[1])
        danger = []

        #for dangerous_places in potential_danger:
        #    if check_if_valid(dangerous_places[0], dangerous_places[1], grid):
        #        if grid[dangerous_places[0]][dangerous_places[1]] == SAFE:
        #            grid[dangerous_places[0]][dangerous_places[1]] = DANGER_ZONE

        grid[snake_head[0]][snake_head[1]] = SNAKE_HEAD

    for f in data['food']:
        grid[f[0]][f[1]] = FOOD

    return mysnake, grid



@bottle.post('/move')
def move():
    data = bottle.request.json

    mysnake, grid = init(data)

    # TODO: Do things with data

    directions = ['up', 'down', 'left', 'right']
    direction = 'up'

    return {
        'move': direction,
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=True)