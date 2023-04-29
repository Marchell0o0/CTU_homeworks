
x = list(map(int, input().split()))
end = int(input())


class state:
    def __init__(self, buckets, current_volume, action, parent=None) -> None:
        self.buckets = buckets
        self.current_volume = current_volume
        self.parent = parent
        self.action = action

    def expand(self):
        res = []

        # Fill up
        for i in range(3):
            temp_volume = self.current_volume[:]
            temp_volume[i] = self.buckets[i]
            res.append(state(self.buckets, temp_volume, 'N' + f'{i}', self))

        # Empty
        for i in range(3):
            temp_volume = self.current_volume[:]
            if temp_volume[i] == 0:
                continue
            else:
                temp_volume[i] = 0
                res.append(
                    state(self.buckets, temp_volume, 'V' + f'{i}', self))

        # From to
        for i in range(3):
            for j in range(3):
                if i == j or self.current_volume[i] == 0 or self.current_volume[j] == self.buckets[j]:
                    continue
                else:
                    possible_move = self.buckets[j] - self.current_volume[j]
                    temp_volume = self.current_volume[:]
                    if possible_move < self.current_volume[i]:
                        temp_volume[j] = self.buckets[j]
                        temp_volume[i] -= possible_move

                        res.append(state(self.buckets, temp_volume,
                                   f'{i}' + 'P' + f'{j}', self))
                    else:        # possible_move >= self.current_volume[i]:
                        temp_volume[i] = 0
                        temp_volume[j] += self.current_volume[i]
                        res.append(state(self.buckets, temp_volume,
                                   f'{i}' + 'P' + f'{j}', self))

        return res


State0 = state(x, [0]*len(x), '', None)
result = []
queue = [State0]
tried_already = set()
while queue:
    current = queue.pop(0)
    tried_already.add(str(current.current_volume))
    next_states = current.expand()
    for next_state in next_states:
        if str(next_state.current_volume) not in tried_already:
            queue.append(next_state)
        if end in next_state.current_volume:
            temp = next_state
            while temp.parent != None:
                result.append(temp.action)
                temp = temp.parent
            for i in range(len(result)-1, -1, -1):
                print(result[i])
            quit()
