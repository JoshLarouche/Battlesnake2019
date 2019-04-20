from collections import deque
import numpy as np

#find node that will free up next if trapped in too small space
def exitFinder(data, board, start):
    '''
    0 = open node
    -1 = wall node
    -2 = checked neighbour open node
    -3 = checked wall
    '''
    queue = deque()
    queue.append(start)
    closed = np.copy(board)#check for curiosity what type is closed maybe set
    closed[data['you']['body'][-1]['x']][data['you']['body'][-1]['y']] = -1
    walls = [] #use something other than list maybe
    while queue:
        current = queue.popleft()
        closed[current[0]][current[1]] = -2 # checked boardspace

        #look around head for options
        for x in range(0, 4):
            if x == 0:
                if current[0] > 0:
                    neighbour = (current[0] - 1, current[1])
                else:
                    continue
            if x == 1:
                if current[1] > 0:
                    neighbour = (current[0], current[1] - 1)
                else:
                    continue
            if x == 2:
                if current[0] < board.shape[0] - 1:
                    neighbour = (current[0] + 1, current[1])
                else:
                    continue
            if x == 3:
                if current[1] < board.shape[1] - 1:
                    neighbour = (current[0], current[1] + 1)
                else:
                    continue

            #look at a wall piece and assign a turn decay timer for when the node will free up
            if closed[neighbour[0]][neighbour[1]] == -1:
                closed[neighbour[0]][neighbour[1]] = -3 # checked wall
                for snake in range(0, len(data['board']['snakes'])): #change to pythonic obligation
                    for body in range(0, len(data['board']['snakes'][snake]['body'])):
                        if data['board']['snakes'][snake]['body'][body]['x'] == neighbour[0] and data['board']['snakes'][snake]['body'][body]['y'] == neighbour[1]:
                            decayTimer = len(data['board']['snakes'][snake]['body']) - body
                            walls.append([decayTimer, (neighbour[0], neighbour[1])])

            #move through space to find wall nodes
            if closed[neighbour[0]][neighbour[1]] > -1:
                queue.append(neighbour)
                closed[neighbour[0]][neighbour[1]] = -2

    #exitNode is wall node with shortest decay timer
    exitNode = walls[0]
    for wall in walls:
        if wall[0] < exitNode[0]:
            exitNode = wall
    return exitNode

#tester main
if __name__ == '__main__':
    board = np.zeros((19, 19), dtype=int)
    board[10][10] = 2
    test = bfs(board, (3, 3))
    print(test)