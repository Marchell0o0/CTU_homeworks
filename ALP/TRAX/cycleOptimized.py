from sys import argv

# with open(argv[1], "r", encoding="utf-8") as f:
#     inp = [list(map(str, line.split())) for line in f]


def inside(r, c, board):
    return 0 <= r < len(board) and 0 <= c < len(board[0])

# inp = [
#     ['ddll', 'lldd', 'dldl'],
#     ['dlld', 'lddl', 'dldl'],
#     ['none', 'none', 'none']
#     ]

# inp = [
#     ['ddll', 'ldld', 'lddl'],
#     ['dlld', 'ldld', 'lldd'],
#     ['ldld', 'ldld', 'ldld']
#     ]

inp = [
    ['dlld', 'lldd', 'none'],
    ['lddl', 'ddll', 'none'],
    ['none', 'none', 'none']
    ]

def main(board, tried_already, res) -> None:
    for color in ["light", "dark"]:
        res = []
        tried_already = set()
        for r in range(len(board)):
            for c in range(len(board[0])):
                if str([r, c]) not in tried_already:
                    cycles_lines(r, c, board, [r, c], 0, color, "nn", "cycles", lookup_closing_lines, tried_already, res)
                    tried_already.add(str([r, c]))
        print("cycles", color, res)
    for color in ["light", "dark"]:
        res = []
        for direction in ["td", "lr"]:
            tried_already = set()
            if direction == "lr":
                for r in range(len(board)):
                    if str([r, 0]) not in tried_already and  board[r][0][0] == color[0]:
                        cycles_lines(r, 0, board, 0, 0, color, direction, "lines", lookup_closing_lines, tried_already, res)
                        tried_already.add(str([r, 0]))
            else:
                for c in range(len(board[0])):
                    if str([0, c]) not in tried_already and board[0][c][1] == color[0]:
                        cycles_lines(0, c, board, 0, 0, color, direction, "lines", lookup_closing_lines, tried_already, res)
                        tried_already.add(str([0, c]))
        print("lines", color, res)



directions = [
    (0, 1, 2, 0),
    (1, 0, 3, 1),
    (0, -1, 0, 2),
    (-1, 0, 1, 3),
    ]




def stats(board):
        result = {"light":0, "dark":0}
        cycles = {"light":[], "dark":[]}
        lines =  {"light":[], "dark":[]}
        # print("checking for cycles")
        for color in ["light", "dark"]:
            tried_already = set()
            for r in range(len(board)):
                for c in range(len(board[0])):
                    if (r, c) not in tried_already:
                        start = (r, c)
                        length = 1
                        queue = [(r,c)]
                        while queue:  
                            r_temp, c_temp = queue.pop(0)
                            tried_already.add((r_temp, c_temp))  
                            # print(color, "current tile", (r_temp, c_temp))
                            for dr, dc, pos1, pos2 in directions:
                                if (inside(r_temp + dr, c_temp + dc, board) and
                                    board[r_temp][c_temp][pos1] == color[0] and
                                    board[r_temp + dr][c_temp + dc][pos2] == color[0]
                                ):
                                    if (r_temp + dr, c_temp + dc) == start and length > 3:
                                        result[color] += length
                                        cycles[color].append(length)
                                        break 
                                    if (r_temp + dr, c_temp + dc) not in tried_already:
                                        queue.append((r_temp + dr, c_temp + dc))
                                        length += 1
                                        break
            tried_already = set()
            for r in range(len(board)):
                if board[r][0][0] == color[0]:
                    # print(color, "checking from this tile", (r, 0), "left to right")
                    queue = [(r, 0)]
                    length = 1
                    while queue:
                        r_temp, c_temp = queue.pop(0)
                        tried_already.add((r_temp, c_temp))
                        # print("current tile", (r_temp, c_temp))
                        if c_temp == len(board[0])-1 and board[r_temp][c_temp][2] == color[0]:
                                result[color] += length
                                lines[color].append(length)
                                break
                        for dr, dc, pos1, pos2 in directions:
                                if (
                                    inside(r_temp + dr, c_temp + dc, board)
                                    and board[r_temp][c_temp][pos1] == color[0]
                                    and board[r_temp + dr][c_temp + dc][pos2] == color[0]
                                    and (r_temp + dr, c_temp + dc) not in tried_already
                                ):
                                    queue.append((r_temp + dr, c_temp + dc))
                                    length += 1
                                    break
            tried_already = set()
            for c in range(len(board)):
                if board[0][c][1] == color[0]:
                    # print(color, "checking from this tile", (0, c), "top to bottom")
                    queue = [(0, c)]
                    length = 1
                    while queue:
                        r_temp, c_temp = queue.pop(0)
                        tried_already.add((r_temp, c_temp))
                        if r_temp == len(board)-1 and board[r_temp][c_temp][3] == color[0]:
                                result[color] += length
                                lines[color].append(length)
                                break
                        for dr, dc, pos1, pos2 in directions:
                                if (
                                    inside(r_temp + dr, c_temp + dc, board)
                                    and board[r_temp][c_temp][pos1] == color[0]
                                    and board[r_temp + dr][c_temp + dc][pos2] == color[0]
                                    and (r_temp + dr, c_temp + dc) not in tried_already
                                ):
                                    queue.append((r_temp + dr, c_temp + dc))
                                    length += 1
                                    break
        return result, cycles, lines





def cycles_lines(r, c, board, start, length, color, direction, mode, lookup, tried_already, res):
    if mode == "cycles":
        if [r, c] == start and length > 3:
            res.append(length)
            return True
    if mode == "lines":
        if (c == len(board) - 1 and direction == "lr") or (
            r == len(board) - 1 and direction == "td"
        ):
            if lookup[(direction, color, board[r][c])]:
                res.append(length + 1)
                return True
    length += 1
    directions = [
        (0, 1, 2, 0),
        (1, 0, 3, 1),
        (0, -1, 0, 2),
        (-1, 0, 1, 3),
    ]
    for dr, dc, pos1, pos2 in directions:
        if (
            inside(r + dr, c + dc, board)
            and board[r][c][pos1] == color[0]
            and board[r + dr][c + dc][pos2] == color[0]
            and str([r + dr, c + dc]) not in tried_already
        ):
            tried_already.add(str([r + dr, c + dc]))
            cycles_lines(r + dr, c + dc, board, start, length, color, direction, mode, lookup, tried_already, res)
            break
    else:
        return False


if __name__ == "__main__":
    # main(inp, set(), [])
    print(stats(inp))
