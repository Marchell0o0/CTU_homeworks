import numpy as np
from collections import deque
import draw as Drawer
import copy
from time import perf_counter

global board
d = Drawer.Drawer()

start_global = perf_counter()



board = [
        ['none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'dldl', 'dldl', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none', 'none']
        ]

board = np.array(board)


# print(board)

lookup_forced_tiles = {
    'l':{
        1: 'ddll',
        2: 'ldld',
        3: 'dlld',
        4: 'lddl',
        5: 'dldl',
        6: 'ddll',
        7: 'lldd',
        8: 'ldld',
        9: 'lddl',
        10: 'dlld',
        11: 'dldl',
        12: 'lldd'
    },
    'd':{
        1: 'lldd',
        2: 'dldl',
        3: 'lddl',
        4: 'dlld',
        5: 'ldld',
        6: 'lldd',
        7: 'ddll',
        8: 'dldl',
        9: 'dlld',
        10: 'lddl',
        11: 'ldld',
        12: 'ddll'
    }
}

directions = (
    (0, 1, 2, 0),
    (1, 0, 3, 1),
    (0, -1, 0, 2),
    (-1, 0, 1, 3),
    )

tiles = ["lldd", "dlld", "ddll", "lddl", "dldl", "ldld"]

shifts = ((0, -1), (-1,0), (0,1), (1,0))

indexes = ((0,1,2), (1,2,3), (2,3,0), (3,0,1))


def inside(r, c, board):
        return 0 <= r < len(board) and 0 <= c < len(board[0])

def getPossibleActions(board):
    edge_tiles = []
    res = []
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] != 'none':
                if r > 0 and board[r-1][c] == 'none':
                    if (r-1, c) not in edge_tiles:
                        edge_tiles.append((r-1, c))
                if r < len(board) - 1 and board[r+1][c] == 'none':
                    if (r+1, c) not in edge_tiles:
                        edge_tiles.append((r+1, c))
                if c > 0 and board[r][c-1] == 'none':
                    if (r, c - 1) not in edge_tiles:
                        edge_tiles.append((r, c - 1))
                if c < len(board[0]) - 1 and board[r][c+1] == 'none':
                    if (r, c + 1) not in edge_tiles:
                        edge_tiles.append((r, c + 1))
    for edge in edge_tiles:
        for tile in tiles:
            move = get_a_move(edge[0], edge[1], tile, board)
            if move:
                res.append(tuple(move))
    return res

def get_a_move(r, c, tile, board):
    temp_board = board.copy()
    res = []
    if isLegal(r, c, tile, temp_board):

        queue = deque([(r, c, tile)])
        res.append((r, c, tile))

        while queue:
            r_temp, c_temp, tile_temp = queue.popleft()
            # print("current tile",r_temp, c_temp, tile_temp)
            # temp_board = temp_board[:r_temp] + ((temp_board[r_temp][:c_temp] + (tile_temp,) +temp_board[r_temp][c_temp+1:]),) + temp_board[ r_temp + 1:]
            temp_board[r_temp][c_temp] = tile_temp
            for idx, shift in enumerate(shifts):
                r_shift = shift[0] + r_temp
                c_shift = shift[1] + c_temp
                color_of_main_tile = tile_temp[idx]
                if inside(r_shift, c_shift, temp_board) and temp_board[r_shift][c_shift] == 'none':
                    # print("current shift tile", r_shift, c_shift)
                    colors_of_checked_tiles = ['','','']
                    for i, item in enumerate([shifts   [indexes[(idx + 3) % 4] [0]], shifts  [indexes[(idx + 3) % 4] [1]],  shifts   [indexes[(idx + 3) % 4] [2] ]]):
                    # print("this is a possible shift tile", r_shift, c_shift, "direction", shift, idx)
                        r_d, c_d = item
                        forced = False
                        r_d_shift = r_d + r_shift
                        c_d_shift = c_d + c_shift
                        if inside(r_d_shift, c_d_shift, temp_board) and temp_board[r_d_shift][c_d_shift] != 'none':
                            colors_of_checked_tiles[i] = (temp_board[r_d_shift][c_d_shift][indexes[(idx + 1) % 4][i]])
                    # print("colors of forcing tiles",colors_of_checked_tiles)
                    # print('color of a main tile',color_of_main_tile)
                    if color_of_main_tile in colors_of_checked_tiles:
                        if colors_of_checked_tiles.count(color_of_main_tile) == 1:
                            forced = True
                            forced_tile = lookup_forced_tiles[color_of_main_tile][idx*3 + colors_of_checked_tiles.index(color_of_main_tile) + 1]
                            # print("forced move, placing this", forced_tile)
                            move = ((r_shift, c_shift, forced_tile)) 
                            queue.append(move)
                            if move not in res:
                                res.append(move)
                            forced = False
                        else:
                            return False  
        return res
    else:
        return False

