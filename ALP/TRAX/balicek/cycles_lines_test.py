from collections import deque
import draw as Drawer
import numpy as np

global size

directions = {
    (0, 1, 2, 0): 1,
    (1, 0, 3, 1): 1,
    (0, -1, 0, 2): 1,
    (-1, 0, 1, 3): 1,
}


def game_result(board):
    cycles_lines = {"light": 0, "dark": 0}
    for color in ["light", "dark"]:
        tried_already = set()
        for r in range(size):
            for c in range(size):
                if board[r][c] != "none" and ((r, c) not in tried_already):
                    length = 1
                    start = (r, c)
                    queue = deque([(r, c)])
                    while queue:
                        r_temp, c_temp = queue.popleft()
                        tried_already.add((r_temp, c_temp))
                        for r_shift, c_shift, main_color, temp_color in directions:
                            r_s = r_temp + r_shift
                            c_s = c_temp + c_shift
                            if (inside(r_s, c_s) and
                                    board[r_s][c_s] != 'none' and
                                    board[r_temp][c_temp][main_color] == color[0] and
                                    board[r_s][c_s][temp_color] == color[0]
                                ):
                                if (r_s, c_s) == start and length > 3:
                                    cycles_lines[color] += length
                                else:
                                    if (r_s, c_s) not in tried_already:
                                        length += 1
                                        queue.append((r_s, c_s))
                                        break

        tried_already = set()
        for r in range(size):
            if board[r][0][0] == color[0]:
                queue = deque([(r, 0)])
                length = 1
                while queue:
                    r_temp, c_temp = queue.popleft()
                    tried_already.add((r_temp, c_temp))
                    if c_temp == size-1 and board[r_temp][c_temp][2] == color[0]:
                        cycles_lines[color] += length
                    for r_shift, c_shift, main_color, temp_color in directions:
                        r_s = r_temp + r_shift
                        c_s = c_temp + c_shift
                        if (inside(r_s, c_s) and
                                board[r_s][c_s] != 'none' and
                                board[r_temp][c_temp][main_color] == color[0] and
                                board[r_s][c_s][temp_color] == color[0] and
                                (r_s, c_s) not in tried_already
                            ):
                            length += 1
                            queue.append((r_s, c_s))
                            break

        tried_already = set()
        for c in range(size):
            if board[0][c][1] == color[0]:
                queue = deque([(0, c)])
                length = 1
                while queue:
                    r_temp, c_temp = queue.popleft()
                    tried_already.add((r_temp, c_temp))
                    if r_temp == size-1 and board[r_temp][c_temp][3] == color[0]:
                        cycles_lines[color] += length
                    for r_shift, c_shift, main_color, temp_color in directions:
                        r_s = r_temp + r_shift
                        c_s = c_temp + c_shift
                        if (inside(r_s, c_s) and
                                board[r_s][c_s] != 'none' and
                                board[r_temp][c_temp][main_color] == color[0] and
                                board[r_s][c_s][temp_color] == color[0] and
                                (r_s, c_s) not in tried_already
                            ):
                            queue.append((r_s, c_s))
                            length += 1
                            break

    return cycles_lines


def inside(r, c):
    global size
    return 0 <= r < size and 0 <= c < size


board = [
        ['dldl', 'dldl', 'dlld', 'lldd', 'dldl', 'dldl', 'dldl'],
        ['lldd', 'dlld', 'ldld', 'lddl', 'dldl', 'dlld', 'lldd'],
        ['lddl', 'ddll', 'lddl', 'dldl', 'dldl', 'ddll', 'lddl'],
        ['dldl', 'dlld', 'lldd', 'dldl', 'dlld', 'lldd', 'dldl'],
        ['lldd', 'ddll', 'lddl', 'dlld', 'ldld', 'lddl', 'dlld'],
        ['lddl', 'dldl', 'dlld', 'ldld', 'lddl', 'dlld', 'ldld'],
        ['dldl', 'dldl', 'ddll', 'lddl', 'dlld', 'lddl', 'ddll']
]

board = np.array(board)

size = len(board)

d = Drawer.Drawer()

d.draw(board, "cycles_lines.png")

print(game_result(board))
