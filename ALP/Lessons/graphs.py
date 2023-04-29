from sys import argv

E = {}

with open(argv[1], "r") as f:
    for line in f:
        v = list(map(int, line.strip().split()))
        if not v[0] in E:
            E[v[0]] = []
        E[v[0]].append(v[1])
print(E)


class State:
    def __init__(self, v):
        self.v = v
        self.action = ""
        self.prev = None

    def expand(self):
        res = []
        for v in E[self.v]:
            newState = State(v)
            newState.prev = self
            newState.action = str(self.v) + "->" + str(v)
            res.append(newState)
        return res


start = State(0)
queue = [start]
isKnown = {}

while len(queue) > 0:
    actual = queue.pop(0)
    isKnown[str(actual.v)] = 1
    print("actual", actual)
    print("actual v", actual.v)
    if actual.v == 4:
        print("goal found")
        tmp = actual
        while tmp != None:
            print(tmp.v, tmp.action)
            tmp = tmp.prev
        break
    newStates = actual.expand()
    for state in newStates:
        if not str(state.v) in isKnown:
            queue.append(state)

print("end of BFS")
