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


class maze:
    def __init__(self):
        self.falseFlat = 0.1
        self.falseHilly = 0.3
        self.falseForested = 0.7
        self.falseMaze = 0.9
        dim = 50;
        self.map = [ [ None for i in range(dim) ] for j in range(dim) ]
        for i in range(0, dim):
            for j in range(0, dim):
                pt = point(i,j)
                rand = random.randint(1, 4)
                c = cell(pt, rand, 1/2500)
                self.map[i][j] = c

        randCol = random.randint(0, dim-1)
        randRow = random.randint(0, dim-1)
        self.target = point(randCol, randRow)


    def printMaze
        #for k in range(0, dim):
        #    for m in range(0, dim):
        #        print(self.map[k][m].state,' ', end = ' ')


mazeTest = maze()
