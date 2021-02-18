import random
import copy
import math
import csv
import heapq
import time
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


    def dfs(self, rows, columns, finalRow, finalCol, mazeIn):
        startTime = time.time()
        if mazeIn[rows][columns].state!='0':
            return False
        fringe = []
        visited = []
        fringe.append(mazeIn[rows][columns])
        while fringe:
            current = fringe.pop()
            currPt = current.pt
            if (currPt.y == finalRow and currPt.x == finalCol):
                return True, time.time()-startTime
                #return current.distance
            if ([currPt.y, currPt.x]) not in visited:
                if(currPt.y+1<self.dim and mazeIn[currPt.y+1][currPt.x].state == '0'):
                    fringe.append(cellMaze( mazeIn[currPt.y+1][currPt.x].pt, mazeIn[currPt.y+1][currPt.x].state, current.distance+1))
                if(currPt.x+1<self.dim and mazeIn[currPt.y][currPt.x+1].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.y][currPt.x+1].pt, mazeIn[currPt.y][currPt.x+1].state, current.distance+1))
                if(currPt.y-1>0 and mazeIn[currPt.y-1][currPt.x].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.y-1][currPt.x].pt, mazeIn[currPt.y-1][currPt.x].state, current.distance+1))
                if(currPt.x-1>0 and mazeIn[currPt.y][currPt.x-1].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.y][currPt.x-1].pt, mazeIn[currPt.y][currPt.x-1].state, current.distance+1))
                visited.append([currPt.y, currPt.x])
                self.counterDFS = len(visited)
        return False, time.time()-startTime


    def bfs(self, rows, columns, finalRow, finalCol, mazeIn):
        startTime = time.time()
        if mazeIn[rows][columns].state!='0':
            return False
        fringe = []
        visited = []
        fringe.append(mazeIn[rows][columns])
        while fringe:
            current = fringe.pop(0)
            currPt = current.pt
            if (currPt.y == finalRow and currPt.x == finalCol):
                #return current.distance
                return True, time.time()-startTime
            if ([currPt.y, currPt.x]) not in visited:
                if(currPt.y+1<self.dim and mazeIn[currPt.y+1][currPt.x].state == '0'):
                    fringe.append(cellMaze( mazeIn[currPt.y+1][currPt.x].pt, mazeIn[currPt.y+1][currPt.x].state, current.distance+1))
                if(currPt.x+1<self.dim and mazeIn[currPt.y][currPt.x+1].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.y][currPt.x+1].pt, mazeIn[currPt.y][currPt.x+1].state, current.distance+1))
                if(currPt.y-1>0 and mazeIn[currPt.y-1][currPt.x].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.y-1][currPt.x].pt, mazeIn[currPt.y-1][currPt.x].state, current.distance+1))
                if(currPt.x-1>0 and mazeIn[currPt.y][currPt.x-1].state == '0'):
                    fringe.append(cellMaze(mazeIn[currPt.y][currPt.x-1].pt, mazeIn[currPt.y][currPt.x-1].state, current.distance+1))
                visited.append([currPt.y, currPt.x])
                self.counterBFS = len(visited)
        return False, time.time()-startTime


    def aStar(self, rows, columns, finalRow, finalCol, mazeIn):
        startTime = time.time()
        if mazeIn[rows][columns].state!='0':
            return False
        fringe = []
        visited = []
        distance = self.calcDistance(rows, columns, finalRow, finalCol)
        heapq.heapify(fringe)
        heapq.heappush(fringe, (distance, [mazeIn[rows][columns]]))


        while fringe:
            current = heapq.heappop(fringe)
            if (current[1][0].pt.y == finalRow and current[1][0].pt.x == finalCol):
                #return current[1][0].distance
                return True, time.time()-startTime
            if [current[1][0].pt.y, current[1][0].pt.x] not in visited:
                if(current[1][0].pt.y+1<self.dim and mazeIn[current[1][0].pt.y+1][current[1][0].pt.x].state == '0'):
                    distanceFringe1 = self.calcDistance(current[1][0].pt.y+1, current[1][0].pt.x, finalRow, finalCol)
                    heapq.heappush(fringe, (distanceFringe1+current[1][0].distance, [cellMaze(mazeIn[current[1][0].pt.y+1][current[1][0].pt.x].pt, mazeIn[current[1][0].pt.y+1][current[1][0].pt.x].state, current[1][0].distance + 1)]))
                if(current[1][0].pt.x+1<self.dim and mazeIn[current[1][0].pt.y][current[1][0].pt.x+1].state == '0'):
                    distanceFringe2 = self.calcDistance(current[1][0].pt.y, current[1][0].pt.x+1, finalRow, finalCol)
                    heapq.heappush(fringe, (distanceFringe2+current[1][0].distance,  [cellMaze(mazeIn[current[1][0].pt.y][current[1][0].pt.x+1].pt, mazeIn[current[1][0].pt.y][current[1][0].pt.x+1].state, current[1][0].distance+1)]))
                if(current[1][0].pt.y-1>0 and mazeIn[current[1][0].pt.y-1][current[1][0].pt.x].state == '0'):
                    distanceFringe3 = self.calcDistance(current[1][0].pt.y-1, current[1][0].pt.x, finalRow, finalCol)
                    heapq.heappush(fringe, (distanceFringe3+current[1][0].distance,  [cellMaze(mazeIn[current[1][0].pt.y-1][current[1][0].pt.x].pt, mazeIn[current[1][0].pt.y-1][current[1][0].pt.x].state, current[1][0].distance+1)]))
                if(current[1][0].pt.x-1>0 and mazeIn[current[1][0].pt.y][current[1][0].pt.x-1].state == '0'):
                    distanceFringe4 = self.calcDistance(current[1][0].pt.y, current[1][0].pt.x-1, finalRow, finalCol)
                    heapq.heappush(fringe, (distanceFringe4+current[1][0].distance,  [cellMaze(mazeIn[current[1][0].pt.y][current[1][0].pt.x-1].pt, mazeIn[current[1][0].pt.y][current[1][0].pt.x-1].state, current[1][0].distance+1)]))
                visited.append([current[1][0].pt.y, current[1][0].pt.x])
                self.counterAStar = len(visited)
        return False, time.time()-startTime

    def calcDistance(self, rows, columns, finalRow, finalCol):
        distance = math.sqrt( ((columns-finalCol)**2)+((rows-finalRow)**2) )
        return distance


Totaltime = 0
size=1000
while Totaltime<60:
    maze = test(size, 0.3)
    startTime = time.time()
    check1 = maze.aStar(0,0,size-1,size-1,maze.maze)
    if (check1[0] == True):
        Totaltime = time.time()-startTime
    print("astar: ", check1)
    size+=5

print("Largest dimensions: ", size-10)
