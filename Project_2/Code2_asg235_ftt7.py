import random
import sys
import csv

class point:
    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row

class cell:
    def __init__(self, pt: point, state = 'X'):
        self.pt = pt
        self.state = state

class minesweeper:
    def __init__(self, dim, numMines):
        sys.setrecursionlimit(5000)
        self.dim = dim
        self.numMines = numMines
        self.numBombs = 0
        self.checkerQueue = []
        self.safeQueue = []
        counter = numMines
        self.mapUser = [ [ None for i in range(dim) ] for j in range(dim) ]
        self.mapInternal = [ [ None for m in range(dim) ] for n in range(dim) ]
        #user maze made below
        for i in range(0, dim):
            for j in range(0, dim):
                pt = point(i,j)
                c = cell(pt, 'X')
                self.mapUser[i][j] = c

        while counter > 0:
            col = random.randint(0, dim-1)
            row = random.randint(0, dim-1)
            if self.mapInternal[col][row] is None:
                counter = counter - 1
            pt = point(col, row)
            self.mapInternal[col][row] = cell(pt, '-1')

        #filling out non-mine cells in MapInternal
        for m in range(0, dim):
            for n in range(0, dim):
                if (self.mapInternal[m][n] is None):
                    pt = point(m, n)
                    self.mapInternal[m][n] = cell(pt, self.checkNeighborMine(self.mapInternal, pt))

    #checks how many neighbors there are that are mines and returns that count
    def checkNeighborMine(self, map, currPt):
        count = 0
        # check left
        if(currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row] is not None and (map[currPt.col-1][currPt.row].state == '-1' or map[currPt.col-1][currPt.row].state == 'M')):
                count +=1
        #check right
        if (currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row] is not None and (map[currPt.col+1][currPt.row].state == '-1' or map[currPt.col+1][currPt.row].state == 'M') ):
                count +=1
        #check top
        if(currPt.row-1 >= 0):
            if(map[currPt.col][currPt.row-1] is not None and (map[currPt.col][currPt.row-1].state == '-1' or map[currPt.col][currPt.row-1].state == 'M')):
                count +=1
        #check bottom
        if (currPt.row+1 < self.dim):
            if(map[currPt.col][currPt.row+1] is not None and (map[currPt.col][currPt.row+1].state == '-1' or map[currPt.col][currPt.row+1].state == 'M' )):
                count +=1
        #check lower left
        if(currPt.row-1 >= 0 and currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row-1] is not None and (map[currPt.col-1][currPt.row-1].state == '-1' or map[currPt.col-1][currPt.row-1].state == 'M' )):
                count +=1
        #check upper left
        if (currPt.row+1 < self.dim and currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row+1] is not None and (map[currPt.col-1][currPt.row+1].state == '-1' or map[currPt.col-1][currPt.row+1].state == 'M')):
                count +=1
        #check Lower right
        if(currPt.row+1 < self.dim and currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row+1] is not None and (map[currPt.col+1][currPt.row+1].state == '-1' or map[currPt.col+1][currPt.row+1].state == 'M')):
                count +=1
        #check Upper right
        if(currPt.row-1 >= 0 and currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row-1] is not None and (map[currPt.col+1][currPt.row-1].state == '-1' or map[currPt.col+1][currPt.row-1].state == 'M' )):
                count +=1

        return count

    #prints the map in a format that is readable
    def printMap(self, map):
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if map[i][j] is None:
                    print('E', end = ' ')
                else:
                    print(map[i][j].state,' ', ' ', end = ' ')
            print()

    #main method for the basic agent (reference to james bond - agent007 but this is the basic version so agent003). It calls agentRecurse which is the recursive method.
    #returns the score that the agent gets
    def agent003(self):
        col = random.randint(0, self.dim-1)
        row = random.randint(0, self.dim-1)
        self.agentRecurse(point(row, col))
        score = self.countScore(self.mapUser)
        return score

    #main method for the advanced agent (reference to james bond - agent007). It calls agentRecurseAdvance which is the recursive method.
    #returns the score that the agent gets
    def agent007(self):
        col = random.randint(0, self.dim-1)
        row = random.randint(0, self.dim-1)
        visited = []
        self.agentRecurseAdvance(point(row, col), visited)
        score = self.countScore(self.mapUser)
        return score

    #recursive agent that gets called for every point.
    #inside, checks if an inference can be made, checks neighbors of neighbors by using method agentRecursveAdvanceNew which does not call random points, and keeps running till the entire maze is shown or marked.
    #returns once it is done executing and goes back to finish agent007
    def agentRecurseAdvance(self, sPoint: point, visited):
        valueMap = self.mapInternal[sPoint.col][sPoint.row].state
        self.mapUser[sPoint.col][sPoint.row] = cell(point(sPoint.col, sPoint.row), valueMap)
        if self.numBombs == self.numMines:
            return
        if not self.allChecked(self.mapUser):
            return
        if(valueMap == '-1'):
            self.numBombs += 1
            normQueue = self.numOfSafeNeighbors(self.mapUser, sPoint)[1]

            organizedQueue = self.chooseNeighbor(self.mapUser, normQueue)
            while organizedQueue:
                spoint = organizedQueue.pop(0)
                if not self.allChecked(self.mapUser):
                    return
                self.agentRecurseAdvanceNew(spoint, visited)

            if not self.allChecked(self.mapUser):
                return
            visited = []
            rand = self.randomCell(self.mapUser)
            self.agentRecurseAdvance(point(rand[0], rand[1]), visited)
        elif(valueMap - self.checkNeighborMine(self.mapUser, sPoint) == self.numOfHiddenNeighbors(self.mapUser, sPoint)):
            numAndQueue = self.markAllNeighbors(self.mapUser, sPoint)
            self.numBombs += numAndQueue[0]
            if not self.allChecked(self.mapUser):
                return
            visited = []
            for z in range(0, len(numAndQueue[1])):
                neighborQueueReg = self.numOfSafeNeighbors(self.mapUser, point(numAndQueue[1][z].col, numAndQueue[1][z].row))[1]``
                if not self.allChecked(self.mapUser):
                    return
                for y in range(0, len(neighborQueueReg)):
                    if not self.allChecked(self.mapUser):
                        return
                    self.agentRecurseAdvanceNew(point(neighborQueueReg[y].col, neighborQueueReg[y].row), visited)
            if not self.allChecked(self.mapUser):
                return
            rand = self.randomCell(self.mapUser)
            self.agentRecurseAdvance(point(rand[0], rand[1]), visited)
        elif(self.neighborCheck(self.mapUser, sPoint)-valueMap-self.numOfSafeNeighbors(self.mapUser,sPoint)[0] == self.numOfHiddenNeighbors(self.mapUser, sPoint)):
            self.markAllSafeNeighbors(self.mapUser, sPoint)
            organizedQueue = self.chooseNeighbor(self.mapUser, self.checkerQueue)
            while organizedQueue:
                checker = True
                spoint = organizedQueue.pop(0)
                for k in range(0, len(visited)):
                    pointToCompare = visited[k]
                    if not self.allChecked(self.mapUser):
                        return
                    if spoint.col == pointToCompare.col and spoint.row == pointToCompare.row:
                        checker = False
                        break
                if checker:
                    visited.append(spoint)
                    self.agentRecurseAdvanceNew(point(spoint.col, spoint.row), visited)
            if not self.allChecked(self.mapUser):
                return
            visited = []
            rand = self.randomCell(self.mapUser)
            self.agentRecurseAdvance(point(rand[0], rand[1]), visited)
        else:
            normQueue = self.numOfSafeNeighbors(self.mapUser, sPoint)[1]
            organizedQueue = self.chooseNeighbor(self.mapUser, normQueue)
            while organizedQueue:
                checker = True

                spoint = organizedQueue.pop(0)
                for k in range(0, len(visited)):
                    pointToCompare = visited[k]
                    if not self.allChecked(self.mapUser):
                        return
                    if spoint.col == pointToCompare.col and spoint.row == pointToCompare.row:
                        checker = False
                        break
                if checker:
                    visited.append(spoint)
                    self.agentRecurseAdvanceNew(point(spoint.col, spoint.row), visited)
            if not self.allChecked(self.mapUser):
                return
            visited = []
            rand = self.randomCell(self.mapUser)
            self.agentRecurseAdvance(point(rand[0], rand[1]), visited)
            if not self.allChecked(self.mapUser):
                return

    #same as agentRecurseAdvance except does not call random point when no inferences can be made, rather just returns back to agentRecurseAdvance
    def agentRecurseAdvanceNew(self, sPoint: point, visited):
        valueMap = self.mapInternal[sPoint.col][sPoint.row].state
        self.mapUser[sPoint.col][sPoint.row] = cell(point(sPoint.col, sPoint.row), valueMap)
        if not self.allChecked(self.mapUser):
            return
        if(valueMap == '-1'):
            self.numBombs += 1
            normQueue = self.numOfSafeNeighbors(self.mapUser, sPoint)[1]

            organizedQueue = self.chooseNeighbor(self.mapUser, normQueue)
            while organizedQueue:
                spoint = organizedQueue.pop(0)
                if not self.allChecked(self.mapUser):
                    return
                self.agentRecurseAdvanceNew(spoint, visited)

            if not self.allChecked(self.mapUser):
                return
            return
        elif(valueMap - self.checkNeighborMine(self.mapUser, sPoint) == self.numOfHiddenNeighbors(self.mapUser, sPoint)):
            numAndQueue = self.markAllNeighbors(self.mapUser, sPoint)
            self.numBombs += numAndQueue[0]
            if not self.allChecked(self.mapUser):
                return
            visited = []
            for z in range(0, len(numAndQueue[1])):
                neighborQueueReg = self.numOfSafeNeighbors(self.mapUser, point(numAndQueue[1][z].col, numAndQueue[1][z].row))[1]
                if not self.allChecked(self.mapUser):
                    return
                for y in range(0, len(neighborQueueReg)):
                    if not self.allChecked(self.mapUser):
                        return
                    self.agentRecurseAdvanceNew(point(neighborQueueReg[y].col, neighborQueueReg[y].row), visited)
            if not self.allChecked(self.mapUser):
                return
            return
        elif(self.neighborCheck(self.mapUser, sPoint)-valueMap-self.numOfSafeNeighbors(self.mapUser,sPoint)[0] == self.numOfHiddenNeighbors(self.mapUser, sPoint)):
            self.markAllSafeNeighbors(self.mapUser, sPoint)
            organizedQueue = self.chooseNeighbor(self.mapUser, self.checkerQueue)
            while organizedQueue:
                checker = True
                spoint = organizedQueue.pop(0)
                for k in range(0, len(visited)):
                    pointToCompare = visited[k]
                    if not self.allChecked(self.mapUser):
                        return
                    if spoint.col == pointToCompare.col and spoint.row == pointToCompare.row:
                        checker = False
                        break
                if checker:
                    visited.append(spoint)
                    self.agentRecurseAdvanceNew(point(spoint.col, spoint.row), visited)
            if not self.allChecked(self.mapUser):
                return
            return
        else:
            normQueue = self.numOfSafeNeighbors(self.mapUser, sPoint)[1]
            organizedQueue = self.chooseNeighbor(self.mapUser, normQueue)
            while organizedQueue:
                checker = True

                spoint = organizedQueue.pop(0)
                for k in range(0, len(visited)):
                    pointToCompare = visited[k]
                    if not self.allChecked(self.mapUser):
                        return
                    if spoint.col == pointToCompare.col and spoint.row == pointToCompare.row:
                        checker = False
                        break
                if checker:
                    visited.append(spoint)
                    self.agentRecurseAdvanceNew(point(spoint.col, spoint.row), visited)
            if not self.allChecked(self.mapUser):
                return
            return

    #counts the score by checking how many M there are on the map
    def countScore(self, map):
        score = 0
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if map[i][j].state == 'M':
                    score +=1
        return score

    #recursive agent that gets called for every point.
    #inside, checks if an inference can be made, and keeps running till the entire maze is shown or marked.
    #returns once it is done executing and goes back to finish agent003
    def agentRecurse(self, sPoint: point):
        valueMap = self.mapInternal[sPoint.col][sPoint.row].state
        self.mapUser[sPoint.col][sPoint.row] = cell(point(sPoint.col, sPoint.row), valueMap)
        if not self.allChecked(self.mapUser):
            return
        if(valueMap == '-1'):
            rand = self.randomCell(self.mapUser)
            self.agentRecurse(point(rand[0], rand[1]))
        elif(valueMap - self.checkNeighborMine(self.mapUser, sPoint) == self.numOfHiddenNeighbors(self.mapUser, sPoint)):
            num = self.markAllNeighbors(self.mapUser, sPoint)[0]
            if not self.allChecked(self.mapUser):
                return
            rand = self.randomCell(self.mapUser)
            self.agentRecurse(point(rand[0], rand[1]))
        elif(self.neighborCheck(self.mapUser, sPoint)-valueMap-self.numOfSafeNeighbors(self.mapUser,sPoint)[0] == self.numOfHiddenNeighbors(self.mapUser, sPoint)):
            self.markAllSafeNeighbors(self.mapUser, sPoint)
            while self.checkerQueue :
                spoint = self.checkerQueue.pop(0)
                self.agentRecurse(spoint)
            if not self.allChecked(self.mapUser):
                return
            rand = self.randomCell(self.mapUser)
            self.agentRecurse(point(rand[0], rand[1]))
        else:
            rand = self.randomCell(self.mapUser)
            self.agentRecurse(point(rand[0], rand[1]))
            if not self.allChecked(self.mapUser):
                return

    #checks if all the cells have been opened
    #returns true if they have, returns false otherwise
    def allChecked(self, map):
        checker = False
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if map[i][j].state == 'X':
                    return True
        return checker

    #organizes the neighbor queue based on priority - first all 0's, then the highest clue values
    #returns modified neighbor queue
    def chooseNeighbor(self, map, inQueue):

        pointList = []
        finalPointList = []
        for q in range(0, len(inQueue)):
            pointList.append(inQueue[q])
        for m in range(0, len(inQueue)):
            neighborQueue = self.numOfSafeNeighbors(self.mapUser, point(inQueue[m].col, inQueue[m].row))[1]
            for n in range(0, len(neighborQueue)):
                checker = True
                for b in range(0, len(pointList)):

                    pointCompare = pointList[b]
                    if pointCompare.col == neighborQueue[n].col and pointCompare.row == neighborQueue[n].row:
                        checker = False

                if checker:
                    pointList.append(neighborQueue[n] )


        counterWhile = 0
        while counterWhile < len(pointList):
            pointToCheck = pointList[counterWhile]
            val = map[pointToCheck.col][pointToCheck.row].state
            if val == 0:
                finalPointList.append(pointToCheck)
                pointList.pop(counterWhile)
            counterWhile += 1

        sortedQueue = sorted(pointList, key=lambda point: self.mapUser[point.col][point.row].state, reverse = True)
        for j in range(0, len(sortedQueue)):
            finalPointList.append(sortedQueue[j])

        return pointList

    #returns count of how many neighbors there are
    def neighborCheck(self, map, currPt):
        count = 0
        # check left
        if(currPt.col-1 >= 0):
            count +=1
        #check right
        if (currPt.col+1 < self.dim):
            count +=1
        #check top
        if(currPt.row-1 >= 0):
            count +=1
        #check bottom
        if (currPt.row+1 < self.dim):
            count +=1
        #check lower left
        if(currPt.row-1 >= 0 and currPt.col-1 >= 0):
            count +=1
        #check upper left
        if (currPt.row+1 < self.dim and currPt.col-1 >= 0):
            count +=1
        #check Lower right
        if(currPt.row+1 < self.dim and currPt.col+1 < self.dim):
            count +=1
        #check Upper right
        if(currPt.row-1 >= 0 and currPt.col+1 < self.dim):
            count +=1

        return count

    #returns a random point that has not already been opened
    def randomCell(self, map):
        condition = False
        while condition is not True:
                col = random.randint(0, self.dim-1)
                row = random.randint(0, self.dim-1)
                if(map[col][row].state == 'X'):
                    return (col, row)

    #returns number of safe neighbors and a queue with those safe neighbors
    def numOfSafeNeighbors(self, map, currPt):
        count = 0
        safeQueue = []
        # check left
        if(currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row] is not None and map[currPt.col-1][currPt.row].state != 'X' and map[currPt.col-1][currPt.row].state != '-1' and map[currPt.col-1][currPt.row].state != 'M'):
                count+=1
                safeQueue.append(point(currPt.col-1, currPt.row))
        #check right
        if (currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row] is not None and map[currPt.col+1][currPt.row].state != 'X' and map[currPt.col+1][currPt.row].state != '-1' and map[currPt.col+1][currPt.row].state != 'M' ):
                count+=1
                safeQueue.append(point(currPt.col+1, currPt.row))
        #check top
        if(currPt.row-1 >= 0):
            if(map[currPt.col][currPt.row-1] is not None and map[currPt.col][currPt.row-1].state != 'X' and map[currPt.col][currPt.row-1].state != '-1' and map[currPt.col][currPt.row-1].state != 'M'):
                count+=1
                safeQueue.append(point(currPt.col, currPt.row-1))
        #check bottom
        if (currPt.row+1 < self.dim):
            if(map[currPt.col][currPt.row+1] is not None and map[currPt.col][currPt.row+1].state != 'X' and map[currPt.col][currPt.row+1].state != '-1' and map[currPt.col][currPt.row+1].state != 'M'):
                count+=1
                safeQueue.append(point(currPt.col, currPt.row+1))
        #check lower left
        if(currPt.row-1 >= 0 and currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row-1] is not None and map[currPt.col-1][currPt.row-1].state != 'X' and map[currPt.col-1][currPt.row-1].state != '-1'  and map[currPt.col-1][currPt.row-1].state != 'M'):
                count+=1
                safeQueue.append(point(currPt.col-1, currPt.row-1))
        #check upper left
        if (currPt.row+1 < self.dim and currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row+1] is not None and map[currPt.col-1][currPt.row+1].state != 'X' and  map[currPt.col-1][currPt.row+1].state != '-1' and  map[currPt.col-1][currPt.row+1].state != 'M'):
                count+=1
                safeQueue.append(point(currPt.col-1, currPt.row+1))
        #check Lower right
        if(currPt.row+1 < self.dim and currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row+1] is not None and map[currPt.col+1][currPt.row+1].state != 'X' and map[currPt.col+1][currPt.row+1].state != '-1' and map[currPt.col+1][currPt.row+1].state != 'M'):
                count+=1
                safeQueue.append(point(currPt.col+1, currPt.row+1))
        #check Upper right
        if(currPt.row-1 >= 0 and currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row-1] is not None and map[currPt.col+1][currPt.row-1].state != 'X' and map[currPt.col+1][currPt.row-1].state != '-1' and map[currPt.col+1][currPt.row-1].state != 'M'):
                count +=1
                safeQueue.append(point(currPt.col+1, currPt.row-1))
        return count, safeQueue

    #returns number of hidden neighbors
    def numOfHiddenNeighbors(self, map, currPt):
        count = 0
        # check left
        if(currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row] is not None and map[currPt.col-1][currPt.row].state == 'X'):
                count+=1
        #check right
        if (currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row] is not None and map[currPt.col+1][currPt.row].state == 'X' ):
                count+=1
        #check top
        if(currPt.row-1 >= 0):
            if(map[currPt.col][currPt.row-1] is not None and map[currPt.col][currPt.row-1].state == 'X'):
                count+=1
        #check bottom
        if (currPt.row+1 < self.dim):
            if(map[currPt.col][currPt.row+1] is not None and map[currPt.col][currPt.row+1].state == 'X' ):
                count+=1
        #check lower left
        if(currPt.row-1 >= 0 and currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row-1] is not None and map[currPt.col-1][currPt.row-1].state == 'X'):
                count+=1
        #check upper left
        if (currPt.row+1 < self.dim and currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row+1] is not None and map[currPt.col-1][currPt.row+1].state == 'X' ):
                count+=1
        #check Lower right
        if(currPt.row+1 < self.dim and currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row+1] is not None and map[currPt.col+1][currPt.row+1].state == 'X'):
                count+=1
        #check Upper right
        if(currPt.row-1 >= 0 and currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row-1] is not None and map[currPt.col+1][currPt.row-1].state == 'X'):
                count +=1
        return count

    #makes all neighbors as mines  and returns the number of mines marked, and a queue of all those cells
    def markAllNeighbors(self, map, currPt):
        count = 0
        marked = []
        # check left
        if(currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row] is not None and map[currPt.col-1][currPt.row].state == 'X'):
                self.mapUser[currPt.col-1][currPt.row].state = 'M'
                count +=1
                marked.append(point(currPt.col-1, currPt.row))
        #check right
        if (currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row] is not None and map[currPt.col+1][currPt.row].state == 'X' ):
                self.mapUser[currPt.col+1][currPt.row].state = 'M'
                count +=1
                marked.append(point(currPt.col+1, currPt.row))
        #check top
        if(currPt.row-1 >= 0):
            if(map[currPt.col][currPt.row-1] is not None and map[currPt.col][currPt.row-1].state == 'X'):
                self.mapUser[currPt.col][currPt.row-1].state = 'M'
                count +=1
                marked.append(point(currPt.col, currPt.row-1))
        #check bottom
        if (currPt.row+1 < self.dim):
            if(map[currPt.col][currPt.row+1] is not None and map[currPt.col][currPt.row+1].state == 'X' ):
                self.mapUser[currPt.col][currPt.row+1].state = 'M'
                count +=1
                marked.append(point(currPt.col, currPt.row+1))
        #check lower left
        if(currPt.row-1 >= 0 and currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row-1] is not None and map[currPt.col-1][currPt.row-1].state == 'X'):
                self.mapUser[currPt.col-1][currPt.row-1].state = 'M'
                count +=1
                marked.append(point(currPt.col-1, currPt.row-1))
        #check upper left
        if (currPt.row+1 < self.dim and currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row+1] is not None and map[currPt.col-1][currPt.row+1].state == 'X' ):
                self.mapUser[currPt.col-1][currPt.row+1].state = 'M'
                count +=1
                marked.append(point(currPt.col-1, currPt.row+1))
        #check Lower right
        if(currPt.row+1 < self.dim and currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row+1] is not None and map[currPt.col+1][currPt.row+1].state == 'X'):
                self.mapUser[currPt.col+1][currPt.row+1].state = 'M'
                count +=1
                marked.append(point(currPt.col+1, currPt.row+1))
        #check Upper right
        if(currPt.row-1 >= 0 and currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row-1] is not None and map[currPt.col+1][currPt.row-1].state == 'X'):
                self.mapUser[currPt.col+1][currPt.row-1].state = 'M'
                count +=1
                marked.append(point(currPt.col+1, currPt.row-1))
        return count, marked

    #makes all neighbors as safe and returns the number of safe neighbors opened
    def markAllSafeNeighbors(self, map, currPt):
        count = 0
        # check left
        if(currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row] is not None and map[currPt.col-1][currPt.row].state == 'X'):
                self.mapUser[currPt.col-1][currPt.row].state = self.mapInternal[currPt.col-1][currPt.row].state
                self.checkerQueue.append(point(currPt.col-1, currPt.row))
                count +=1
        #check right
        if (currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row] is not None and map[currPt.col+1][currPt.row].state == 'X' ):
                self.mapUser[currPt.col+1][currPt.row].state = self.mapInternal[currPt.col+1][currPt.row].state
                self.checkerQueue.append(point(currPt.col+1, currPt.row))
                count +=1
        #check top
        if(currPt.row-1 >= 0):
            if(map[currPt.col][currPt.row-1] is not None and map[currPt.col][currPt.row-1].state == 'X'):
                self.mapUser[currPt.col][currPt.row-1].state = self.mapInternal[currPt.col][currPt.row-1].state
                self.checkerQueue.append(point(currPt.col, currPt.row-1))
                count +=1
        #check bottom
        if (currPt.row+1 < self.dim):
            if(map[currPt.col][currPt.row+1] is not None and map[currPt.col][currPt.row+1].state == 'X' ):
                self.mapUser[currPt.col][currPt.row+1].state = self.mapInternal[currPt.col][currPt.row+1].state
                self.checkerQueue.append(point(currPt.col, currPt.row+1))
                count +=1
        #check lower left
        if(currPt.row-1 >= 0 and currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row-1] is not None and map[currPt.col-1][currPt.row-1].state == 'X'):
                self.mapUser[currPt.col-1][currPt.row-1].state = self.mapInternal[currPt.col-1][currPt.row-1].state
                self.checkerQueue.append(point(currPt.col-1, currPt.row-1))
                count +=1
        #check upper left
        if (currPt.row+1 < self.dim and currPt.col-1 >= 0):
            if(map[currPt.col-1][currPt.row+1] is not None and map[currPt.col-1][currPt.row+1].state == 'X' ):
                self.mapUser[currPt.col-1][currPt.row+1].state = self.mapInternal[currPt.col-1][currPt.row+1].state
                self.checkerQueue.append(point(currPt.col-1, currPt.row+1))
                count +=1
        #check Lower right
        if(currPt.row+1 < self.dim and currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row+1] is not None and map[currPt.col+1][currPt.row+1].state == 'X'):
                self.mapUser[currPt.col+1][currPt.row+1].state = self.mapInternal[currPt.col+1][currPt.row+1].state
                self.checkerQueue.append(point(currPt.col+1, currPt.row+1))
                count +=1
        #check Upper right
        if(currPt.row-1 >= 0 and currPt.col+1 < self.dim):
            if(map[currPt.col+1][currPt.row-1] is not None and map[currPt.col+1][currPt.row-1].state == 'X'):
                self.mapUser[currPt.col+1][currPt.row-1].state = self.mapInternal[currPt.col+1][currPt.row-1].state
                self.checkerQueue.append(point(currPt.col+1, currPt.row-1))
                count +=1
        return count


