from fractions import Fraction
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
        self.dim = 25;
        self.FalseNegativeMap =  [ [ None for i in range(self.dim) ] for j in range(self.dim) ]
        self.map = [ [ None for i in range(self.dim) ] for j in range(self.dim) ]
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                pt = point(i,j)
                rand = random.randint(1, 4)
                c = cell(pt, rand, float.hex(1/625))
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

    def printLand(self):
        for k in range(0, self.dim):
            for m in range(0, self.dim):
                print(self.map[k][m].state,' ', end = ' ')
            print()

    def printProb(self):
        for k in range(0, self.dim):
            for m in range(0, self.dim):
                print(float.fromhex(self.map[k][m].prob),' ', end = ' ')
            print()

    def updateProb(self, col, row):
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if i == col and j == row:
                    continue
                self.map[i][j].prob = float.hex(float.fromhex(self.map[i][j].prob)/(float.fromhex(self.map[col][row].prob)*float.fromhex(self.FalseNegativeMap[col][row])+(1-float.fromhex(self.map[col][row].prob))))
        self.map[col][row].prob = float.hex((float.fromhex(self.FalseNegativeMap[col][row])*float.fromhex(self.map[col][row].prob))/(float.fromhex(self.map[col][row].prob)*float.fromhex(self.FalseNegativeMap[col][row])+(1-float.fromhex(self.map[col][row].prob))))
        #self.printProb()
        #print()

    def searchNext(self, currCol, currRow):
        points = []
        prob = round(float.fromhex(self.map[0][0].prob), 10)
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                #print("new prob, old prob: ", round(float.fromhex(self.map[i][j].prob), 10), round(prob, 10))
                if round(float.fromhex(self.map[i][j].prob), 10)>round(prob, 10):
                    points = []
                    prob = float.fromhex(self.map[i][j].prob)
                    pt = (i,j)
                    points.append(pt)
                elif round(float.fromhex(self.map[i][j].prob), 10) == round(prob, 10):
                    pt = (i,j)
                    points.append(pt)
                #print(points)
        col = points[0][0]
        row= points[0][1]
        #print("col, row in search next: ", col, row)
        distance = abs(currCol-col)+abs(currRow-row)

        for point in points:
        #    print("col, row: ", point[0], point[1])
            newDistance = abs(currCol-point[0])+abs(currRow-point[1])
            if distance>newDistance:
                distance = newDistance
                col = point[0]
                row = point[1]
        #print("distance in search next: ", distance)
        return col, row, distance

    def agent1(self):
        #self.printLand()
        #print("Target Row: ", self.target.col)
        #print("Target Col: ", self.target.row)
        #print()
        currCol = random.randint(0, self.dim-1)
        currRow = random.randint(0, self.dim-1)
        distance = 0
        search = 0
        while True:
            search +=1
            #print("Row: ", currCol)
            #print("Col: ", currRow)
            if self.map[currCol][currRow].pt.col == self.target.col and self.map[currCol][currRow].pt.row == self.target.row:
                if random.random() > float.fromhex(self.FalseNegativeMap[currCol][currRow]):
                    #print('type: ', self.map[currCol][currRow].state)
                    #print("distance in agent 1: ", distance)
                    return distance+search
            self.updateProb(currCol, currRow)
            currCol, currRow, mDistance = self.searchNext(currCol, currRow)


            distance += mDistance

    def Agent2Search(self, currCol, currRow):
        points = []
        #print()
        prob = round(float.fromhex(self.map[0][0].prob)*(1-float.fromhex(self.FalseNegativeMap[0][0])), 10)
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                #print((float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))), ' ', end = ' ')
                if round((float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))), 10)>round(prob, 10):
                    points = []
                    prob = float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))
                    pt = (i,j)
                    points.append(pt)
                elif round((float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))), 10) == round(prob, 10):
                    pt = (i,j)
                    points.append(pt)
            #print()
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

    def agent2(self):
        #self.printLand()
        #print("Target Row: ", self.target.col)
        #print("Target Col: ", self.target.row)
        #print()
        currCol = random.randint(0, self.dim-1)
        currRow = random.randint(0, self.dim-1)
        distance = 0
        search = 0
        while True:
            search +=1
            #print("Row: ", currCol)
            #print("Col: ", currRow)
            if self.map[currCol][currRow].pt.col == self.target.col and self.map[currCol][currRow].pt.row == self.target.row:
                if random.random() > float.fromhex(self.FalseNegativeMap[currCol][currRow]):
                    #print('type: ', self.map[currCol][currRow].state)
                    return distance+search
            self.updateProb(currCol, currRow)
            #self.printProb()
            #print()
            currCol, currRow, mDistance = self.Agent2Search(currCol, currRow)
            distance += mDistance

    def improvedSearch(self, currCol, currRow):
        points = [(currCol, currRow)]
        pointsSecond = [(currCol, currRow)]
        #print()
        prob = 0
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                #print((float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))), ' ', end = ' ')
                if (round((float.fromhex(self.map[i][j].prob)*(1-float.fromhex(self.FalseNegativeMap[i][j]))), 10) < round((float.fromhex(self.map[points[0][0]][points[0][1]].prob)*(1-float.fromhex(self.FalseNegativeMap[points[0][0]][points[0][1]]))), 10) and
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

            #print()
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
                    #print("curr dist: ", distance)
                    #print("new dist + coordi, coordj: ", newDistance, points[i][0], points[i][1], points[j][0], points[j][1])
                    if distance>newDistance:
                        distance = newDistance
                        col = points[i][0]
                        row = points[i][1]
                        finalDistance = abs(currCol-points[i][0])+abs(currRow-points[i][1])

        return col, row, finalDistance

    def improvedAgent(self):
        #self.printLand()
        #print("Target Row: ", self.target.col)
        #print("Target Col: ", self.target.row)
        #print()
        currCol = random.randint(0, self.dim-1)
        currRow = random.randint(0, self.dim-1)
        distance = 0
        search = 0
        while True:
            search +=1
            #print("Row: ", currCol)
            #print("Col: ", currRow)
            if self.map[currCol][currRow].pt.col == self.target.col and self.map[currCol][currRow].pt.row == self.target.row:
                if random.random() > float.fromhex(self.FalseNegativeMap[currCol][currRow]):
                    #print('type: ', self.map[currCol][currRow].state)
                    return distance+search
            self.updateProb(currCol, currRow)
            #self.printProb()
            #print()
            currCol, currRow, mDistance = self.improvedSearch(currCol, currRow)
            distance += mDistance


scoreAgent1 = 0
for i in range(0, 100):
    #print(i)
    landTest1 = land()
    score1 = landTest1.agent1()
    #print(score1)
    scoreAgent1 += score1

print("Agent1: ", scoreAgent1/100)

scoreAgent2 = 0
for j in range(0, 100):
    #print(j)
    landTest2 = land()
    score2 = landTest2.agent2()
    #print(score2)
    scoreAgent2 += score2

print("Agent2: ", scoreAgent2/100)

scoreAgentAdv = 0
for k in range(0, 100):
    #print(k)
    landTestAdv = land()
    scoreAdv = landTestAdv.improvedAgent()
    #print(scoreAdv)
    scoreAgentAdv += scoreAdv

print("AgentAdv: ", scoreAgentAdv/100)

#landTest = land()
#score1 = landTest.agent1()
#print(score1)

#landTest2 = land()
#score2 = landTest2.agent2()
#print(score2)

#landTestAdv = land()
#scoreAdv = landTestAdv.improvedAgent()
#print(scoreAdv)
