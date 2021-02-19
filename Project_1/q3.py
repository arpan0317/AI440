import random
import copy
import math
import csv
import heapq
class point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class cellMaze:
    def __init__(self, pt: point, state = '0', distance = 0):
        self.state = state
        self.distance = distance
        self.pt = pt

    def __lt__(self, other):
        return self.distance < other.distance

class q3:
    def __init__(self, dim, p):
        self.maze = [ [ None for i in range(dim) ] for j in range(dim) ]
        self.dim = dim
        self.p = p
        self.foundDFS = False
        self.visited = []
        self.counterDFS = 0
        self.counterBFS = 0
        self.counterAStar = 0
        for i in range(0, dim):
            for j in range(0, dim):
                pt = point(i,j)
                c = cellMaze(pt, '0',0)
                if p > random.random():
                    c.state = '2'
                self.maze[i][j] = c
                ptFirst = point(0,0)
                ptLast = point(dim-1, dim-1)
                self.maze[0][0] = cellMaze(ptFirst,'0',0)
                self.maze[dim-1][dim-1] = cellMaze(ptLast,'0',0)
                #print(self.maze[i][j].state, end = ' ')
            #print()

#DONE, does not account for any fires, order of stack pop goes down, right, up, left
#returns true, distance of path
    def dfs(self, x, y, finalX, finalY, mazeIn):
        if mazeIn[x][y].state!='0':
            return False, False
        fringe = []
        visited = []
        fringe.append(mazeIn[x][y])
        while fringe:
            current = fringe.pop()
            currPt = current.pt
            if (currPt.x == finalX and currPt.y == finalY):
                return True, current.distance
            if ([currPt.x, currPt.y]) not in visited:
                if(currPt.y-1>=0 and mazeIn[currPt.x][currPt.y-1].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.x][currPt.y-1].pt, mazeIn[currPt.x][currPt.y-1].state, current.distance+1))
                if(currPt.x-1>=0 and mazeIn[currPt.x-1][currPt.y].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.x-1][currPt.y].pt, mazeIn[currPt.x-1][currPt.y].state, current.distance+1))
                if(currPt.y+1<self.dim and mazeIn[currPt.x][currPt.y+1].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.x][currPt.y+1].pt, mazeIn[currPt.x][currPt.y+1].state, current.distance+1))
                if(currPt.x+1<self.dim and mazeIn[currPt.x+1][currPt.y].state == '0'):
                    fringe.append(cellMaze( mazeIn[currPt.x+1][currPt.y].pt, mazeIn[currPt.x+1][currPt.y].state, current.distance+1))
                visited.append([currPt.x, currPt.y])
                self.counterDFS = len(visited)
        return False, False

#DONE, does not account for fire spread, order of queue pop goes down, right, up, left
#returns true, distance of path
    def bfs(self, x, y, finalX, finalY, mazeIn):
        if mazeIn[x][y].state!='0':
            return False, False
        fringe = []
        visited = []
        fringe.append(mazeIn[x][y])
        while fringe:
            current = fringe.pop(0)
            currPt = current.pt
            if (currPt.x == finalX and currPt.y == finalY):
                return True, current.distance
            if ([currPt.x, currPt.y]) not in visited:
                if(currPt.x+1<self.dim and mazeIn[currPt.x+1][currPt.y].state == '0'):
                    fringe.append(cellMaze( mazeIn[currPt.x+1][currPt.y].pt, mazeIn[currPt.x+1][currPt.y].state, current.distance+1))
                if(currPt.y+1<self.dim and mazeIn[currPt.x][currPt.y+1].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.x][currPt.y+1].pt, mazeIn[currPt.x][currPt.y+1].state, current.distance+1))
                if(currPt.x-1>=0 and mazeIn[currPt.x-1][currPt.y].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.x-1][currPt.y].pt, mazeIn[currPt.x-1][currPt.y].state, current.distance+1))
                if(currPt.y-1>=0 and mazeIn[currPt.x][currPt.y-1].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.x][currPt.y-1].pt, mazeIn[currPt.x][currPt.y-1].state, current.distance+1))
                visited.append([currPt.x, currPt.y])
                self.counterBFS = len(visited)
        return False, False

