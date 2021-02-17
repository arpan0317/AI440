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
                print(self.maze[i][j].state, end = ' ')
            print()




#    def dfsOg(self, rows, columns, finalRow, finalCol, mazeIn):
#        current = [rows, columns]
#        if (self.foundDFS):
#            return True
#        if mazeIn[rows][columns].state != '0' or current in self.visited:
#            return False
#
#        self.visited.append(current)
#
#        if rows == finalRow and columns == finalCol:
#            self.foundDFS = True
#
#        print(rows, columns)
#        if rows+1<self.dim:
#            self.dfs(rows+1, columns, finalRow, finalCol, mazeIn)
#        if columns+1<self.dim:
#            self.dfs(rows, columns+1, finalRow, finalCol, mazeIn)
#        if rows-1>0:
#            self.dfs(rows-1, columns, finalRow, finalCol, mazeIn)
#        if columns-1>0:
#            self.dfs(rows, columns-1, finalRow, finalCol, mazeIn)
#
#        return self.foundDFS


#    def dfsOg(self, rows, columns, finalRow, finalCol, mazeIn):
#        mazeUse = copy.deepcopy(mazeIn)
#        if mazeUse[rows][columns].state!='0':
#            return False
#        fringe = []
#        visited = []
#        fringe.append([rows,columns])
#
#        while fringe:
#            current = fringe.pop()
#
#            if (current[0] == finalRow and current[1] == finalCol):
#                return True
#            if current not in visited:
#                #print(current[0], current[1])
#                if(current[0]+1<self.dim and mazeUse[current[0]+1][current[1]].state == '0'):
#                    fringe.append([current[0]+1, current[1]])
#                if(current[1]+1<self.dim and mazeUse[current[0]][current[1]+1].state == '0'):
#                    fringe.append([current[0], current[1]+1])
#                if(current[0]-1>0 and mazeUse[current[0]-1][current[1]].state == '0'):
#                    fringe.append([current[0]-1, current[1]])
#                if(current[1]-1>0 and mazeUse[current[0]][current[1]-1].state == '0'):
#                    fringe.append([current[0], current[1]-1])
#                visited.append(current)
#                self.counterDFS = len(visited)
#
#        return False

    def dfs(self, rows, columns, finalRow, finalCol, mazeIn):
        mazeUse = copy.deepcopy(mazeIn)
        if mazeUse[rows][columns].state!='0':
            return False
        fringe = []
        visited = []
        fringe.append(mazeUse[rows][columns])
        while fringe:
            current = fringe.pop()
            #print(current[0][0], current[0][1], mazeIn[current[0][0]][current[0][1]].distance)
            #print(self.counterBFS)
            currPt = current.pt
            if (currPt.y == finalRow and currPt.x == finalCol):
                return current.distance
            if ([currPt.y, currPt.x]) not in visited:
                if(currPt.y+1<self.dim and mazeUse[currPt.y+1][currPt.x].state == '0'):
                    fringe.append(cellMaze( mazeUse[currPt.y+1][currPt.x].pt, mazeUse[currPt.y+1][currPt.x].state, current.distance+1))
                if(currPt.x+1<self.dim and mazeUse[currPt.y][currPt.x+1].state == '0'):
                    fringe.append(cellMaze(mazeUse[currPt.y][currPt.x+1].pt, mazeUse[currPt.y][currPt.x+1].state, current.distance+1))
                if(currPt.y-1>0 and mazeUse[currPt.y-1][currPt.x].state == '0'):
                    fringe.append(cellMaze(mazeUse[currPt.y-1][currPt.x].pt, mazeUse[currPt.y-1][currPt.x].state, current.distance+1))
                if(currPt.x-1>0 and mazeUse[currPt.y][currPt.x-1].state == '0'):
                    fringe.append(cellMaze(mazeUse[currPt.y][currPt.x-1].pt, mazeUse[currPt.y][currPt.x-1].state, current.distance+1))
                visited.append([currPt.y, currPt.x])
                self.counterDFS = len(visited)
        return False


    def bfs(self, rows, columns, finalRow, finalCol, mazeIn):
        mazeUse = copy.deepcopy(mazeIn)
        if mazeUse[rows][columns].state!='0':
            return False
        fringe = []
        visited = []
        fringe.append(mazeUse[rows][columns])
        while fringe:
            current = fringe.pop(0)
            #print(current[0][0], current[0][1], mazeIn[current[0][0]][current[0][1]].distance)
            #print(self.counterBFS)
            currPt = current.pt
            if (currPt.y == finalRow and currPt.x == finalCol):
                return current.distance
            if ([currPt.y, currPt.x]) not in visited:
                if(currPt.y+1<self.dim and mazeUse[currPt.y+1][currPt.x].state == '0'):
                    fringe.append(cellMaze( mazeUse[currPt.y+1][currPt.x].pt, mazeUse[currPt.y+1][currPt.x].state, current.distance+1))
                if(currPt.x+1<self.dim and mazeUse[currPt.y][currPt.x+1].state == '0'):
                    fringe.append(cellMaze(mazeUse[currPt.y][currPt.x+1].pt, mazeUse[currPt.y][currPt.x+1].state, current.distance+1))
                if(currPt.y-1>0 and mazeUse[currPt.y-1][currPt.x].state == '0'):
                    fringe.append(cellMaze(mazeUse[currPt.y-1][currPt.x].pt, mazeUse[currPt.y-1][currPt.x].state, current.distance+1))
                if(currPt.x-1>0 and mazeUse[currPt.y][currPt.x-1].state == '0'):
                    fringe.append(cellMaze(mazeUse[currPt.y][currPt.x-1].pt, mazeUse[currPt.y][currPt.x-1].state, current.distance+1))
                visited.append([currPt.y, currPt.x])
                self.counterBFS = len(visited)
        return False


    def aStar(self, rows, columns, finalRow, finalCol, mazeIn):
        mazeUse = copy.deepcopy(mazeIn)
        if mazeUse[rows][columns].state!='0':
            return False
        fringe = []
        visited = []
        distance = self.calcDistance(rows, columns, finalRow, finalCol)
        heapq.heapify(fringe)
        heapq.heappush(fringe, (distance, [mazeUse[rows][columns]]))


        while fringe:
            current = heapq.heappop(fringe)
            #print("current: ", (current[0], current[1]))
            #print(self.counterAStar)
            if (current[1][0].pt.y == finalRow and current[1][0].pt.x == finalCol):
                return current[1][0].distance
            if [current[1][0].pt.y, current[1][0].pt.x] not in visited:
                if(current[1][0].pt.y+1<self.dim and mazeUse[current[1][0].pt.y+1][current[1][0].pt.x].state == '0'):
                    distanceFringe1 = self.calcDistance(current[1][0].pt.y+1, current[1][0].pt.x, finalRow, finalCol)
                    #print("1: ", distanceFringe1)
                    heapq.heappush(fringe, (distanceFringe1, [cellMaze(mazeUse[current[1][0].pt.y+1][current[1][0].pt.x].pt, mazeUse[current[1][0].pt.y+1][current[1][0].pt.x].state, current[1][0].distance + 1)]))
                if(current[1][0].pt.x+1<self.dim and mazeUse[current[1][0].pt.y][current[1][0].pt.x+1].state == '0'):
                    distanceFringe2 = self.calcDistance(current[1][0].pt.y, current[1][0].pt.x+1, finalRow, finalCol)
                    #print("2: ", distanceFringe2)
                    heapq.heappush(fringe, (distanceFringe2,  [cellMaze(mazeUse[current[1][0].pt.y][current[1][0].pt.x+1].pt, mazeUse[current[1][0].pt.y][current[1][0].pt.x+1].state, current[1][0].distance+1)]))
                if(current[1][0].pt.y-1>0 and mazeUse[current[1][0].pt.y-1][current[1][0].pt.x].state == '0'):
                    distanceFringe3 = self.calcDistance(current[1][0].pt.y-1, current[1][0].pt.x, finalRow, finalCol)
                    #print("3: ", distanceFringe3)
                    heapq.heappush(fringe, (distanceFringe3,  [cellMaze(mazeUse[current[1][0].pt.y-1][current[1][0].pt.x].pt, mazeUse[current[1][0].pt.y-1][current[1][0].pt.x].state, current[1][0].distance+1)]))
                if(current[1][0].pt.x-1>0 and mazeUse[current[1][0].pt.y][current[1][0].pt.x-1].state == '0'):
                    distanceFringe4 = self.calcDistance(current[1][0].pt.y, current[1][0].pt.x-1, finalRow, finalCol)
                    #print("4: ", distanceFringe4)
                    heapq.heappush(fringe, (distanceFringe4,  [cellMaze(mazeUse[current[1][0].pt.y][current[1][0].pt.x-1].pt, mazeUse[current[1][0].pt.y][current[1][0].pt.x-1].state, current[1][0].distance+1)]))
                visited.append([current[1][0].pt.y, current[1][0].pt.x])
                self.counterAStar = len(visited)
        return False

    def calcDistance(self, rows, columns, finalRow, finalCol):
        distance = math.sqrt( ((columns-finalCol)**2)+((rows-finalRow)**2) )
        return distance

