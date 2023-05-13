from sys import argv
import numpy as np


with open(argv[1], "r", encoding="utf-8") as f:
    X = [list(map(int, line.split())) for line in f]

X = np.array(X)
X[X >= 0] = 0
X[X < 0] = 1


def get_max_area_hist(x):
    max_area = 0
    cur_area = 0
    max_h = 0
    max_l = 0
    stack = [0]
    x = [-1] + x + [-1]
    for c in range(1, len(x)):
        while x[stack[-1]] > x[c]:
            j = stack.pop()
            l, r = c, stack[-1]
            cur_area = x[j] * (l - r - 1)
            if cur_area > max_area:
                max_area = cur_area
                max_h = x[j]
                max_l = r
        stack.append(c)
    return max_area, max_h, max_l


cur_area = 0
max_area = 0
last_index = 0
height = 0
left = 0


m = len(X[0])
n = len(X)
hist = [0] * m
for i in range(n):
    for j in range(m):
        if X[i, j] == 1:
            hist[j] += 1
        else:
            hist[j] = 0
    current_area, temp_height, temp_left = get_max_area_hist(hist)
    if current_area > max_area:
        last_index = i
        max_area = current_area
        left = temp_left
        height = temp_height
width = max_area // height
print(last_index - height + 1, left)
print(last_index, left + width - 1)
