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
        self.counterBFSFire = 0
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




    def dfs(self, x, y, finalX, finalY, mazeIn):
        if mazeIn[x][y].state!='0':
            return False
        fringe = []
        visited = []
        fringe.append(mazeIn[x][y])
        while fringe:
            current = fringe.pop()
            currPt = current.pt
            if (currPt.x == finalX and currPt.y == finalY):
                return True
                #return current.distance
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
                self.counterDFS = len(visited)
                #print([currPt.x, currPt.y])
        return False


    def bfs(self, x, y, finalX, finalY, mazeIn):
        if mazeIn[x][y].state!='0':
            return False
        fringe = []
        visited = []
        if mazeIn[finalX][finalY].state == '1':
            return False
        fringe.append(mazeIn[x][y])
        while fringe:
            current = fringe.pop(0)
            currPt = current.pt
            if (currPt.x == finalX and currPt.y == finalY):
                #return current.distance
                return True
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
                #print("bfs")
                #self.printMaze(mazeIn)
                #print([currPt.x, currPt.y])
        return False

    def bfsForFire(self, x, y, finalX, finalY, mazeIn):
        if mazeIn[x][y].state!='0':
            return False
        fringe = []
        visited = []
        fringe.append(mazeIn[x][y])
        while fringe:
            current = fringe.pop(0)
            currPt = current.pt
            if (currPt.x == finalX and currPt.y == finalY):
                #return current.distance
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
                #print("bfs")
                #self.printMaze(mazeIn)
                #print([currPt.x, currPt.y])
        return False


    def bfsWithFire2(self, x, y, finalX, finalY, mazeIn, q):
        if mazeIn[x][y].state!='0':
            return False
        fringe = []
        visited = []
        fringe.append(mazeIn[x][y])
        while fringe:
            current = fringe.pop(0)
            currPt = current.pt
            if (currPt.x == finalX and currPt.y == finalY):
                #return current.distance
                return True
            if ([currPt.x, currPt.y]) not in visited:
                if mazeIn[finalX][finalY].state == '1':
                    return False
                if mazeIn[currPt.x][currPt.y].state == '1':
                    if len(fringe) == 0:
                        return False
                    current = fringe.pop(0)
                    currPt = current.pt
                    visited.append([currPt.x, currPt.y])
                else:
                    mazeIn = self.advance_fire_one_step(mazeIn,  q)
                    if mazeIn[currPt.x][currPt.y].state != '1':
                        print("strat 2")
                        if(currPt.x+1<self.dim and mazeIn[currPt.x+1][currPt.y].state != '2'):
                            print("down: ", mazeIn[currPt.x+1][currPt.y].state)
                            fringe.append(cellMaze( mazeIn[currPt.x+1][currPt.y].pt, mazeIn[currPt.x+1][currPt.y].state, current.distance+1))
                        if(currPt.y+1<self.dim and mazeIn[currPt.x][currPt.y+1].state != '2'):
                            print("right: ", mazeIn[currPt.x][currPt.y+1].state)
                            fringe.append(cellMaze(mazeIn[currPt.x][currPt.y+1].pt, mazeIn[currPt.x][currPt.y+1].state, current.distance+1))
                        if(currPt.x-1>=0 and mazeIn[currPt.x-1][currPt.y].state != '2'):
                            print("up: ", mazeIn[currPt.x-1][currPt.y].state)
                            fringe.append(cellMaze(mazeIn[currPt.x-1][currPt.y].pt, mazeIn[currPt.x-1][currPt.y].state, current.distance+1))
                        if(currPt.y-1>=0 and mazeIn[currPt.x][currPt.y-1].state != '2'):
                            print("left: ", mazeIn[currPt.x][currPt.y-1].state)
                            fringe.append(cellMaze(mazeIn[currPt.x][currPt.y-1].pt, mazeIn[currPt.x][currPt.y-1].state, current.distance+1))
                        visited.append([currPt.x, currPt.y])

                        #print("fire")
                        self.printMaze(mazeIn)
                        print([currPt.x, currPt.y])
                        #self.counterBFS = len(visited)
            #print()

        return False



    def bfsWithFire1(self, x, y, finalX, finalY, mazeIn, q):

        copyBFS = copy.deepcopy(mazeIn)
        if mazeIn[x][y].state!='0':
            return False
        fringe = []
        visited = []
        fringe.append(mazeIn[x][y])
        while fringe:
            current = fringe.pop(0)
            currPt = current.pt
            if (currPt.x == finalX and currPt.y == finalY):
                checker = self.bfs(0,0,self.dim-1, self.dim-1, copyBFS)
                #print("bfsfire1: ", current.distance)
                #print("bfsOgMaze: ", checker)
                if checker<current.distance:
                    return False
                else:

                    #return current.distance
                    return True
            if ([currPt.x, currPt.y]) not in visited:
                if mazeIn[finalX][finalY].state == '1':
                    return False
                if mazeIn[currPt.x][currPt.y].state == '1':
                    if len(fringe) == 0:
                        return False
                    current = fringe.pop(0)
                    currPt = current.pt
                    visited.append([currPt.x, currPt.y])
                else:
                    mazeIn = self.advance_fire_one_step(mazeIn,  q)
                    if mazeIn[currPt.x][currPt.y].state != '1':
                        print("strat1")
                        if(currPt.x+1<self.dim and mazeIn[currPt.x+1][currPt.y].state != '2'):
                            print("down: ", mazeIn[currPt.x+1][currPt.y].state)
                            fringe.append(cellMaze( mazeIn[currPt.x+1][currPt.y].pt, mazeIn[currPt.x+1][currPt.y].state, current.distance+1))
                        if(currPt.y+1<self.dim and mazeIn[currPt.x][currPt.y+1].state != '2'):
                            print("right: ", mazeIn[currPt.x][currPt.y+1].state)
                            fringe.append(cellMaze(mazeIn[currPt.x][currPt.y+1].pt, mazeIn[currPt.x][currPt.y+1].state, current.distance+1))
                        if(currPt.x-1>=0 and mazeIn[currPt.x-1][currPt.y].state != '2'):
                            print("up: ", mazeIn[currPt.x-1][currPt.y].state)
                            fringe.append(cellMaze(mazeIn[currPt.x-1][currPt.y].pt, mazeIn[currPt.x-1][currPt.y].state, current.distance+1))
                        if(currPt.y-1>=0 and mazeIn[currPt.x][currPt.y-1].state != '2'):
                            print("left: ", mazeIn[currPt.x][currPt.y-1].state)
                            fringe.append(cellMaze(mazeIn[currPt.x][currPt.y-1].pt, mazeIn[currPt.x][currPt.y-1].state, current.distance+1))
                        visited.append([currPt.x, currPt.y])
                        self.printMaze(mazeIn)
                        #print("fire")
                        #self.printMaze(mazeIn)
                        print([currPt.x, currPt.y])
                        self.counterBFSFire = len(visited)
            #print()
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
                #return current[1][0].distance
                return True
            if [current[1][0].pt.y, current[1][0].pt.x] not in visited:
                #print([current[1][0].pt.y, current[1][0].pt.x])
                if(current[1][0].pt.y+1<self.dim and mazeIn[current[1][0].pt.y+1][current[1][0].pt.x].state == '0'):
                    distanceFringe1 = self.calcDistance(current[1][0].pt.y+1, current[1][0].pt.x, finalRow, finalCol)
                    heapq.heappush(fringe, (distanceFringe1+current[1][0].distance, [cellMaze(mazeIn[current[1][0].pt.y+1][current[1][0].pt.x].pt, mazeIn[current[1][0].pt.y+1][current[1][0].pt.x].state, current[1][0].distance + 1)]))
                if(current[1][0].pt.x+1<self.dim and mazeIn[current[1][0].pt.y][current[1][0].pt.x+1].state == '0'):
                    distanceFringe2 = self.calcDistance(current[1][0].pt.y, current[1][0].pt.x+1, finalRow, finalCol)
                    heapq.heappush(fringe, (distanceFringe2+current[1][0].distance,  [cellMaze(mazeIn[current[1][0].pt.y][current[1][0].pt.x+1].pt, mazeIn[current[1][0].pt.y][current[1][0].pt.x+1].state, current[1][0].distance+1)]))
                if(current[1][0].pt.y-1>=0 and mazeIn[current[1][0].pt.y-1][current[1][0].pt.x].state == '0'):
                    distanceFringe3 = self.calcDistance(current[1][0].pt.y-1, current[1][0].pt.x, finalRow, finalCol)
                    heapq.heappush(fringe, (distanceFringe3+current[1][0].distance,  [cellMaze(mazeIn[current[1][0].pt.y-1][current[1][0].pt.x].pt, mazeIn[current[1][0].pt.y-1][current[1][0].pt.x].state, current[1][0].distance+1)]))
                if(current[1][0].pt.x-1>=0 and mazeIn[current[1][0].pt.y][current[1][0].pt.x-1].state == '0'):
                    distanceFringe4 = self.calcDistance(current[1][0].pt.y, current[1][0].pt.x-1, finalRow, finalCol)
                    heapq.heappush(fringe, (distanceFringe4+current[1][0].distance,  [cellMaze(mazeIn[current[1][0].pt.y][current[1][0].pt.x-1].pt, mazeIn[current[1][0].pt.y][current[1][0].pt.x-1].state, current[1][0].distance+1)]))
                visited.append([current[1][0].pt.y, current[1][0].pt.x])
                self.counterAStar = len(visited)
        return False

    def calcDistance(self, rows, columns, finalRow, finalCol):
        distance = math.sqrt( ((columns-finalCol)**2)+((rows-finalRow)**2) )
        return distance


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
                        mazeUse[y][x].state = '1'
        return mazeUse

