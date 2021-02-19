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
        y = random.randrange(0,dim)
        x = random.randrange(0,dim)
        fireCell = cellMaze(point(y,x), '1', 0)
        self.maze[y][x] = fireCell
        #for m in range(0, dim):
            #for n in range(0, dim):
                #print(self.maze[m][n].state, end = ' ')
            #print()

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

#DONE, advances fire one step for the input maze and input spread rate
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
                        mazeUse[y][x].state = '1'
        return mazeUse

    def printMaze(self, mazeIn):
        for i in range(0,self.dim):
            for j in range(0, self.dim):
                print(mazeIn[i][j].state, end = ' ')
            print()

#helper method to check where the fire in a maze is
    def checkFireLoc(self, mazeIn):
        for x in range(0,self.dim):
            for y in range(0, self.dim):
                if mazeIn[x][y].state == '1':
                    fireLocX = x
                    fireLocY = y
                    return fireLocX, fireLocY

#DONE, returns true if fire is accessible from starting points
#used as helper method for strat1 and strat2
    def bfsFireFind(self, x, y, finalX, finalY, mazeIn):
        if mazeIn[x][y].state!='0':
            return False
        fringe = []
        visited = []
        fringe.append(mazeIn[x][y])
        while fringe:
            current = fringe.pop(0)
            currPt = current.pt
            if (currPt.x == finalX and currPt.y == finalY):
                return True
            if ([currPt.x, currPt.y]) not in visited:
                if(currPt.x+1<self.dim and mazeIn[currPt.x+1][currPt.y].state != '2'):
                    fringe.append(cellMaze( mazeIn[currPt.x+1][currPt.y].pt, mazeIn[currPt.x+1][currPt.y].state, current.distance+1))
                if(currPt.y+1<self.dim and mazeIn[currPt.x][currPt.y+1].state != '2'):
                    fringe.append(cellMaze(mazeIn[currPt.x][currPt.y+1].pt, mazeIn[currPt.x][currPt.y+1].state, current.distance+1))
                if(currPt.x-1>=0 and mazeIn[currPt.x-1][currPt.y].state != '2'):
                    fringe.append(cellMaze(mazeIn[currPt.x-1][currPt.y].pt, mazeIn[currPt.x-1][currPt.y].state, current.distance+1))
                if(currPt.y-1>=0 and mazeIn[currPt.x][currPt.y-1].state != '2'):
                    fringe.append(cellMaze(mazeIn[currPt.x][currPt.y-1].pt, mazeIn[currPt.x][currPt.y-1].state, current.distance+1))
                visited.append([currPt.x, currPt.y])
                self.counterBFS = len(visited)
                #print([currPt.x, currPt.y])
        return False

#DONE, returns true if maze path from bfs still works with fire, false otherwise
    def strat1(self, x, y, finalX, finalY, mazeIn, q):
        check = self.bfs(x, y, finalX, finalY, mazeIn)
        fireLoc = self.checkFireLoc(mazeIn)
        check2 = self.bfsFireFind(x,y,fireLoc[0], fireLoc[1], mazeIn)
        if check[0] == False or check2 == False:
            return False
        if check[2] != False:
            travelStack = check[2]
            while len(travelStack) != 0:
                curr = travelStack.pop()
                mazeIn = self.advance_fire_one_step(mazeIn, q)
                if mazeIn[curr[0]][curr[1]].state != '0':
                    return False
            return True

    def strat2(self, x, y, finalX, finalY, mazeIn, q):
        check = self.bfs(x, y, finalX, finalY, mazeIn)
        fireLoc = self.checkFireLoc(mazeIn)
        check2 = self.bfsFireFind(x,y,fireLoc[0], fireLoc[1], mazeIn)
        if check[0] == False or check2 == False:
            return False

        return self.recStrat2(x, y, finalX, finalY, mazeIn, q)

    def recStrat2(self, x, y, finalX, finalY, mazeIn, q):
        #self.printMaze(mazeIn)
        #print("inputs: ", x,y,finalX,finalY)
        check = self.bfs(x, y, finalX, finalY, mazeIn)
        #print(check[2])
        if check[0] == False:
            return False
        if x == finalX and y == finalY:
            return True
        else:
            mazeIn = self.advance_fire_one_step(mazeIn, q)
            point = check[2].pop()
            pointCont = check[2].pop()
            return self.recStrat2(pointCont[0], pointCont[1], finalX, finalY, mazeIn, q)



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

data_headerQ5 = ['firerate', 'avg path found % 1', 'avg path found % 2']
with open('exportQ5.csv', 'w') as file_writerQ5:
    writerQ5 = csv.writer(file_writerQ5)
    writerQ5.writerow(data_headerQ5)

    for probQ5 in range(1,50):
        truthCounter1 = 0
        truthCounter2 = 0
        for countQ5 in range(0,20):
            mazeQ5 = path(40,0.3)
            checkQ5BFS = mazeQ5.bfs(0,0,39,39,mazeQ5.maze)
            if checkQ5BFS[0] ==  False:
                continue
            checkStrat1 = mazeQ5.strat1(0,0,39,39,mazeQ5.maze, probQ5/50)
            if checkStrat1 == True:
                truthCounter1 = truthCounter1 + 1
            checkStrat2 = mazeQ5.strat2(0,0,39,39,mazeQ5.maze, probQ5/50)
            if checkStrat2 == True:
                truthCounter2 = truthCounter2 + 1
            print("iteration: ", countQ5, " firerate: ", probQ5/50)
        dataQ5 = [probQ5/50, truthCounter1/20, truthCounter2/20]
        print(dataQ5)
        writerQ5.writerow(dataQ5)

#maze = path(5, 0.3)
#mazeFireChane = maze.calcFireChance(maze.maze, 0.1)
