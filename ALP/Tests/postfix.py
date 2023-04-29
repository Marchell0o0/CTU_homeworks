from sys import argv

with open(argv[1], "r") as f:
    inp = [line.strip() for line in f]

postfix = str(argv[2])

# print(inp)
# print(postfix)

count = 0
smallest = []


def find_shortest(ls):
    shortest = ls[0]
    for i in range(len(ls)):
        if len(ls[i]) < len(shortest):
            shortest = ls[i]
    return shortest


for word in inp:
    same = 0
    if len(postfix) < len(word):
        for i in range(1, len(postfix) + 1):
            if word[-i] == postfix[-i]:
                same += 1
            if same == len(postfix):
                count += 1
                smallest.append(word)

print(count)
if count != 0:
    print(find_shortest(smallest))
else:
    print("None")
