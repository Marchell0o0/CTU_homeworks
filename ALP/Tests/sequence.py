from sys import argv


with open(argv[1], "r", encoding="utf-8") as f:
    inp = [list(map(int, line.split())) for line in f]

max_length = 0
for r in range(len(inp)):
    current_length = 0
    for c in range(len(inp[0])):
        if inp[r][c] % 2 == 0 and inp[r][c] >= 0:
            if current_length == 0:
                temp_answer = ['r', r, c, 0]
                current_length += 1
            else:
                current_length += 1

        else:
            if current_length > max_length:
                max_length = current_length
                answer = temp_answer
                answer[3] = max_length
            current_length = 0

        if current_length > max_length:
            max_length = current_length
            answer = temp_answer
            answer[3] = max_length

for c in range(len(inp[0])):
    current_length = 0
    for r in range(len(inp)):
        if inp[r][c] % 2 == 0 and inp[r][c] >= 0:
            if current_length == 0:
                temp_answer = ['s', r, c, 0]
                current_length += 1
            else:
                current_length += 1

        else:
            if current_length > max_length:
                max_length = current_length
                answer = temp_answer
                answer[3] = max_length
            current_length = 0

        if current_length > max_length:
            max_length = current_length
            answer = temp_answer
            answer[3] = max_length

if max_length > 0:
    for item in answer:
        print(str(item), end=' ')
else:
    print("NEEXISTUJE")
