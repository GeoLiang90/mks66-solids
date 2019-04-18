from display import *
from matrix import *
from gmath import *
import random

#i is index
def scanline_convert(polygons, i, screen, zbuffer ):
    r = int(random.random() * 256)
    g = int(random.random() * 256)
    b = int(random.random() * 256)
    color = [r,g,b]
    #Save the 3 points that im currently working with
    mypoints = [polygons[i],polygons[i + 1],polygons[i + 2]]
    #In order for a top middle bottom, I have to sort points
    #B must always have the lowest Y

    lowest_index = 0

    for p in range(len(mypoints)):
        if mypoints[p][1] < mypoints[lowest_index][1]:
            lowest_index = p

    B = mypoints[lowest_index]
    mypoints.pop(lowest_index)
    #print(B)
    lowest_index = 0

    for p in range(len(mypoints)):
        if mypoints[p][1] < mypoints[lowest_index][1]:
            lowest_index = p

    M = mypoints[lowest_index]
    mypoints.pop(lowest_index)
    #print(M)

    T = mypoints[0]
    #print(T)
    if (T[1] != B[1]):
        startX0 = B[0]
        startX1 = B[0]
        startZ0 = B[2]
        startZ1 = B[2]
        startY = B[1]
        changex0 = 0
        changex1 = 0
        changez0y = 0
        changez1y = 0
        changezx = 0
        #Under Midpoint case
        if M[1] != B[1]:
            changex0 = (M[0] - B[0]) / (M[1] - B[1])

        if T[1] != B[1]:
            changex1 = (T[0] - B[0]) / (T[1] - B[1])


        if (M[1] != B[1]):
            changez0y = (M[2] - B[2]) / (M[1] - B[1])

        if (T[1] != B[1]):
            changez1y = (T[2] - B[2]) / (T[1] - B[1])

        if (changez0y != changez1y):
            changezx = (changez1y - changez0y) / (changex1 - changex0)
        #Under midline
        while startY < M[1]:
            draw_line(int(startX0),int(startY),int(startZ0),int(startX1),int(startY),int(startZ1),screen,zbuffer,color)
            startX0 += changex0
            startX1 += changex1
            startZ0 += changez0y
            startZ1 += changez1y
            startY += 1
        #At some point ill hit the midline so set x0 my changing point to the x of middle
        startX0 = M[0]
        if (T[1] != M[1]):
            changex0 = (T[0] - M[0]) / (T[1] - M[1])
        else:
            changex0 = 0
        while startY < T[1]:
            draw_line(int(startX0),int(startY),int(startZ0),int(startX1),int(startY),int(startZ1),screen,zbuffer,color)
            startX0 += changex0
            startX1 += changex1
            startZ0 += changez0y
            startZ1 += changez1y
            startY += 1

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )



def draw_line( x0, y0, z0, x1, y1, z1, screen, zbuffer, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False

    if ( abs(x1-x0) >= abs(y1 - y0) ): #octants 1/8
        wide = True
        loop_start = x
        loop_end = x1
        dx_east = dx_northeast = 1
        dy_east = 0
        d_east = A
        if ( A > 0 ): #octant 1
            d = A + B/2
            dy_northeast = 1
            d_northeast = A + B
        else: #octant 8
            d = A - B/2
            dy_northeast = -1
            d_northeast = A - B

    else: #octants 2/7
        tall = True
        dx_east = 0
        dx_northeast = 1
        if ( A > 0 ): #octant 2
            d = A/2 + B
            dy_east = dy_northeast = 1
            d_northeast = A + B
            d_east = B
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A/2 - B
            dy_east = dy_northeast = -1
            d_northeast = A - B
            d_east = -1 * B
            loop_start = y1
            loop_end = y

    while ( loop_start < loop_end ):
        plot( screen, zbuffer, color, x, y, 0 )
        if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
             (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):

            x+= dx_northeast
            y+= dy_northeast
            d+= d_northeast
        else:
            x+= dx_east
            y+= dy_east
            d+= d_east
        loop_start+= 1
    plot( screen, zbuffer, color, x, y, 0 )
