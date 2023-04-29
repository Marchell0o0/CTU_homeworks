def inside(m, r, c):
    return 0 <= r < len(m) and 0 <= c < len(m[0])


def floodfill(m, r1, c1):
    stack = []
    stack.append([r1, c1])
    neighbors = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    while len(stack) > 0:
        actual = stack.pop()
        row, col = actual
        m[row][col] = "*"
        for n in neighbors:
            rowOffset, colOffset = n
            rown = row + rowOffset
            coln = col + colOffset
            if inside(m, rown, coln) and m[rown][coln] == 0:
                stack.append([rown, coln])
    return m


m = [
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
]

print(*floodfill(m, 0, 0), sep="\n")
