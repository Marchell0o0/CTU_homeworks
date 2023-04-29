VOLUME = [5, 4, 3]


class State:
    def __init__(self, v, prev=None):
        self.v = v[:]
        self.prev = prev
        self.action = ""

    def expand(self):
        # returns list of States
        res = []
        for i in range(len(self.v)):
            if self.v[i] == VOLUME[i]:
                continue
            new = State(self.v, self)
            new.v[i] = VOLUME[i]
            new.action = "N" + str(i)
            res.append(new)

        for i in range(len(self.v)):
            if self.v[i] == 0:
                continue
            new = State(self.v, self)
            new.v[i] = 0
            new.action = "V" + str(i)
            res.append(new)

        for i in range(len(self.v)):
            for j in range(len(self.v)):
                if i == j or self.v[i] == 0 or self.v[j] == VOLUME[j]:
                    continue
                new = State(self.v, self)
                new.action = str(i) + "P" + str(j)
                z = VOLUME[j] - self.v[j]
                if self.v[i] >= z:
                    new.v[i] -= z
                    new.v[j] += z
                else:
                    new.v[j] += new.v[i]
                    new.v[i] = 0
                res.append(new)
        return res


start = State([0, 0, 0])

queue = [start]
isKnown = {}
while len(queue) > 0:
    actual = queue.pop(0)
    isKnown[str(actual.v)] = 1
    print("actual", actual)
    print("actual v", actual.v)
    if actual.v == [0, 0, 1]:
        tmp = actual
        while tmp != None:
            print(tmp.v, tmp.action)
            tmp = tmp.prev
        break
    newStates = actual.expand()
    for state in newStates:
        if not str(state.v) in isKnown:
            queue.append(state)
