from sys import argv

n = int(argv[1])
e = int(argv[2])
inp = str(input())
blocks = []
res = []


for i in range(0, len(inp), 4):
    blocks.append(inp[i : i + 4])


for item in blocks:
    while len(item) != 4:
        item = item + chr(0)
    x = ((ord(item[0]) * 256 + ord(item[1])) * 256 + ord(item[2])) * 256 + ord(item[3])
    code = pow(x, e, n)
    res.append(code)

[print(item, end=" ") for item in res]
