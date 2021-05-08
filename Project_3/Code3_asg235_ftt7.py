import random
import sys
import csv

class point:
    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row

#state 1 = flat, 2 = hilly, 3 = forested, 4 = maze of caves
class cell:
    def __init__(self, pt: point, state, prob):
        self.pt = pt
        self.state = state
        self.prob = prob

#make a map with each cell being randomly assigned a state
#make a FalseNegativeMap with each cell holding the chance of a false negative for that type of state
#setting a random target cell
class land:
    def __init__(self):
        self.dim = 50;
        self.FalseNegativeMap =  [ [ None for i in range(self.dim) ] for j in range(self.dim) ]
        self.map = [ [ None for i in range(self.dim) ] for j in range(self.dim) ]
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                pt = point(i,j)
                rand = random.randint(1, 4)
                c = cell(pt, rand, float.hex(1/2500))
                if rand == 1:
                    self.FalseNegativeMap[i][j] = float.hex(0.1)
                elif rand == 2:
                    self.FalseNegativeMap[i][j] = float.hex(0.3)
                elif rand == 3:
                    self.FalseNegativeMap[i][j] = float.hex(0.7)
                elif rand == 4:
                    self.FalseNegativeMap[i][j] = float.hex(0.9)
                self.map[i][j] = c

        randCol = random.randint(0, self.dim-1)
        randRow = random.randint(0, self.dim-1)
        self.target = point(randCol, randRow)

#helper method to print the land map
    def printLand(self):
        for k in range(0, self.dim):
            for m in range(0, self.dim):
                print(self.map[k][m].state,' ', end = ' ')
            print()

#helper method to print the probability map
    def printProb(self):
        for k in range(0, self.dim):
            for m in range(0, self.dim):
                print(float.fromhex(self.map[k][m].prob),' ', end = ' ')
            print()

#updates the probaility on the map by using equations from Problem 1
    def updateProb(self, col, row):
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if i == col and j == row:
                    continue
                self.map[i][j].prob = float.hex(float.fromhex(self.map[i][j].prob)/(float.fromhex(self.map[col][row].prob)*float.fromhex(self.FalseNegativeMap[col][row])+(1-float.fromhex(self.map[col][row].prob))))
        self.map[col][row].prob = float.hex((float.fromhex(self.FalseNegativeMap[col][row])*float.fromhex(self.map[col][row].prob))/(float.fromhex(self.map[col][row].prob)*float.fromhex(self.FalseNegativeMap[col][row])+(1-float.fromhex(self.map[col][row].prob))))

#used for Basic Agent 1 to search for the next cell to visit by checking all the probailities and choosing the highest one
#also calculates and returns distance needed to get to that cell
    def searchNext(self, currCol, currRow):
        points = []
        prob = round(float.fromhex(self.map[0][0].prob), 10)
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if round(float.fromhex(self.map[i][j].prob), 10)>round(prob, 10):
                    points = []
                    prob = float.fromhex(self.map[i][j].prob)
                    pt = (i,j)
                    points.append(pt)
                elif round(float.fromhex(self.map[i][j].prob), 10) == round(prob, 10):
                    pt = (i,j)
                    points.append(pt)
        col = points[0][0]
        row= points[0][1]
        distance = abs(currCol-col)+abs(currRow-row)

        for point in points:
            newDistance = abs(currCol-point[0])+abs(currRow-point[1])
            if distance>newDistance:
                distance = newDistance
                col = point[0]
                row = point[1]
        return col, row, distance

#main agent 1 method to check if we fouind the target cell and if it was successful, if not, update the probabilties and find the next cell to visit and update distance travelled
    def agent1(self):
        currCol = random.randint(0, self.dim-1)
        currRow = random.randint(0, self.dim-1)
        distance = 0
        search = 0
        while True:
            search +=1
            if self.map[currCol][currRow].pt.col == self.target.col and self.map[currCol][currRow].pt.row == self.target.row:
                if random.random() > float.fromhex(self.FalseNegativeMap[currCol][currRow]):
                    return distance+search
            self.updateProb(currCol, currRow)
            currCol, currRow, mDistance = self.searchNext(currCol, currRow)


            distance += mDistance

