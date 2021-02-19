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

class path:
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
                print(self.maze[i][j].state, end = ' ')
            print()

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
                print(currNode)
                pathStack.append(currNode)
                for i in range(0, current.distance):
                    print(traceBack.get((currNode)))
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


maze = path(5, 0.3)
check = maze.bfs(0,0,4,4,maze.maze)
print(check[0])
path = check[2]
if path != False:
    for i in range(0, len(path)):
        print(path.pop())
