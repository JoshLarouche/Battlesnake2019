from collections import deque
import numpy as np
'''
0 = looking for food
1 = count the available space
2 = check if we can see our tail  (unused)
'''
#breadth first search floodfill to find a goal
def bfs(board, start, foodFind, tail):
    count = 1
    queue = deque()
    queue.append(start)
    closed = np.copy(board)#check for curiosity what type is close maybe set
    while queue:
        #print('here')
        count = count + 1
        current = queue.popleft()
        closed[current[0]][current[1]] = -1

        #if found food
        if board[current[0]][current[1]] == 2 and foodFind == 0:
            return current

        #if found tail
        if current[0] == tail[0] and current[1] == tail[1] and foodFind == 2:
            return True

        #move through board for algorithm
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

            '''if neighbour[0] == 15 or neighbour[1] == 15:
                continue'''

            #if not wall
            if closed[neighbour[0]][neighbour[1]] != -1:
                queue.append(neighbour)
                closed[neighbour[0]][neighbour[1]] = -1

    #return count of available space
    if foodFind == 1:
        return count

    return False

'''from collections import deque


def bfs(graph, root):
    visited, queue = set(), deque([root])
    while queue: 
        vertex = queue.popleft()
        for neighbour in graph[vertex]: 
            if neighbour not in visited:

                visited.add(neighbour) 
                queue.append(neighbour)
    return visited'''

#tester main
if __name__ == '__main__':
    board = np.zeros((19, 19), dtype=int)
    board[10][10] = 2
    test = bfs(board, (3, 3))
    print(test)