#search method for Basic Agent 2 taking into account the probability of finding the target
    def Agent2Search(self, currCol, currRow):
        points = []
        prob = round(float.fromhex(self.map[0][0].prob)*(1-float.fromhex(self.FalseNegativeMap[0][0])), 10)
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if round((float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))), 10)>round(prob, 10):
                    points = []
                    prob = float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))
                    pt = (i,j)
                    points.append(pt)
                elif round((float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))), 10) == round(prob, 10):
                    pt = (i,j)
                    points.append(pt)
        col = points[0][0]
        row= points[0][1]
        distance = abs(currCol-col)+abs(currRow-row)

        for pt in points:
            newDistance = abs(currCol-pt[0])+abs(currRow-pt[1])
            if distance>newDistance:
                distance = newDistance
                col = pt[0]
                row = pt[1]

        return col, row, distance

#main agent 2 method that goes thru and checks the whole maze
    def agent2(self):
        currCol = random.randint(0, self.dim-1)
        currRow = random.randint(0, self.dim-1)
        distance = 0
        search = 0
        while True:
            search +=1
            if self.map[currCol][currRow].pt.col == self.target.col and self.map[currCol][currRow].pt.row == self.target.row:
                if random.random() > float.fromhex(self.FalseNegativeMap[currCol][currRow]):
                    return distance+search
            self.updateProb(currCol, currRow)
            currCol, currRow, mDistance = self.Agent2Search(currCol, currRow)
            distance += mDistance

#imporved search based on our imporovement algorithm
    def improvedSearch(self, currCol, currRow):
        points = [(currCol, currRow)]
        pointsSecond = [(currCol, currRow)]
        prob = 0
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if abs(currCol-i)+abs(currRow-j)>50:
                    continue
                elif (round((float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))), 10) < round((float.fromhex(self.map[points[0][0]][points[0][1]].prob)*(1-float.fromhex(self.FalseNegativeMap[points[0][0]][points[0][1]]))), 10) and
                    round((float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))), 10) > round((float.fromhex(self.map[pointsSecond[0][0]][pointsSecond[0][1]].prob)*(1-float.fromhex(self.FalseNegativeMap[pointsSecond[0][0]][pointsSecond[0][1]]))), 10)):
                    pointsSecond.append((i, j))
                elif round((float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))), 10)>round(prob, 10):
                    pointsSecond = points
                    points = []
                    prob = float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))
                    pt = (i,j)
                    points.append(pt)
                elif round((float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))), 10) == round(prob, 10):
                    pt = (i,j)
                    points.append(pt)
        col = points[0][0]
        row= points[0][1]
        secondCol = pointsSecond[0][0]
        secondRow = pointsSecond[0][1]
        distanceSecond = abs(currCol-col)+abs(currRow-row) + abs(col-secondCol)+abs(row-secondRow)
        distance = 101
        if len(points)<=2:
            for pt1 in points:
                for pt2 in pointsSecond:
                    newDistance = abs(currCol-pt1[0])+abs(currRow-pt1[1])+abs(pt1[0] - pt2[0])+abs(pt1[1]-pt2[1])
                    if distance>newDistance:
                        distance = newDistance
                        col = pt1[0]
                        row = pt1[1]
                        finalDistance = abs(currCol-pt1[0])+abs(currRow-pt1[1])
        else:
            for i in range(0, len(points)):
                for j in range(0, len(points)):
                    if(i == j):
                        continue
                    newDistance = abs(currCol-points[i][0])+abs(currRow-points[i][1])+abs(points[i][0] - points[j][0])+abs(points[i][1]-points[j][1])
                    if distance>newDistance:
                        distance = newDistance
                        col = points[i][0]
                        row = points[i][1]
                        finalDistance = abs(currCol-points[i][0])+abs(currRow-points[i][1])

        return col, row, finalDistance

#improved agent main method that checks if it was success, if not search for next cell and rerun
    def improvedAgent(self):
        currCol = random.randint(0, self.dim-1)
        currRow = random.randint(0, self.dim-1)
        distance = 0
        search = 0
        while True:
            search +=1
            if self.map[currCol][currRow].pt.col == self.target.col and self.map[currCol][currRow].pt.row == self.target.row:
                if random.random() > float.fromhex(self.FalseNegativeMap[currCol][currRow]):
                    return distance+search
            self.updateProb(currCol, currRow)

            currCol, currRow, mDistance = self.improvedSearch(currCol, currRow)
            distance += mDistance
