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

def bfsWithFirePlots(self, x, y, finalX, finalY, mazeIn, q):

    copyBFS = copy.deepcopy(mazeIn)
    print("new maze original")
    self.printMaze(copyBFS)
    if mazeIn[x][y].state!='0':
        return False, False
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
            if checker[1]<current.distance:
                print("checking: ", checker, current.distance)
                return False, True
            else:

                #return current.distance
                return True, True
        if ([currPt.x, currPt.y]) not in visited:
            if mazeIn[finalX][finalY].state == '1':
                return False, False
            if mazeIn[currPt.x][currPt.y].state == '1':
                if len(fringe) == 0:
                    return False, False
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
    return False, False


    def plotting(self, mazeQ3):
        data_headerQ3 = ['bfs1 steps', 'bfs2 steps', 'q']
        with open('exportQ4.csv', 'w') as file_writerQ3:
            writerQ3 = csv.writer(file_writerQ3)
            writerQ3.writerow(data_headerQ3)

            for x in range(0,100):
                for y in range(0,100):
                    mazeQ3 = test(5,0.3)
                    for i in range(0, mazeQ3.dim):
                        for j in range(0, mazeQ3.dim):
                            if mazeQ3.maze[i][j].state == '1':
                                xLocFire = i
                                yLocFire = j
                    initialCheck = mazeQ3.bfsForFire(0,0, xLocFire, yLocFire, mazeQ3.maze)
                    if(initialCheck != False):
                        check = mazeQ3.bfs(0,0,4,4,mazeQ3.maze)
                        if(check[0] != False):
                            #check2 = mazeQ3.bfsWithFire1(0,0,9,9,mazeQ3.maze, y/100)
                            #check3 = mazeQ3.bfsWithFire2(0,0,9,9,mazeQ3.maze, y/100)
                            #print("new maze ")
                            check1 = mazeQ3.bfsWithFirePlots(0,0,4,4,mazeQ3.maze, y/100)
                            if check1[0] == False and check1[1] == True:
                                return
                            dataQ3 = [check1[0], check1[1], y/100]
                            writerQ3.writerow(dataQ3)
                            print()
maze = test(10,0.3)
maze.plotting(maze)
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
#Totaltime = 0
#size=10
#while Totaltime<10:
#    maze = test(size, 0.3)
#    startTime = time.time()
#    check1 = maze.aStar(0,0,size-1,size-1,maze.maze)
#    endTime = time.time()
#    if (check1 == True):
#        Totaltime = endTime-startTime
#    #print("astar: ", check1)
#    size+=5
#Totaltime1 = 0
#size1=10
#while Totaltime1<10:
#    maze = test(size1, 0.3)
#    startTime = time.time()
#    check2 = maze.dfs(0,0,size1-1,size1-1,maze.maze)
#    endTime = time.time()
#    if (check2 == True):
#        Totaltime1 = endTime-startTime
#    #print("dfs: ", check2)
#    size1+=5
#Totaltime2 = 0
#size2=10
#while Totaltime2<10:
#    maze = test(size2, 0.3)
#    startTime = time.time()
#    check3 = maze.bfs(0,0,size2-1,size2-1,maze.maze)
#    endTime = time.time()
#    if (check3 == True):
#        Totaltime2 = endTime-startTime
    #print("bfs: ", check3)
#    size2+=5

#print("Largest aStar dimensions: ", size-10) 250, 255
#print("Largest dfs dimensions: ", size1-10)  310, 300
#print("Largest bfs dimensions: ", size2-10)  240, 250