def isLegal(r, c, tile, board):
    if (
        (r == 0 or board[r - 1][c] == "none" or board[r - 1][c][3] == tile[1])
        and (c == len(board[0]) - 1 or board[r][c + 1] == "none" or board[r][c + 1][0] == tile[2])
        and (r == len(board) - 1 or board[r + 1][c] == "none" or board[r + 1][c][1] == tile[3])
        and (c == 0 or board[r][c - 1] == "none" or board[r][c - 1][2] == tile[0])
    ):
        return True
    else:
        return False


# print(*moves, sep='\n')



board_get_action_test = [
    ['lddl', 'dldl', 'dlld', 'lldd', 'dldl', 'dldl', 'ddll'],
    ['lldd', 'dlld', 'ldld', 'lddl', 'dldl', 'dlld', 'lldd'],
    ['none', 'none', 'lddl', 'dldl', 'dldl', 'ddll', 'lddl'],
    ['none', 'none', 'lldd', 'dldl', 'dlld', 'lldd', 'dldl'],
    ['lldd', 'ddll', 'lddl', 'dlld', 'ldld', 'lddl', 'dlld'],
    ['lddl', 'dldl', 'dlld', 'ldld', 'lddl', 'dlld', 'ldld'],
    ['none', 'dldl', 'ddll', 'lddl', 'dlld', 'lddl', 'ddll']
]

board_get_action_test = np.array(board_get_action_test)

start = perf_counter()
moves = getPossibleActions(board_get_action_test)
end = perf_counter()
print("time of a possible moves func", end - start)

d.draw(board_get_action_test, "starting board.png")

assert getPossibleActions(board_get_action_test) == [
    ((2, 0, 'lddl'), (2, 1, 'ddll'), (3, 0, 'dldl'), (3, 1, 'dlld')),
    ((2, 0, 'ldld'), (2, 1, 'ldld'), (3, 1, 'ldld'), (3, 0, 'ddll')),
    ((2, 1, 'ddll'), (2, 0, 'lddl'), (3, 1, 'dlld'), (3, 0, 'dldl')),
    ((2, 1, 'ldld'), (3, 1, 'ldld'), (3, 0, 'ddll'), (2, 0, 'ldld')),
    ((3, 1, 'dlld'), (2, 1, 'ddll'), (2, 0, 'lddl'), (3, 0, 'dldl')),
    ((3, 1, 'ldld'), (3, 0, 'ddll'), (2, 1, 'ldld'), (2, 0, 'ldld')),
    ((3, 0, 'ddll'), (2, 0, 'ldld'), (3, 1, 'ldld'), (2, 1, 'ldld')),
    ((3, 0, 'dldl'), (3, 1, 'dlld'), (2, 1, 'ddll'), (2, 0, 'lddl')),
    ((6, 0, 'lldd'),),
    ((6, 0, 'dldl'),)
    ], "getPossibleAction function isnt working properly"




end_global = perf_counter()
print("whole program took", end_global - start_global)

