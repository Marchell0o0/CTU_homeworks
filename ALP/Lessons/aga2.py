p1 = [0,3,0,1]
p2 = [1,0,1]

def polySum(p1, p2):
    res = [0]*max( len(p1), len(p2))
    if len(p1) < len(p2):
        p1, p2 = p2, p1
    while len(p2) < len(p1):
        p2.append(0)
    for i in range(len(res)):
        res[i] = p1[i]+p2[i]
    return res


def find(where, what):
    for start in range (len(where)-len(what)+1):
        i = 0
        while i < len(what) and where[start+i] == what[i]:
            i += 1
        if i == len(what):
            return start
    return -1


def mv(m, v):
    res = [0] * len(v)
    for r in range(len(m)):
        for i in range(len(v)):
            res[r] += m[r][i] * v[i]      
    return res

print(mv([[1,1],[1,1]],[1,1]))

f = open("m.txt", "r")
