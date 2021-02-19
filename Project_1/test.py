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

class test:
    def __init__(self, dim, p):
        self.maze = [ [ None for i in range(dim) ] for j in range(dim) ]
        self.dim = dim
        self.p = p
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
                print(self.maze[i][j].state, end = ' ')
            print()

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
#returns true, distance of path, pathStack with top of stack being 0,0
    def bfs(self, x, y, finalX, finalY, mazeIn):
        if mazeIn[x][y].state!='0':
            return False, False, False
        fringe = []
        visited = []
        pathStack = []
        traceBack = {}
        traceBack[(0,0)] = (0,0)
        fringe.append(mazeIn[x][y])
        while fringe:
            current = fringe.pop(0)
            currPt = current.pt
            if (currPt.x == finalX and currPt.y == finalY):
                currNode = (finalX, finalY)
                #print(currNode)
                pathStack.append(currNode)
                for i in range(0, current.distance):
                    #print(traceBack.get((currNode)))
                    pathStack.append(traceBack.get((currNode)))
                    currNode = traceBack.get((currNode))
                return True, current.distance, pathStack
            if ([currPt.x, currPt.y]) not in visited:
                if(currPt.x+1<self.dim and mazeIn[currPt.x+1][currPt.y].state == '0'):
                    fringe.append(cellMaze( mazeIn[currPt.x+1][currPt.y].pt, mazeIn[currPt.x+1][currPt.y].state, current.distance+1))
                    if ([currPt.x+1, currPt.y]) not in visited:
                        traceBack[(currPt.x+1, currPt.y)] = (currPt.x, currPt.y)
                if(currPt.y+1<self.dim and mazeIn[currPt.x][currPt.y+1].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.x][currPt.y+1].pt, mazeIn[currPt.x][currPt.y+1].state, current.distance+1))
                    if ([currPt.x, currPt.y+1]) not in visited:
                        traceBack[(currPt.x, currPt.y+1)] = (currPt.x, currPt.y)
                if(currPt.x-1>=0 and mazeIn[currPt.x-1][currPt.y].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.x-1][currPt.y].pt, mazeIn[currPt.x-1][currPt.y].state, current.distance+1))
                    if ([currPt.x-1, currPt.y]) not in visited:
                        traceBack[(currPt.x-1, currPt.y)] = (currPt.x, currPt.y)
                if(currPt.y-1>=0 and mazeIn[currPt.x][currPt.y-1].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.x][currPt.y-1].pt, mazeIn[currPt.x][currPt.y-1].state, current.distance+1))
                    if ([currPt.x, currPt.y-1]) not in visited:
                        traceBack[(currPt.x, currPt.y-1)] = (currPt.x, currPt.y)
                visited.append([currPt.x, currPt.y])
                self.counterBFS = len(visited)
                #print([currPt.x, currPt.y])
        return False, False, False

