from collections import deque
import numpy as np

'''
OBJECTIVE LEGEND:
0 = looking for food
1 = count the available space
2 = check if we can see our tail (unused)
'''

#breadth first search floodfill to find a goal
def bfs(board, start, objective, tail):
    count = 1
    queue = deque()
    queue.append(start)
    closed = np.copy(board)

    #priority queue for bfs loop
    while queue:
        count = count + 1
        current = queue.popleft()
        closed[current[0]][current[1]] = -1

        #if found food
        if board[current[0]][current[1]] == 2 and objective == 0:
            return current

        #if found tail
        if current[0] == tail[0] and current[1] == tail[1] and objective == 2:
            return True

        #move through board for algorithm
        for x in range(0, 4):

            # left
            if x is 0:
                if current[0] == 0:
                    continue
                neighbour = (current[0] - 1, current[1])

            # up
            if x is 1:
                if current[1] == 0:
                    continue
                neighbour = (current[0], current[1] - 1)

            # right
            if x is 2:
                if current[0] == board.shape[0] - 1:
                    continue
                neighbour = (current[0] + 1, current[1])

            # down
            if x is 3:
                if current[1] == board.shape[1] - 1:
                    continue
                neighbour = (current[0], current[1] + 1)

            #if not wall
            if closed[neighbour[0]][neighbour[1]] != -1:
                queue.append(neighbour)
                closed[neighbour[0]][neighbour[1]] = -1

    #return count of available space
    if objective == 1:
        return count

    return False

#tester main
if __name__ == '__main__':
    board = np.zeros((19, 19), dtype=int)
    board[10][10] = 2
    test = bfs(board, (3, 3))
    #print(test)
