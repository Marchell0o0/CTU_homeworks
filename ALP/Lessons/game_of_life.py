import copy
import time

def p(m):
    for r in range(len(m)):
        for c in range(len(m[0])):
            if m[r][c] == 1:
                print("X", end = " ")
            else:
                print(".", end = " ")
        print()

def step(m):
    new = copy.deepcopy(m)
    for r in range(len(m)):
        for c in range(len(m[0])):
            living = 0
            for ro in [-1,0,1]:
                for co in [-1,0,1]:
                    if m[(r+ro)%len(m)][(c+co)%len(m[0])] == 1:
                        living += 1
            if living == 3:
                new[r][c] = 1
            elif m[r][c] == 1 and living == 2:
                new[r][c] = 1   
            else:
                new[r][c] = 0
    p(new)

a = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   ]

for i in range(40):
    step(a)
    print()
    time.sleep(0.3)
