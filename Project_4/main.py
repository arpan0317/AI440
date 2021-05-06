import cv2
import numpy as np
import random
import math
import statistics
from statistics import mode

ogImage = cv2.imread("bigImage.jpg")
cv2.imshow("og", ogImage)
cv2.waitKey(0)
ogImage = cv2.cvtColor(ogImage, cv2.COLOR_BGR2RGB)

ogHeight, ogWidth, ogDepth = ogImage.shape[0:3]
bwImage = ogImage.copy()

for i in range(0, ogHeight):
    for j in range(0, ogWidth):
        grayVal = 0.21 * ogImage[i, j, 0] + 0.72 * ogImage[i, j, 1] + 0.07 * ogImage[i, j, 2]
        bwImage[i, j, :] = grayVal

cluster = []
for k in range(0, 5):
    x = random.randrange(0, 256)
    y = random.randrange(0, 256)
    z = random.randrange(0, 256)
    cluster.append((x,y,z))

for i in range(0, 50):
    print(i)
    cluster1 = []
    cluster2 = []
    cluster3 = []
    cluster4 = []
    cluster5 = []

    allClusters = [cluster1, cluster2, cluster3, cluster4, cluster5]

    for i in range(0, ogHeight):
        for j in range(0, ogWidth):

            dist = []
            for k in range(0, 5):
                dist.append(math.sqrt(2 * (cluster[k][0] - ogImage[i, j, 0])**2 + 4 * (cluster[k][1] - ogImage[i, j, 1])**2 + 3*(cluster[k][2] - ogImage[i,j,2])**2))
            distance = min(dist)
            index = dist.index(distance)
            if(index == 0):
                allClusters[0].append((i, j))
            elif(index == 1):
                allClusters[1].append((i, j))
            elif(index == 2):
                allClusters[2].append((i, j))
            elif(index == 3):
                allClusters[3].append((i, j))
            elif(index == 4):
                allClusters[4].append((i, j))


    iSum = 0
    jSum = 0
    for i in range(0, 5):
        rVal = 0
        gVal = 0
        bVal = 0
        if(len(allClusters[i]) != 0):
            for j in range(0, len(allClusters[i])):
                iPoint = allClusters[i][j][0]
                jPoint = allClusters[i][j][1]
                rVal += ogImage[iPoint, jPoint, 0]
                gVal += ogImage[iPoint, jPoint, 1]
                bVal += ogImage[iPoint, jPoint, 2]
            cluster[i] = (rVal/len(allClusters[i]), gVal/len(allClusters[i]), bVal/len(allClusters[i]))
        else:
            x = random.randrange(0, 256)
            y = random.randrange(0, 256)
            z = random.randrange(0, 256)
            cluster[i] = (x,y,z)

for i in range(0, 5):
    print(cluster[i])

kmeanImage = ogImage.copy()
for i in range(0, 5):
    for j in range(len(allClusters[i])):
        iPoint = allClusters[i][j][0]
        jPoint = allClusters[i][j][1]
        rVal = cluster[i][0]
        gVal = cluster[i][1]
        bVal = cluster[i][2]
        kmeanImage[iPoint, jPoint, 0] = rVal
        kmeanImage[iPoint, jPoint, 1] = gVal
        kmeanImage[iPoint, jPoint, 2] = bVal

kmeanImageFlipped = cv2.cvtColor(kmeanImage, cv2.COLOR_RGB2BGR)
cv2.imshow("test", kmeanImageFlipped)
newImage = kmeanImage.copy()
cv2.waitKey(0)
counter = 0
arrDiff = []
for i in range(1, ogHeight-1):
    for j in range(math.ceil(ogWidth/2), ogWidth-1):
        arrDiff = []
        sortedArr = []
        arrRight = [(i-1, j-1), (i - 1, j), (i-1, j+1), (i, j-1), (i, j), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]
        #for k in range(1, ogHeight-1):
        #    for l in range(1, math.floor(ogWidth/2)):
        for n in range(0,1000):
                k = random.randrange(1, ogHeight-1)
                l = random.randrange(1, math.floor(ogWidth/2))
                colorDiff = abs(int(bwImage[arrRight[0][0], arrRight[0][1], 0]) - int(bwImage[k-1, l-1, 0])) + abs(int(bwImage[arrRight[1][0], arrRight[1][1], 0]) - int(bwImage[k-1, l, 0])) + abs(int(bwImage[arrRight[2][0], arrRight[2][1], 0]) - int(bwImage[k-1, l+1, 0])) + abs(int(bwImage[arrRight[3][0], arrRight[3][1], 0]) - int(bwImage[k, l-1, 0])) + abs(int(bwImage[arrRight[4][0], arrRight[4][1], 0]) - int(bwImage[k, l, 0])) + abs(int(bwImage[arrRight[5][0], arrRight[5][1], 0]) - int(bwImage[k, l+1, 0])) + abs(int(bwImage[arrRight[6][0], arrRight[6][1], 0]) - int(bwImage[k+1, l-1, 0])) + abs(int(bwImage[arrRight[7][0], arrRight[7][1], 0]) - int(bwImage[k+1, l, 0]))  + abs(int(bwImage[arrRight[8][0], arrRight[8][1], 0]) - int(bwImage[k+1, l+1, 0]))
                arrDiff.append((colorDiff, k, l))
                counter += 1
                print(counter)
        sortedArr = sorted(arrDiff, key=lambda diff: diff[0])
        colorArray = []
        for m in range(0, 6):
            iVal = sortedArr[m][1]
            jVal = sortedArr[m][2]
            colorArray.append((kmeanImage[iVal, jVal, 0], kmeanImage[iVal, jVal, 1], kmeanImage[iVal, jVal, 2]))
        mostCommonColor = mode(colorArray)
        newImage[i,j,0] = mostCommonColor[0]
        newImage[i,j,1] = mostCommonColor[1]
        newImage[i,j,2] = mostCommonColor[2]
newImage = cv2.cvtColor(newImage, cv2.COLOR_RGB2BGR)
cv2.imshow("final", newImage)
cv2.waitKey(0)
