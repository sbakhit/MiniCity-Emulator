import random
from turtle import *

def pseudorandom(M,N):
    l=[(x+1,y+1) for x in range(N) for y in range(M)]
    random.shuffle(l)
    for i in range(M*N-1):
            for j in range (i+1,M*N): # find a compatible ...
                if l[i][0] != l[j][0]:
                    l[i+1],l[j] = l[j],l[i+1]
                    break  
            else:   # or insert otherwise.
                while True:
                    l[i],l[i-1] = l[i-1],l[i]
                    i-=1
                    if l[i][0] != l[i-1][0]: break  
    return l

# coordinates = pseudorandom(1024, 1024)
# print(len(coordinates))

def driving(coordinates):
    
    # set the initial point, our coordinates are a list of tuples
    memory_counter = 0

    while True:
        # now we drive the damn thing
        penup()
        starting_points = coordinates[memory_counter]
        setpos(starting_points[0], starting_points[1])
        print("Turtle's position = ",pos())        
        memory_counter += 1
        if(memory_counter >= len(coordinates)):
            break
    done()

coordinates = [(500, 450),(501, 450),(501, 451),(501, 452),(502, 452),(502, 453),(503, 453),(503, 454),(504, 454),(504, 455)]

coordinates = [(100, 150),(101, 150),(101, 151),(101, 152),(102, 152),(102, 153),(103, 153),(103, 154),(104, 154),(104, 155)]

setup(1024, 1024)
driving(coordinates)

