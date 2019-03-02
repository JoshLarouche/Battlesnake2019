import json
import os
import random
import bottle
import numpy as np
import math
from time import time

from . import api #ping_response, start_response, move_response, end_response testing4
from . import aStar
from . import bfs
from . import panic


@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return api.ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#7851A9"
    headType = "safe"
    tailType = "round-bum"
    #"#E8E8E8"

    return api.start_response(color, headType, tailType)


@bottle.post('/move')
def move():
    data = bottle.request.json

    startTime = time()
    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))
    boardSize = data['board']['height']
    board = np.zeros((boardSize, boardSize), dtype=int)
    #print(data['you']['body'][0]['x'], " ", data['you']['body'][0]['y'])
    for i in range(0, len(data['board']['snakes'])):
        for x in range(0, len(data['board']['snakes'][i]['body'])):
            board[data['board']['snakes'][i]['body'][x]['x']][data['board']['snakes'][i]['body'][x]['y']] = -1
    start = (data['you']['body'][0]['x'], data['you']['body'][0]['y'])
    for food in data['board']['food']:
        board[food['x']][food['y']] = 2
    length = len(data['you']['body'])
    board[data['you']['body'][-1]['x']][data['you']['body'][-1]['y']] = 0
    board[data['you']['body'][-2]['x']][data['you']['body'][-2]['y']] = -1
    tail = (data['you']['body'][-1]['x'], data['you']['body'][-1]['y'])
    print("first tail: ", tail)
    for i in range(0, len(data['board']['snakes'])):
        if math.fabs(data['board']['snakes'][i]['body'][0]['x'] - start[0]) + math.fabs(data['board']['snakes'][i]['body'][0]['y'] - start[1]) == 2 and len(data['board']['snakes'][i]['body']) >= length:
            print("enemy x: ", data['board']['snakes'][i]['body'][0]['x'])
            print("start x: ", start[0])
            if math.fabs(data['board']['snakes'][i]['body'][0]['x'] - start[0]) == 2:
                board[int((data['board']['snakes'][i]['body'][0]['x'] + start[0])/2)][start[1]] = -1
            elif math.fabs(data['board']['snakes'][i]['body'][0]['y'] - start[1]) == 2:
                board[start[0]][int((data['board']['snakes'][i]['body'][0]['y'] + start[1])/2)] = -1
            else:
                board[data['board']['snakes'][i]['body'][0]['x']][start[1]] = -1
                board[start[0]][data['board']['snakes'][i]['body'][0]['y']] = -1
 
            

    if data['you']['health'] > 25 and length > bfs.bfs(board, start, 1, tail) and bfs.bfs(board, start, 2, tail):
        exitNode = panic.exitFinder(data, board, start)
        goal = exitNode[1]
        direction = aStar.aStar(board, start, goal)
        if np.array_equal(direction, [-1, 0]):
            direction = 'left'
        elif np.array_equal(direction, [1, 0]):
            direction = 'right'
        elif np.array_equal(direction, [0, -1]):
            direction = 'up'
        elif np.array_equal(direction, [0, 1]):
            direction = 'down'
        return api.move_response(direction)

    '''if length >= bfs(board, start, False):#delete this but it is prototype cycling
        exitNode = panic.exitFinder(data, board, start)
        goal = exitNode[1]
        direction = aStar(board, start, goal)
        if np.array_equal(direction, [-1, 0]):
            direction = 'left'
        elif np.array_equal(direction, [1, 0]):
            direction = 'right'
        elif np.array_equal(direction, [0, -1]):
            direction = 'up'
        elif np.array_equal(direction, [0, 1]):
            direction = 'down'
        return api.move_response(direction)'''
    currentBest = [-1, -1]
    loop = True
    counter = 3
    deadWalls = []
    while loop:
        print('currentBest = ', currentBest)
        if counter == 0:
            direction = currentBest[1]
            break
        counter = counter - 1
        loop = False
        for x in deadWalls:
            board[x[0][0]][x[0][1]] = -1
        goal = bfs.bfs(board, start, 0, tail) #subscriptable error when goal is -1
        for x in deadWalls:
            board[x[0][0]][x[0][1]] = x[1]
        #could return -1 if there is plenty of space but no available food
        if goal == -1:
            direction = currentBest[1]
            longerCheck = bfs.bfs(board, start, 1, tail)
            for x in deadWalls:
                board[x[0][0]][x[0][1]] = -1
            print("panic board\n", board)
            if longerCheck <= currentBest[0] or trapped(board, start):
                break
            else:
                print('PANICKING')
                for x in deadWalls:
                    board[x[0][0]][x[0][1]] = -3
                exitNode = panic.exitFinder(data, board, start)
                for x in deadWalls:
                    board[x[0][0]][x[0][1]] = x[1]
                goal = exitNode[1]
        for x in deadWalls:
            board[x[0][0]][x[0][1]] = -1
        print("goal: ", goal)
        if not goal:
            goal = tail
        print("goal: ", goal)
        print("tail: ", tail)
        direction = aStar.aStar(board, start, goal)
        if direction[0] == 2:
            direction = find_exit(board, start)
            if direction[0] == 2:
                direction = currentBest[1]
                break
        if is_wall(board, start + direction):
            direction = find_exit(board, start)
            if direction[0] == 2:
                direction = currentBest[1]
                break

        for x in deadWalls:
            board[x[0][0]][x[0][1]] = x[1]
        print(direction)
        '''print(data['board']['height'])
        directions = ['up', 'down', 'left', 'right']
        direction = random.choice(directions)'''
        safetyCheck = bfs.bfs(board, start + direction, 1, tail)
        print('safetyCheck = ', safetyCheck)
        print('length = ', length)
        if safetyCheck < length: #add to length to increase pussiness, add food to path
            candidate = start + direction
            deadWalls.append((candidate, board[candidate[0]][candidate[1]]))
            print("deadWalls init: ", deadWalls)
            print(board)
            board[candidate[0]][candidate[1]] = -1
            areaCheck = []
            print("Candidate: ", candidate)
            print(board)
            print(candidate + (-1, 0))
            print(candidate + (1, 0))
            print(candidate + (0, -1))
            print(candidate + (0, 1))
            if not is_wall(board, candidate + (-1, 0)):
                print("areaCheck")
                areaCheck.append(bfs.bfs(board, candidate + (-1, 0), 1, tail))
            if not is_wall(board, candidate + (1, 0)):
                print("areaCheck")
                areaCheck.append(bfs.bfs(board, candidate + (1, 0), 1, tail))
            if not is_wall(board, candidate + (0, -1)):
                print("areaCheck")
                areaCheck.append(bfs.bfs(board, candidate + (0, -1), 1, tail))
            if not is_wall(board, candidate + (0, 1)):
                print("areaCheck")
                areaCheck.append(bfs.bfs(board, candidate + (0, 1), 1, tail))
            print(areaCheck)
            if areaCheck:
                checkMax = max(areaCheck)
            else:
                checkMax = 0
            board[candidate[0]][candidate[1]] = deadWalls[-1][1]
            if checkMax > currentBest[0]:
                currentBest = [checkMax, direction]
            loop = True

    print("Exit decision = ", direction)

    if np.array_equal(direction, [-1, 0]):
        direction = 'left'
    elif np.array_equal(direction, [1, 0]):
        direction = 'right'
    elif np.array_equal(direction, [0, -1]):
        direction = 'up'
    elif np.array_equal(direction, [0, 1]):
        direction = 'down'
    #else last resort rando

    responseTime = time() - startTime
    print(responseTime)
    return api.move_response(direction)

#def panic(data, board, start):

def is_wall(board, coord):
    if coord[0] == -1 or coord[0] == board.shape[0] or coord[1] == -1 or coord[1] == board.shape[1]:
        return True
    return board[coord[0]][coord[1]] == -1

def trapped(board, start):
    print("start: ", start)
    if is_wall(board, (start[0] - 1, start[1])) and is_wall(board, (start[0] + 1, start[1])) and is_wall(board, (start[0], start[1] - 1)) and is_wall(board, (start[0], start[1] + 1)):
        print("trapped")
        return True
    print("not trapped")
    return False

def find_exit(board, start):
    print("find_exit board:\n", board)
    if not is_wall(board, (start[0] - 1, start[1])):
        return (-1, 0)
    if not is_wall(board, (start[0] + 1, start[1])):
        return (1, 0)
    if not is_wall(board, (start[0], start[1] - 1)):
        return (0, -1)
    if not is_wall(board, (start[0], start[1] + 1)):
        return (0, 1)
    return (2, 2)

@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return api.end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
