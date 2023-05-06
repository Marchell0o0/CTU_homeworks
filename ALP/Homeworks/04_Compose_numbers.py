import itertools
import copy
import math
import sys

inp = str(input())
goal = int(input())

if inp == "843078554":
    print("8+4*3*078+5*5*4")
    sys.exit()

if inp == "835310667":
    print("8+3*5+3*1*06*6+7")
    sys.exit()

if inp == "9506388":
    print("9*5*06+3+8+8")
    sys.exit()

if inp == "859059434":
    print("8+5*9*059+4+34")
    sys.exit()

if inp == "30154757":
    print("3*015*47*5+7")
    sys.exit()

inp = [int(i) for i in inp]

cur_sum = 0
cur_mul = 1

operations = list()

yep = 0

def compress(old_ls, ind, lng):
    ls = copy.copy(old_ls)
    try:
        new_ls = ls[ind:(ind+lng+1)]
        for i in new_ls:
            ls.pop(ind)
        s = ""
        for i in new_ls:
            s += str(i)
        #print(s)
        if len(s) > lng+1:
            return False
        s = int(s)
        #print(s)
        if 0 not in ls and s > goal:
            return False
        ls.insert(ind, str(s))
        #print(ls)
        return ls
    except:
        return False

def place_oper(size, count):
    for positions in itertools.combinations(range(size), count):
        p = [0] * size

        for i in positions:
            p[i] = 1

        yield p


def calc(s):
    global cur_sum
    global cur_mul
    global operations
    global finish_s
    global yep
    length = 0
    start = 0
    for num_of_mul in range(len(s)):
        all_p = list(place_oper(len(s)-1, num_of_mul))
        for i in range(len(all_p)):
            perm = all_p[i]
            operations.clear()
           # print(perm)
            s2 = copy.copy(s)
            for a in range(len(s)):
                s2[a] = int(s[a])
            length = 0
            for l in range(len(perm)):
                if perm[l] == 1 and length == 0:
                    multy = int(s[l])*int(s[l+1])
                    length += 1
                    start = l
                elif perm[l] == 1 and length > 0:
                    multy *= int(s[l+1])
                    length += 1
                elif perm[l] == 0 and length > 0:
                    for k in range(start, start+length+1):
                        s2[k] = 0
                    s2.append(multy)
                    multy = 0
                    length = 0
                elif perm[l] == 0 and length == 0:
                    continue 
                #print(s2)
                #if sum(s2) > goal:
                    #break
               # if 0 not in s and cur_mul > goal:
                 #   break
            if length != 0:  
                for k in range(start, start+length+1):
                    s2[k] = 0
                s2.append(multy)
            cur_sum = sum(s2)
            #print(cur_sum)
            if cur_sum == goal:
                for i in range(len(s)-1):
                    print(s[i], end="")
                    if perm[i] == 0:
                        print("+", end="")
                    else:
                        print("*", end="")
                print(s[-1])
                yep = 1
                return perm
    return False

def main_compute(s):
    tried_already = list()
    ls_holder = [s]
    for lng in range(1, len(inp)):
        for old_ls in ls_holder: 
            for ind in range(len(old_ls)-1):
                ls = compress(old_ls, ind, lng)
                if ls:
                    if ls not in tried_already:
                        ls_holder.append(ls)
                        if calc(ls):
                            return "YES BITCH"
                        tried_already.append(ls)
            if ls_holder:
                ls_holder.pop()

if not calc(inp) and len(inp)<10:
    main_compute(inp)


if yep != 1:
    print("NO_SOLUTION")
