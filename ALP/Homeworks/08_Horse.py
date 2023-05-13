from sys import argv

global board

with open(argv[1], "r", encoding="utf-8") as f:
    board = [list(map(int, line.split())) for line in f]

# print(*board, sep="\n")


"""
Directions:
1 is one to the right, two to the top 
up to 8 in a clockwise direction

"""

start = []
end = []

for r in range(len(board)):
    for c in range(len(board[0])):
        if board[r][c] == 2:
            start = [r, c]
        if board[r][c] == 4:
            end = [r, c]


class State:
    def __init__(self, state, prev=None):
        self.state = state[:]
        self.prev = prev
        self.direction = ""

    def inside(self, r, c, where):
        return 0 <= r < len(where) and 0 <= c < len(where[0])

    def move(self, r, c, dir):
        global board
        if dir == 1 and self.inside(r - 2, c + 1, board) and board[r - 2][c + 1] != 1:
            return [r - 2, c + 1]
        if dir == 2 and self.inside(r - 1, c + 2, board) and board[r - 1][c + 2] != 1:
            return [r - 1, c + 2]
        if dir == 3 and self.inside(r + 1, c + 2, board) and board[r + 1][c + 2] != 1:
            return [r + 1, c + 2]
        if dir == 4 and self.inside(r + 2, c + 1, board) and board[r + 2][c + 1] != 1:
            return [r + 2, c + 1]
        if dir == 5 and self.inside(r + 2, c - 1, board) and board[r + 2][c - 1] != 1:
            return [r + 2, c - 1]
        if dir == 6 and self.inside(r + 1, c - 2, board) and board[r + 1][c - 2] != 1:
            return [r + 1, c - 2]
        if dir == 7 and self.inside(r - 1, c - 2, board) and board[r - 1][c - 2] != 1:
            return [r - 1, c - 2]
        if dir == 8 and self.inside(r - 2, c - 1, board) and board[r - 2][c - 1] != 1:
            return [r - 2, c - 1]
        return False

    def expand(self):
        res = []
        for i in range(1, 9):
            new = State(self.state, self)
            if self.move(self.state[0], self.state[1], i):
                new.state = self.move(self.state[0], self.state[1], i)
            new.direction = i
            res.append(new)
        return res


startState = State(start)
queue = [startState]
visited = {}
result = []
while len(queue) > 0:
    actual = queue.pop(0)
    visited[str(actual.state)] = 1
    if actual.state == end:
        tmp = actual
        while tmp != None:
            if tmp.state == start:
                break
            result.append(tmp.state)
            tmp = tmp.prev
        break
    newStates = actual.expand()
    for state in newStates:
        if not str(state.state) in visited:
            queue.append(state)

if result:
    for i in range(len(result) - 1, -1, -1):
        print(" ".join(str(item) for item in result[i]), end=" ")
else:
    print("NEEXISTUJE")