#data_headerQ3 = ['bfs1 steps', 'bfs2 steps', 'q']
#with open('exportQ4.csv', 'w') as file_writerQ3:
#    writerQ3 = csv.writer(file_writerQ3)
#    writerQ3.writerow(data_headerQ3)
#
#    for x in range(0,10):
#        for y in range(0,100):
#            mazeQ3 = test(10,0.3)
#            for i in range(0, mazeQ3.dim):
#                for j in range(0, mazeQ3.dim):
#                    if mazeQ3.maze[i][j].state == '1':
#                        xLocFire = i
#                        yLocFire = j
#            initialCheck = mazeQ3.bfsForFire(0,0, xLocFire, yLocFire, mazeQ3.maze)
#            if(initialCheck != False):
#                check = mazeQ3.bfs(0,0,9,9,mazeQ3.maze)
#                if(check != False):
#                    check2 = mazeQ3.bfsWithFire1(0,0,9,9,mazeQ3.maze, y/100)
#                    check3 = mazeQ3.bfsWithFire2(0,0,9,9,mazeQ3.maze, y/100)
#                    dataQ3 = [check2, check3, y/100]
#                    writerQ3.writerow(dataQ3)

#for x in range(0,1000):
#    maze = test(5,0.3)
#    check = maze.bfsWithFire1(0,0,4,4,maze.maze,0.1)
#    check1 = maze.bfsWithFire2(0,0,4,4,maze.maze,0.1)
#    if check == True and check1 == False:
#        print("hit")
#        break

