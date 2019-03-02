import numpy as np
import math
from lib import queue

def backPedal(cameFrom, start, goal):
	path = []
	curr = goal
	while curr[0] != -1:
		path.append(tuple(curr))
		curr = cameFrom[curr[0]][curr[1]]
	#print("Path: ", path)
	npPath = np.array(path[-2])
	npStart = np.array(start)
	direction = npPath - npStart
	return direction

def aStar(board, start, goal): #combine with bfs for efficiency
	#print(board)
	path = {}
	
	closedSet = np.zeros(board.shape, dtype=int) #change later to np.copy
	for (x,y), value in np.ndenumerate(board):
		if value == -1:
			closedSet[x][y] = 1
	closedSet[start[0]][start[1]] = 0
	closedSet[goal[0]][goal[1]] = 0

	openSet = queue.PriorityQueue()
	cameFrom = np.zeros((board.shape[0], board.shape[1], 2), dtype=int)
	cameFrom[start[0]][start[1]] = (-1, -1)
	#print(cameFrom)
	gScore = np.full(board.shape, -1, dtype=int)
	
	gScore[start[0]][start[1]] = 0
	
	fScore = np.full(board.shape, -1, dtype=int)

	fScore[start[0]][start[1]] = math.fabs(goal[0] - start[0]) + math.fabs(goal[1] - start[1])
	
	openSet.put((fScore[start[0]][start[1]], start))
	
	while not openSet.empty():
		current = openSet.get()[1]
		if current == goal:
			#print("We done boys")
			return backPedal(cameFrom, start, goal)
		if closedSet[current[0]][current[1]] == 1:
			continue
		closedSet[current[0]][current[1]] = 1
		for x in range(0, 4):
			
			neighbour = (-1, -1)
			
			#LOOK AT THIS FUCKED UP SHITTERY AGAIN!!!
			if x is 0:
				if current[0] == 0:
					continue
				'''elif board[current[0] - 1][current[1]] == -1:
					continue'''
				neighbour = (current[0] - 1, current[1])
			if x is 1:
				if current[1] == 0:
					continue
				'''elif board[current[0]][current[1] - 1] == -1:
					continue'''
				neighbour = (current[0], current[1] - 1)
			if x is 2:
				#print(board.shape[0])
				if current[0] == board.shape[0] - 1:
					#print('danger')
					continue
				'''elif board[current[0] + 1][current[1]] == -1:
					continue'''
				neighbour = (current[0] + 1, current[1])
				#print(neighbour)
			if x is 3:
				#print(board.shape[0])
				if current[1] == board.shape[0] - 1:
					#print('danger')
					continue
				'''elif board[current[0]][current[1] + 1] == -1:
					continue'''
				neighbour = (current[0], current[1] + 1)
				#print(neighbour)

			'''if neighbour[0] == 15 or neighbour[1] == 15:
				continue'''

			if closedSet[neighbour[0]][neighbour[1]] == 1:
				continue
			
			tentativeGScore = gScore[current[0]][current[1]] + 1

			neighbourGScore = gScore[neighbour[0]][neighbour[1]]
			
			#print("tentativeScore", tentativeGScore)
			#print("neighbourScore", neighbourGScore)
			#print()
			
			if tentativeGScore < neighbourGScore or neighbourGScore == -1:
				
				gScore[neighbour[0]][neighbour[1]] = tentativeGScore
				cameFrom[neighbour[0]][neighbour[1]] = current
				fScore[neighbour[0]][neighbour[1]] = gScore[neighbour[0]][neighbour[1]] + math.fabs(goal[0] - neighbour[0]) + math.fabs(goal[1] - neighbour[1])
				
				
				openSet.put((fScore[neighbour[0]][neighbour[1]], neighbour))
			
		#print(current)
		
	
	return -1


def main():
	board = np.zeros((19, 19), dtype=int)
	goal = (5, 16)
	start = (12, 3)
	#print(board)
	path = aStar(board, start, goal)
	#print(path)

	
if __name__ == '__main__':
	main()
