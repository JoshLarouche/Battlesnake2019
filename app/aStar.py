import numpy as np
import math
import queue

#finds the direction to go after the aStar algorithm finds a path
def backPedal(cameFrom, start, goal):
	path = []
	curr = goal
	while curr[0] != -1:
		path.append(tuple(curr))
		curr = cameFrom[curr[0]][curr[1]]
	npPath = np.array(path[-2])
	npStart = np.array(start)
	direction = npPath - npStart
	print(path)
	return direction

#finds the shortest paths to a goal node from a start node
def aStar(board, start, goal): #combine with bfs for efficiency

	#set of checked nodes on the board
	closedSet = np.zeros(board.shape, dtype=int) #possibly change to np.copy for consistency
	for (x,y), value in np.ndenumerate(board):
		if value == -1:
			closedSet[x][y] = 1
	closedSet[start[0]][start[1]] = 0
	closedSet[goal[0]][goal[1]] = 0

	#priority check for the next node to check
	openSet = queue.PriorityQueue()

	#node we came from
	cameFrom = np.zeros((board.shape[0], board.shape[1], 2), dtype=int)
	cameFrom[start[0]][start[1]] = (-1, -1)

	#score the the weight it takes to travel to a node
	gScore = np.full(board.shape, -1, dtype=int)
	
	gScore[start[0]][start[1]] = 0

	#heuristic for the weight it will take to get to the goal
	fScore = np.full(board.shape, -1, dtype=int)

	fScore[start[0]][start[1]] = math.fabs(goal[0] - start[0]) + math.fabs(goal[1] - start[1])
	
	openSet.put((fScore[start[0]][start[1]], start))

	#checking for the goal node
	while not openSet.empty():
		current = openSet.get()[1]
		if current == goal:
			return backPedal(cameFrom, start, goal)
		if closedSet[current[0]][current[1]] == 1:
			continue
		closedSet[current[0]][current[1]] = 1
		for x in range(0, 4):
			
			neighbour = (-1, -1)

			#left
			if x is 0:
				if current[0] == 0:
					continue
				neighbour = (current[0] - 1, current[1])

			#up
			if x is 1:
				if current[1] == 0:
					continue
				neighbour = (current[0], current[1] - 1)

			#right
			if x is 2:
				if current[0] == board.shape[0] - 1:
					continue
				neighbour = (current[0] + 1, current[1])

			#down
			if x is 3:
				if current[1] == board.shape[1] - 1:
					continue
				neighbour = (current[0], current[1] + 1)

			#if coordinate has already been checked
			if closedSet[neighbour[0]][neighbour[1]] == 1:
				continue

			#assigning gScore to neighbour of current node
			tentativeGScore = gScore[current[0]][current[1]] + 1

			neighbourGScore = gScore[neighbour[0]][neighbour[1]]

			#adding neighbour to openSet if shortest path
			if tentativeGScore < neighbourGScore or neighbourGScore == -1:
				
				gScore[neighbour[0]][neighbour[1]] = tentativeGScore
				cameFrom[neighbour[0]][neighbour[1]] = current
				fScore[neighbour[0]][neighbour[1]] = gScore[neighbour[0]][neighbour[1]] + math.fabs(goal[0] - neighbour[0]) + math.fabs(goal[1] - neighbour[1])

				openSet.put((fScore[neighbour[0]][neighbour[1]], neighbour))

	#error code for couldn't find path to goal
	return (2, 2)

#tester main
def main():
	board = np.zeros((11, 11), dtype=int)
	goal = (8, 3)
	start = (9, 0)
	board[9, 1] = -1
	board[8, 3] = 3
	print(board)
	path = aStar(board, start, goal)
	print(path)

	
if __name__ == '__main__':
	main()