#DONE, does not account for fire, heap pop order is based on heuristic euclidian distance to goal + steps already travelled
#returns true, distance of path, actual path in stack with top being 0,0
    def aStar(self, x, y, finalX, finalY, mazeIn):
        if mazeIn[x][y].state!='0':
            return False, False, False
        fringe = []
        visited = []
        pathStack = []
        traceBack = {}
        traceBack[(0,0)] = (0,0)
        distance = self.calcDistance(x, y, finalX, finalY)
        heapq.heapify(fringe)
        heapq.heappush(fringe, (distance, [mazeIn[x][y]]))
        while fringe:
            current = heapq.heappop(fringe)
            if (current[1][0].pt.x == finalX and current[1][0].pt.y == finalY):
                currNode = (finalX, finalY)
                pathStack.append(currNode)
                for i in range(0, current[1][0].distance):
                    #print(traceBack.get((current)))
                    pathStack.append(traceBack.get((currNode)))
                    currNode = traceBack.get((currNode))
                return True, current[1][0].distance, pathStack
            if [current[1][0].pt.x, current[1][0].pt.y] not in visited:
                if(current[1][0].pt.x+1<self.dim and mazeIn[current[1][0].pt.x+1][current[1][0].pt.y].state == '0'):
                    distanceFringe1 = self.calcDistance(current[1][0].pt.x+1, current[1][0].pt.y, finalX, finalY)
                    heapq.heappush(fringe, (distanceFringe1+current[1][0].distance, [cellMaze(mazeIn[current[1][0].pt.x+1][current[1][0].pt.y].pt, mazeIn[current[1][0].pt.x+1][current[1][0].pt.y].state, current[1][0].distance + 1)]))
                    if ([current[1][0].pt.x+1, current[1][0].pt.y]) not in visited:
                        traceBack[(current[1][0].pt.x+1, current[1][0].pt.y)] = (current[1][0].pt.x, current[1][0].pt.y)
                if(current[1][0].pt.y+1<self.dim and mazeIn[current[1][0].pt.x][current[1][0].pt.y+1].state == '0'):
                    distanceFringe2 = self.calcDistance(current[1][0].pt.x, current[1][0].pt.y+1, finalX, finalY)
                    heapq.heappush(fringe, (distanceFringe2+current[1][0].distance,  [cellMaze(mazeIn[current[1][0].pt.x][current[1][0].pt.y+1].pt, mazeIn[current[1][0].pt.x][current[1][0].pt.y+1].state, current[1][0].distance+1)]))
                    if ([current[1][0].pt.x, current[1][0].pt.y+1]) not in visited:
                        traceBack[(current[1][0].pt.x, current[1][0].pt.y+1)] = (current[1][0].pt.x, current[1][0].pt.y)
                if(current[1][0].pt.x-1>=0 and mazeIn[current[1][0].pt.x-1][current[1][0].pt.y].state == '0'):
                    distanceFringe3 = self.calcDistance(current[1][0].pt.x-1, current[1][0].pt.y, finalX, finalY)
                    heapq.heappush(fringe, (distanceFringe3+current[1][0].distance,  [cellMaze(mazeIn[current[1][0].pt.x-1][current[1][0].pt.y].pt, mazeIn[current[1][0].pt.x-1][current[1][0].pt.y].state, current[1][0].distance+1)]))
                    if ([current[1][0].pt.x-1, current[1][0].pt.y]) not in visited:
                        traceBack[(current[1][0].pt.x-1, current[1][0].pt.y)] = (current[1][0].pt.x, current[1][0].pt.y)
                if(current[1][0].pt.y-1>=0 and mazeIn[current[1][0].pt.x][current[1][0].pt.y-1].state == '0'):
                    distanceFringe4 = self.calcDistance(current[1][0].pt.x, current[1][0].pt.y-1, finalX, finalY)
                    heapq.heappush(fringe, (distanceFringe4+current[1][0].distance,  [cellMaze(mazeIn[current[1][0].pt.x][current[1][0].pt.y-1].pt, mazeIn[current[1][0].pt.x][current[1][0].pt.y-1].state, current[1][0].distance+1)]))
                    if ([current[1][0].pt.x, current[1][0].pt.y-1]) not in visited:
                        traceBack[(current[1][0].pt.x, current[1][0].pt.y-1)] = (current[1][0].pt.x, current[1][0].pt.y)
                visited.append([current[1][0].pt.x, current[1][0].pt.y])
                self.counterAStar = len(visited)
        return False, False, False

#DONE, helper method to calculate euclidian distance
    def calcDistance(self, rows, columns, finalRow, finalCol):
        distance = math.sqrt( ((columns-finalCol)**2)+((rows-finalRow)**2) )
        return distance

#data_headerQ2 = ['density', 'reached']
#with open('exportQ2.csv', 'w') as file_writerQ2:
#    writerQ2 = csv.writer(file_writerQ2)
#    writerQ2.writerow(data_headerQ2)

#    for probQ2 in range(1,100):
#        trueCounter = 0
#        for countQ2 in range(0,100):
#            mazeQ2 = test(100,probQ2/100)
#            checkQ2 = mazeQ2.dfs(0,0,99,99,mazeQ2.maze)
#            if checkQ2[0] == True:
#                trueCounter = trueCounter + 1
#            print("prob: " , probQ2/100, " iteration: ", countQ2)
#        dataQ2 = [probQ2/100, trueCounter/100]
#        writerQ2.writerow(dataQ2)
#FILE DONE