data_headerQ2 = ['density', 'reached']
with open('exportQ2.csv', 'w') as file_writerQ2:
    writerQ2 = csv.writer(file_writerQ2)
    writerQ2.writerow(data_headerQ2)

    for probQ2 in range(1,100):
        for countQ2 in range(0,10):
            mazeQ2 = test(20,probQ2/100)
            checkQ2 = mazeQ2.dfs(0,0,19,19,mazeQ2.maze)
            #print(checkQ2)
            dataQ2 = [probQ2/100, checkQ2]
            writerQ2.writerow(dataQ2)
        #print(probQ2/100)

#data_headerQ3 = ['difference', 'reachedBFS', 'reachedAStar', 'prob']
#with open('exportQ3.csv', 'w') as file_writerQ3:
#    writerQ3 = csv.writer(file_writerQ3)
#    writerQ3.writerow(data_headerQ3)
#
#    for probQ3 in range(1,100):
#        for countQ3 in range(0,10):
#            mazeQ3 = test(20,probQ3/100)
#            check = mazeQ3.bfs(0,0,19,19,mazeQ3.maze)
#            #print(check)
#            check2 = mazeQ3.aStar(0,0,19,19,mazeQ3.maze)
#            #print(check2)
#            differenceAStarBFS = mazeQ3.counterBFS - mazeQ3.counterAStar
#            #print(mazeQ3.counterBFS)
#            #print(mazeQ3.counterAStar)
#            #print(mazeQ3.counterDFS)
#            dataQ3 = [differenceAStarBFS, check, check2, probQ3/100]
#            writerQ3.writerow(dataQ3)
#        #print(probQ3/100)


maze = test(100,0.3)
#check = maze.aStar(0,0,19,19,maze.maze)
#print(check)

check1 = maze.bfs(0,0,99,99,maze.maze)
print("bfs: ", check1, maze.counterBFS)
check2 = maze.dfs(0,0,99,99,maze.maze)
print("dfs: ", check2, maze.counterDFS)
check3 = maze.aStar(0,0,99,99,maze.maze)
print("astar: ", check3, maze.counterAStar)
#print("moving to bfs")
#print(maze.counterBFS)




#print("moving to bfs")
#check1 = maze.bfs(0,0,199,199,maze.maze)
#print(check1)
#print("moving to astar")
#check2 = maze.aStar(0,0,9,9,maze.maze)
#print(check2)
