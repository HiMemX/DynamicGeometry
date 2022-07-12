
def getavrg(points):
    avrgx = 0
    avrgy = 0
    avrgz = 0
    for point in points:
        avrgx += point[0]/len(points)
        avrgy += point[1]/len(points)
        avrgz += point[2]/len(points)
    return [avrgx, avrgy, avrgz]
    