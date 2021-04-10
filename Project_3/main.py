from fraction import fraction
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


class land:
    def __init__(self):
        self.dim = 3;
        self.FalseNegativeMap =  [ [ None for i in range(self.dim) ] for j in range(self.dim) ]
        self.map = [ [ None for i in range(self.dim) ] for j in range(self.dim) ]
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                pt = point(i,j)
                rand = random.randint(1, 4)
                c = cell(pt, rand, 1/9)
                if rand == 1:
                    self.FalseNegativeMap[i][j] = 0.1
                elif rand == 2:
                    self.FalseNegativeMap[i][j] = 0.3
                elif rand == 3:
                    self.FalseNegativeMap[i][j] = 0.7
                elif rand == 4:
                    self.FalseNegativeMap[i][j] = 0.9
                self.map[i][j] = c
        self.Agent2Map =  self.map

        randCol = random.randint(0, self.dim-1)
        randRow = random.randint(0, self.dim-1)
        self.target = point(randCol, randRow)

    def printLand(self):
        for k in range(0, self.dim):
            for m in range(0, self.dim):
                print(self.map[k][m].state,' ', end = ' ')
            print()

    def printProb(self):
        for k in range(0, self.dim):
            for m in range(0, self.dim):
                print(self.map[k][m].prob,' ', end = ' ')
            print()

    def updateProb(self, col, row):
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if i == col and j == row:
                    continue
                self.map[i][j].prob = (self.map[i][j].prob)/(self.map[col][row].prob*self.FalseNegativeMap[col][row]+(1-self.map[col][row].prob))
        self.map[col][row].prob = (self.FalseNegativeMap[col][row]*self.map[col][row].prob)/(self.map[col][row].prob*self.FalseNegativeMap[col][row]+(1-self.map[col][row].prob))
        self.printProb()
        print()

    def searchNext(self, currCol, currRow):
        points = []
        prob = self.map[0][0].prob
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if self.map[i][j].prob>prob:
                    points = []
                    prob = self.map[i][j].prob
                    pt = (i,j)
                    points.append(pt)
                elif self.map[i][j].prob == prob:
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

    def agent1(self):
        self.printLand()
        print("Target Row: ", self.target.col)
        print("Target Col: ", self.target.row)
        print()
        currCol = random.randint(0, self.dim-1)
        currRow = random.randint(0, self.dim-1)
        distance = 0
        search = 0
        while True:
            search +=1
            print("Row: ", currCol)
            print("Col: ", currRow)
            if self.map[currCol][currRow].pt.col == self.target.col and self.map[currCol][currRow].pt.row == self.target.row:
                if random.random() > self.FalseNegativeMap[currCol][currRow]:
                    print('type: ', self.map[currCol][currRow].state)
                    return distance+search
            self.updateProb(currCol, currRow)
            currCol, currRow, mDistance = self.searchNext(currCol, currRow)


            distance += mDistance

    def Agent2Search(self, currCol, currRow):
        points = []
        print()
        prob = self.map[0][0].prob*(1-self.FalseNegativeMap[0][0])
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                print((self.map[i][j].prob*(1-self.FalseNegativeMap[i][j])), ' ', end = ' ')
                if (self.map[i][j].prob*(1-self.FalseNegativeMap[i][j]))>prob:
                    points = []
                    prob = self.map[i][j].prob*(1-self.FalseNegativeMap[i][j])
                    pt = (i,j)
                    points.append(pt)
                elif (self.map[i][j].prob*(1-self.FalseNegativeMap[i][j])) == prob:
                    pt = (i,j)
                    points.append(pt)
            print()
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

    def agent2(self):
        self.printLand()
        print("Target Row: ", self.target.col)
        print("Target Col: ", self.target.row)
        print()
        currCol = random.randint(0, self.dim-1)
        currRow = random.randint(0, self.dim-1)
        distance = 0
        search = 0
        while True:
            search +=1
            print("Row: ", currCol)
            print("Col: ", currRow)
            if self.map[currCol][currRow].pt.col == self.target.col and self.map[currCol][currRow].pt.row == self.target.row:
                if random.random() > self.FalseNegativeMap[currCol][currRow]:
                    print('type: ', self.map[currCol][currRow].state)
                    return distance+search
            self.updateProb(currCol, currRow)
            currCol, currRow, mDistance = self.Agent2Search(currCol, currRow)


            distance += mDistance

landTest = land()
score = landTest.agent2()
print('score: ', score)