#DONE, does not account for fire, heap pop order is based on heuristic euclidian distance to goal + steps already travelled
    def aStar(self, x, y, finalX, finalY, mazeIn):
        if mazeIn[x][y].state!='0':
            return False, False
        fringe = []
        visited = []
        distance = self.calcDistance(x, y, finalX, finalY)
        heapq.heapify(fringe)
        heapq.heappush(fringe, (distance, [mazeIn[x][y]]))
        while fringe:
            current = heapq.heappop(fringe)
            if (current[1][0].pt.x == finalX and current[1][0].pt.y == finalY):
                return True, current[1][0].distance
            if [current[1][0].pt.x, current[1][0].pt.y] not in visited:
                if(current[1][0].pt.x+1<self.dim and mazeIn[current[1][0].pt.x+1][current[1][0].pt.y].state == '0'):
                    distanceFringe1 = self.calcDistance(current[1][0].pt.x+1, current[1][0].pt.y, finalX, finalY)
                    heapq.heappush(fringe, (distanceFringe1+current[1][0].distance, [cellMaze(mazeIn[current[1][0].pt.x+1][current[1][0].pt.y].pt, mazeIn[current[1][0].pt.x+1][current[1][0].pt.y].state, current[1][0].distance + 1)]))
                if(current[1][0].pt.y+1<self.dim and mazeIn[current[1][0].pt.x][current[1][0].pt.y+1].state == '0'):
                    distanceFringe2 = self.calcDistance(current[1][0].pt.x, current[1][0].pt.y+1, finalX, finalY)
                    heapq.heappush(fringe, (distanceFringe2+current[1][0].distance,  [cellMaze(mazeIn[current[1][0].pt.x][current[1][0].pt.y+1].pt, mazeIn[current[1][0].pt.x][current[1][0].pt.y+1].state, current[1][0].distance+1)]))
                if(current[1][0].pt.x-1>=0 and mazeIn[current[1][0].pt.x-1][current[1][0].pt.y].state == '0'):
                    distanceFringe3 = self.calcDistance(current[1][0].pt.x-1, current[1][0].pt.y, finalX, finalY)
                    heapq.heappush(fringe, (distanceFringe3+current[1][0].distance,  [cellMaze(mazeIn[current[1][0].pt.x-1][current[1][0].pt.y].pt, mazeIn[current[1][0].pt.x-1][current[1][0].pt.y].state, current[1][0].distance+1)]))
                if(current[1][0].pt.y-1>=0 and mazeIn[current[1][0].pt.x][current[1][0].pt.y-1].state == '0'):
                    distanceFringe4 = self.calcDistance(current[1][0].pt.x, current[1][0].pt.y-1, finalX, finalY)
                    heapq.heappush(fringe, (distanceFringe4+current[1][0].distance,  [cellMaze(mazeIn[current[1][0].pt.x][current[1][0].pt.y-1].pt, mazeIn[current[1][0].pt.x][current[1][0].pt.y-1].state, current[1][0].distance+1)]))
                visited.append([current[1][0].pt.x, current[1][0].pt.y])
                self.counterAStar = len(visited)
        return False, False

#DONE, helper method to calculate euclidian distance
    def calcDistance(self, rows, columns, finalRow, finalCol):
        distance = math.sqrt( ((columns-finalCol)**2)+((rows-finalRow)**2) )
        return distance

data_headerQ3 = ['avg difference', 'density']
with open('exportQ3.csv', 'w') as file_writerQ3:
    writerQ3 = csv.writer(file_writerQ3)
    writerQ3.writerow(data_headerQ3)

    for probQ3 in range(1,50): 
        difference = 0
        diffSum = 0
        for countQ3 in range(0,25):
            mazeQ3 = q3(100,probQ3/50)
            checkQ3BFS = mazeQ3.bfs(0,0,99,99,mazeQ3.maze)
            checkQ3AStar = mazeQ3.aStar(0,0,99,99,mazeQ3.maze)
            difference = mazeQ3.counterBFS - mazeQ3.counterAStar
            diffSum = diffSum + difference
            print("diff: " ,difference, " iteration: ", countQ3)
        dataQ3 = [diffSum/25, probQ3/50]
        writerQ3.writerow(dataQ3)
