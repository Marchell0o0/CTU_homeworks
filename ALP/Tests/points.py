from math import sqrt

inp = list(map(float, input().split()))

distance = {}
xs = []
ys = []
for i in range(0, len(inp), 2):
    distance[i // 2] = sqrt(inp[i] ** 2 + inp[i + 1] ** 2)
    xs.append(inp[i])
    ys.append(inp[i + 1])
distanceSorted = dict(sorted(distance.items(), key=lambda x: x[1]))


circleDot = list(distanceSorted.keys())[(len(distance) // 2) - 1]


middle = [sum(xs, 0) / len(xs), sum(ys, 0) / len(ys)]
cur_min = sqrt(((inp[0] - middle[0]) ** 2) + ((inp[1] - middle[1]) ** 2))
ind = 0
for i in range(2, len(inp), 2):
    temp = sqrt(((inp[i] - middle[0]) ** 2) + ((inp[i + 1] - middle[1]) ** 2))
    if cur_min > temp:
        cur_min = temp
        ind = i // 2

print(ind, circleDot)