scoreAdvance = 0
scoreSimp = 0
#for i in range(0, 250):
#    map1 = minesweeper(25,100)
#    scoreAdvance += map1.agentAdvance()
#    print(i)

#for j in range(0, 250):
#    map2 = minesweeper(25,100)
#    scoreSimp += map2.agentSimp()
#    print(j)

#print(scoreAdvance/250)
#print(scoreSimp/250)

#map = minesweeper(4,5)
#map.agentAdvance()

#data_headerQ3 = ['mine density', 'score simp']
#with open('exportPerformance.csv', 'w') as file_writerQ3:
#    writerQ3 = csv.writer(file_writerQ3)
#    writerQ3.writerow(data_headerQ3)
#
#    for mineDensity in range(1,225):
#        scoreSimp = 0
#        for iteration in range(25):
#            map2 = minesweeper(15,mineDensity)
#            scoreSimp += map2.agentSimp()
#            print("iteration simp: ", iteration)
#            print("mineDensity simp: ", mineDensity)
#        dataQ3 = [mineDensity, scoreSimp/25]
#        writerQ3.writerow(dataQ3)


data_headerQ4 = ['mine density', 'score advance']
with open('exportPerformanceAdvance.csv', 'w') as file_writerQ4:
    writerQ4 = csv.writer(file_writerQ4)
    writerQ4.writerow(data_headerQ4)

    for mineDensity1 in range(1,225):
        scoreAdvance = 0
        for iteration1 in range(10):
            map1 = minesweeper(15,mineDensity1)
            scoreAdvance += map1.agentAdvance()
            print("iteration adv: ", iteration1)
            print("mineDensity adv: ", mineDensity1)
        dataQ4 = [mineDensity1, scoreAdvance/10]
        writerQ4.writerow(dataQ4)
