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
        y = random.randrange(0,dim)
        x = random.randrange(0,dim)
        fireCell = cellMaze(point(y,x), '1', 0)
        self.maze[y][x] = fireCell
        for m in range(0, dim):
            for n in range(0, dim):
                print(self.maze[m][n].state, end = ' ')
            print()
        print()




    def dfs(self, rows, columns, finalRow, finalCol, mazeIn):
        if mazeIn[rows][columns].state!='0':
            return False
        fringe = []
        visited = []
        fringe.append(mazeIn[rows][columns])
        while fringe:
            current = fringe.pop()
            currPt = current.pt
            if (currPt.y == finalRow and currPt.x == finalCol):
                return True
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
        if mazeIn[rows][columns].state!='0':
            return False
        fringe = []
        visited = []
        fringe.append(mazeIn[rows][columns])
        while fringe:
            current = fringe.pop(0)
            currPt = current.pt
            if (currPt.y == finalRow and currPt.x == finalCol):
                return current.distance
                #return True
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
        return False


    def aStar(self, rows, columns, finalRow, finalCol, mazeIn):
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
                return current[1][0].distance
                #return True
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
        return False

    def calcDistance(self, rows, columns, finalRow, finalCol):
        distance = math.sqrt( ((columns-finalCol)**2)+((rows-finalRow)**2) )
        return distance

    def aStarWithFire(self, rows, columns, finalRow, finalCol, mazeIn, q):
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
                return current[1][0].distance
                #return True
            if [current[1][0].pt.y, current[1][0].pt.x] not in visited:
                if (mazeIn[current[1][0].pt.y][current[1][0].pt.x].state =='1'):
                    return False
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
                mazeIn = self.advance_fire_one_step(mazeIn, q)
                for m in range(0, self.dim):
                    for n in range(0, self.dim):
                        print(mazeIn[m][n].state, end = ' ')
                    print()
                print()
                self.counterAStar = len(visited)


        return False

    def printMaze(self, mazeIn):
        for i in range(0,self.dim):
            for j in range(0, self.dim):
                print(mazeIn[i][j].state, end = ' ')
            print()

    def advance_fire_one_step(self, mazeIn, q):
        mazeUse = copy.deepcopy(mazeIn)
        for y in range(0,self.dim):
            for x in range(0,self.dim):
                fireCounter = 0
                if mazeUse[y][x].state == '0':
                    if(y+1<self.dim and mazeUse[y+1][x].state == '1'):
                         fireCounter = fireCounter + 1
                    if(x+1<self.dim and mazeUse[y][x+1].state == '1'):
                        fireCounter = fireCounter + 1
                    if(y-1>0 and mazeUse[y-1][x].state == '1'):
                        fireCounter = fireCounter + 1
                    if(x-1>0 and mazeUse[y][x-1].state == '1'):
                        fireCounter = fireCounter + 1
                    prob = 1 - (1-q)**fireCounter
                    if random.random() <= prob:
                        mazeUse[y][x].state == '1'
        return mazeUse


mazeTest = test(5, 0.3)
check = mazeTest.aStarWithFire(0,0,4,4,mazeTest.maze, 1)
print("astarfire: ", check)
check2 = mazeTest.bfs(0,0,4,4,mazeTest.maze)
print("bfs: ",  check2)
