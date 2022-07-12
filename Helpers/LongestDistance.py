# Gets the longest distance of a set of points
import math

def getdiff(point1, point2):
    return (point1[0]-point2[0], point1[1]-point2[1], point1[2]-point2[2])

def getdist(point1):
    return math.sqrt(point1[0]**2 + point1[1]**2 + point1[2]**2)

def getlongestdist(origin, points):
    longestdist = 0
    for point1 in points:
        currdist = getdist(getdiff(origin, point1))
        if currdist > longestdist:
            longestdist = currdist

    return longestdist