#check = maze.aStarWithFireStrat1(0,0,9,9,maze.maze, 0.1)
#check1 = maze.aStarWithFireStrat2(0,0,4,4,maze.maze, 0.1)
#check2 = maze.bfs(0,0,4,4,maze.maze)
#check3 = maze.aStar(0,0,9,9,maze.maze)
#check4 = maze.dfs(0,0,4,4,maze.maze)
#for x in range(0,1000):
#maze = test(10,0.1)
#    check = maze.bfsWithFire1(0,0,9,9,maze.maze, 0.1)
#check1 = maze.bfs(0,0,9,9,maze.maze)
#print(check1)
#    if check==True:
#        print('bfsOriginal: ', check1)
#        print("bfsfireOut: ", check)
#        break

#check6 = maze.bfsWithFire2(0,0,4,4,maze.maze, 0.1)
#print("1: ", check)
#print("2: ", check1)
#print("astar: ", check3)
#print("astar1: ", check)
#print("dfs: ", maze.counterDFS)
#print("bfs: ", check2)

#print("bfsfire2: ", check6)
Totaltime = 0
size=10
while Totaltime<10:
    maze = test(size, 0.3)
    startTime = time.time()
    check1 = maze.aStar(0,0,size-1,size-1,maze.maze)
    endTime = time.time()
    if (check1 == True):
        Totaltime = endTime-startTime
    #print("astar: ", check1)
    size+=5
Totaltime1 = 0
size1=10
while Totaltime1<10:
    maze = test(size1, 0.3)
    startTime = time.time()
    check2 = maze.dfs(0,0,size1-1,size1-1,maze.maze)
    endTime = time.time()
    if (check2 == True):
        Totaltime1 = endTime-startTime
    #print("dfs: ", check2)
    size1+=5
Totaltime2 = 0
size2=10
while Totaltime2<10:
    maze = test(size2, 0.3)
    startTime = time.time()
    check3 = maze.bfs(0,0,size2-1,size2-1,maze.maze)
    endTime = time.time()
    if (check3 == True):
        Totaltime2 = endTime-startTime
    #print("bfs: ", check3)
    size2+=5

print("Largest aStar dimensions: ", size-10)
print("Largest dfs dimensions: ", size1-10)
print("Largest bfs dimensions: ", size2-10)
