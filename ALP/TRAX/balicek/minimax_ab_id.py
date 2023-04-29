import draw as Drawer
import sys
import random
import copy
import base as Base
import time
import math
from collections import deque
import numpy as np
import cProfile
import pstats


global size


class Player(Base.BasePlayer):
    def __init__(self, board, name, color):
        Base.BasePlayer.__init__(self, board, name, color)
        self.algorithmName = "My great player"

    def move(self):
        global size
        start = time.time()
        temp_board = np.array(self.board)
        size = len(board)
        rmove = []
        # Ten seconds
        # try:
        #     long_function_call()
        # except Exception, msg:
        #     print "Timed out!"
        # i = 1
        if self.myColor == 'l':
            # start = time.time()
            # while time.time() - start  < 1:
            root = tree_node_light(game_state(temp_board), 0)
            rmove = minimax_light(root, 3, temp_board)
            # i += 1
            # if move_temp:
            #     rmove = move_temp
            # else:
            #     break
        else:
            # start = time.time()
            # while time.time() - start  < 1:
            root = tree_node_dark(game_state(temp_board), 0)
            rmove = minimax_dark(root, 3, temp_board)
            # i += 1
            # if move_temp:
            # rmove = move_temp
            # else:
            # break
        # print(i)
        return rmove

    def move_random(self):
        global size
        board = np.array(self.board)
        size = len(board)

        r_move = []
        State0 = game_state(board)
        possible_actions = State0.getPossibleActions()
        if possible_actions:
            for tile_move in possible_actions[0]:
                r, c, tile = tile_move
                r_move.append([r, c, tile])
            return r_move
        else:
            return []


class tree_node_light:
    def __init__(self, state, depth):
        self.state = state
        self.stat_temp = state.cycles_lines2_0()
        self.isTerminal = state.isTerminal(self.stat_temp[1])
        self.depth = depth
        self.children = []

        self.saldo = self.stat_temp[0]['light'] - self.stat_temp[0]['dark']


class tree_node_dark:
    def __init__(self, state, depth):
        self.state = state
        self.stat_temp = state.cycles_lines2_0()
        self.isTerminal = state.isTerminal(self.stat_temp[1])
        self.depth = depth
        self.children = []

        self.saldo = self.stat_temp[0]['dark'] - self.stat_temp[0]['light']


def minimax_light(node, depth, board):
    branch = 0
    res = []
    best_child = None
    if node.isTerminal:
        return []

    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    possible_actions = node.state.getPossibleActions()

    for action in possible_actions:

        child = take_Action_light(node, action)
        eval = minimax_inner_light(child, depth - 1, False, alpha, beta)
        alpha = max(alpha, eval)
        if beta <= alpha:
            break
        # d.draw(child.state.board, f"{branch} points of this branch are {eval}.png")

        if eval > max_eval:
            max_eval = eval
            best_child = child
        branch += 1

    # print("best score to get", max_eval)

    solution_board = best_child.state.board
    for r in range(size):
        for c in range(size):
            if board[r][c] != solution_board[r][c]:
                res.append([r, c, solution_board[r][c]])
    return res


def minimax_dark(node, depth, board):
    branch = 0
    res = []
    best_child = None
    if node.isTerminal:
        return []

    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    possible_actions = node.state.getPossibleActions()

    for action in possible_actions:

        child = take_Action_dark(node, action)
        eval = minimax_inner_dark(child, depth - 1, False, alpha, beta)
        alpha = max(alpha, eval)
        if beta <= alpha:
            break
        # d.draw(child.state.board, f"{branch} points of this branch are {eval}.png")

        if eval > max_eval:
            max_eval = eval
            best_child = child
        branch += 1

    # print("best score to get", max_eval)

    solution_board = best_child.state.board
    for r in range(size):
        for c in range(size):
            if board[r][c] != solution_board[r][c]:
                res.append([r, c, solution_board[r][c]])
    return res


def minimax_inner_light(node, depth, maximizing_player, alpha, beta):
    # d.draw(node.state.board, f"branch {branch}, depth {depth}, {node.saldo}.png")
    # print(node.state.current_player)
    if depth == 0 or node.isTerminal:
        # d.draw(node.state.board, f"{count, node.stat_temp, node.saldo}.png")
        return node.saldo

    if maximizing_player:
        max_eval = float('-inf')
        possible_actions = node.state.getPossibleActions()
        for action in possible_actions:
            child = take_Action_light(node, action)
            # node_number += 1
            eval = minimax_inner_light(child, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = float('inf')
        possible_actions = node.state.getPossibleActions()
        for action in possible_actions:
            child = take_Action_light(node, action)
            # node_number += 1
            eval = minimax_inner_light(child, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def minimax_inner_dark(node, depth, maximizing_player, alpha, beta):

    # d.draw(node.state.board, f"branch {branch}, depth {depth}, {node.saldo}.png")
    # print(node.state.current_player)
    if depth == 0 or node.isTerminal:
        # d.draw(node.state.board, f"{count, node.stat_temp, node.saldo}.png")
        return node.saldo

    if maximizing_player:
        max_eval = float('-inf')
        possible_actions = node.state.getPossibleActions()
        for action in possible_actions:
            child = take_Action_dark(node, action)
            # node_number += 1
            eval = minimax_inner_dark(child, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = float('inf')
        possible_actions = node.state.getPossibleActions()
        for action in possible_actions:
            child = take_Action_dark(node, action)
            # node_number += 1
            eval = minimax_inner_dark(child, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def take_Action_light(node, move):
    temp_board = node.state.board.copy()

    for tile in move:
        r_temp, c_temp, tile_temp = tile
        temp_board[r_temp][c_temp] = tile_temp

    # if node.state.current_player == "d":
    next_node = tree_node_light(game_state(temp_board), node.depth + 1)
    # else:
    # next_node = tree_node(game_state(temp_board), node.depth + 1)
    node.children.append(next_node)
    return next_node


def take_Action_dark(node, move):
    temp_board = node.state.board.copy()

    for tile in move:
        r_temp, c_temp, tile_temp = tile
        temp_board[r_temp][c_temp] = tile_temp

    # if node.state.current_player == "d":
    next_node = tree_node_dark(game_state(temp_board), node.depth + 1)
    # else:
    # next_node = tree_node(game_state(temp_board), node.depth + 1)
    node.children.append(next_node)
    return next_node


lookup_forced_tiles = {
    'l': {
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
    'd': {
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

directions2 = (
    (0, 1, 2, 0),
    (1, 0, 3, 1),
    (0, -1, 0, 2),
    (-1, 0, 1, 3),
)

directions = {
    (0, 1, 2, 0): 1,
    (1, 0, 3, 1): 1,
    (0, -1, 0, 2): 1,
    (-1, 0, 1, 3): 1,
}

tiles = ["lldd", "dlld", "ddll", "lddl", "dldl", "ldld"]

shifts = {
    (0, -1, 0): ((1, 0, 1), (0, -1, 2), (-1, 0, 3)),
    (-1, 0, 1): ((0, -1, 2), (-1, 0, 3), (0, 1, 0)),
    (0, 1, 2): ((-1, 0, 3), (0, 1, 0), (1, 0, 1)),
    (1, 0, 3): ((0, 1, 0), (1, 0, 1), (0, -1, 2)),
}


class game_state:
    def __init__(self, board):
        self.board = board
        # self.current_player = current_player
        self.children = []

    def getPossibleActions(self):
        board = self.board
        res = []
        edge_tiles = set()
        for r in range(size):
            for c in range(size):
                if board[r][c] != 'none':
                    if r > 0 and board[r-1][c] == 'none':
                        edge_tiles.add((r-1, c))
                    if r < size - 1 and board[r+1][c] == 'none':
                        edge_tiles.add((r+1, c))
                    if c > 0 and board[r][c-1] == 'none':
                        edge_tiles.add((r, c - 1))
                    if c < size - 1 and board[r][c+1] == 'none':
                        edge_tiles.add((r, c + 1))
        for edge in edge_tiles:
            for tile in tiles:
                done = False
                if res:
                    for variant in res:
                        if (edge[0], edge[1], tile) in variant:
                            done = True
                    if done == False:
                        move = self.get_a_move(edge[0], edge[1], tile)
                        if move:
                            res.append(move)
                else:
                    move = self.get_a_move(edge[0], edge[1], tile)
                    if move:
                        res.append(move)
        res = list(map(tuple, res))
        res.sort(key=len)
        return res

    def get_a_move(self, r, c, tile):
        temp_board = self.board.copy()
        res = set()
        if self.isLegal(r, c, tile):

            queue = deque([(r, c, tile)])
            res.add((r, c, tile))

            while queue:
                r_temp, c_temp, tile_temp = queue.popleft()
                temp_board[r_temp][c_temp] = tile_temp
                for shift in shifts:
                    count = 0
                    r_shift = shift[0] + r_temp
                    c_shift = shift[1] + c_temp
                    color_of_main_tile = tile_temp[shift[2]]
                    if inside(r_shift, c_shift) and temp_board[r_shift][c_shift] == 'none':
                        for i in range(3):
                            r_d, c_d, color = shifts[shift][i]
                            r_d_shift = r_d + r_shift
                            c_d_shift = c_d + c_shift
                            if inside(r_d_shift, c_d_shift):
                                tile_d_shift = temp_board[r_d_shift][c_d_shift]
                                if tile_d_shift[color] == color_of_main_tile:
                                    count += 1
                                    index = i
                        # if count != 0:
                        if count == 1:
                            forced_tile = lookup_forced_tiles[color_of_main_tile][shift[2]*3 + index + 1]
                            move = ((r_shift, c_shift, forced_tile))
                            queue.append(move)
                            if move not in res:
                                res.add(move)
                        elif count > 1:
                            return False
            return res
        else:
            return False

    def isLegal(self, r, c, tile):
        board = self.board
        if (
            (r == 0 or board[r - 1][c] ==
             "none" or board[r - 1][c][3] == tile[1])
            and (c == size - 1 or board[r][c + 1] == "none" or board[r][c + 1][0] == tile[2])
            and (r == size - 1 or board[r + 1][c] == "none" or board[r + 1][c][1] == tile[3])
            and (c == 0 or board[r][c - 1] == "none" or board[r][c - 1][2] == tile[0])
        ):
            return True
        else:
            return False

    def cycles_lines2_0(self):
        board = self.board

        # count = 0
        # result = {"light":0., "dark":0.}
        # length_of_lines = {"light":0, "dark":0}
        # count_of_lines = {"light":0, "dark":0}

        cycles_count = 0
        points = {"light": 0, "dark": 0}
        for color in ["light", "dark"]:
            tried_already = set()
            for r in range(size):
                for c in range(size):
                    if board[r][c] != "none" and ((r, c) not in tried_already):
                        # print("checking from this tile", (r,c))
                        length = 1
                        start = (r, c)
                        queue = deque([(r, c)])
                        cycle = False
                        while queue:
                            r_temp, c_temp = queue.popleft()
                            # print("cvurrent tile",r_temp, c_temp)
                            tried_already.add((r_temp, c_temp))
                            for r_shift, c_shift, main_color, temp_color in directions:
                                r_s = r_temp + r_shift
                                c_s = c_temp + c_shift
                                # print(board[r_temp][c_temp][main_color], board[r_s][c_s][temp_color])
                                # print(r_s,c_s,(r_s, c_s) not in tried_already)
                                if (inside(r_s, c_s) and
                                        board[r_s][c_s] != 'none' and
                                        board[r_temp][c_temp][main_color] == color[0] and
                                        board[r_s][c_s][temp_color] == color[0]
                                        ):
                                    if (r_s, c_s) == start and length > 3:
                                        cycle = True
                                        cycles_count += 1
                                        break
                                    else:
                                        if (r_s, c_s) not in tried_already:
                                            length += 1
                                            queue.append((r_s, c_s))
                                            break
                                    # previous = (r_temp, c_temp)

                        if not cycle:
                            points[color] += length**2
                        else:
                            points[color] += 100*length
                            # print(color, "cycle points", length*5)
                        # count_of_lines[color] += 1
            # print(color, res)
            # print(color, length_of_lines[color], count_of_lines[color])
            # result[color] = length_of_lines[color]/count_of_lines[color]
        return points, cycles_count

    def isTerminal(self, cycles):
        return cycles != 0 or (not any('none' in i for i in self.board))


def inside(r, c):
    global size
    return 0 <= r < size and 0 <= c < size


if __name__ == "__main__":

    boardRows = 10
    boardCols = boardRows
    board = [["none"]*boardCols for _ in range(boardRows)]
    board[boardRows//2][boardCols//2] = ["lldd", "dlld",
                                         "ddll", "lddl", "dldl", "ldld"][random.randint(0, 5)]

    d = Drawer.Drawer()

    board_get_action_test = [
        ['lddl', 'dldl', 'dlld', 'lldd', 'dldl', 'dldl', 'ddll'],
        ['lldd', 'dlld', 'ldld', 'lddl', 'dldl', 'dlld', 'lldd'],
        ['none', 'none', 'lddl', 'dldl', 'dldl', 'ddll', 'lddl'],
        ['none', 'none', 'lldd', 'dldl', 'dlld', 'lldd', 'dldl'],
        ['lldd', 'ddll', 'lddl', 'dlld', 'ldld', 'lddl', 'dlld'],
        ['lddl', 'dldl', 'dlld', 'ldld', 'lddl', 'dlld', 'ldld'],
        ['none', 'dldl', 'ddll', 'lddl', 'dlld', 'lddl', 'ddll']
    ]
#     board_get_action_test = np.array(board_get_action_test)
#     State_test = game_state(board_get_action_test, "l")
#     start = time.perf_counter()
#     moves = State_test.getPossibleActions()
#     end = time.perf_counter()
#     print("time of a possible moves func", end - start)
    # print(*moves, sep='\n')
    # for idx, move in enumerate(moves):
    #     temp_board = board_get_action_test.copy()
    #     for tile in move:
    #         temp_board[tile[0]][tile[1]] = tile[2]
    #     print(move, cycles_lines(temp_board))
    #     d.draw(temp_board, f"move {move, idx}.png")
    # assert getPossibleActions(board_get_action_test) == [
    #     ((3, 1, 'dlld'), (3, 0, 'dldl'), (2, 0, 'lddl'), (2, 1, 'ddll')),
    #     ((2, 1, 'ldld'), (3, 1, 'ldld'), (2, 0, 'ldld'), (3, 0, 'ddll')),
    #     ((6, 0, 'lldd'),),
    #     ((6, 0, 'dldl'),)
    # ], "getPossibleAction function isnt working properly"
    # sys.exit()

    # d.draw(board_get_action_test, 'testing.png')

    # State0 = game_state(board_get_action_test, 'l')
    # print(State0.cycles_lines2_0())

    """
    def get_Saldo(board):
        for _ in range(1000):
            State0 = tree_node_light(game_state(board), 0)
        return 

    board_get_action_test = np.array(board_get_action_test)
    
    size = 
    with cProfile.Profile() as pr:
        
        get_Saldo(board_get_action_test)
        # State0.saldo
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    stats.dump_stats(filename= "profiling_cycles.prof")
    """

    # root_test_first_expansion = tree_node(State0, 0)
    # root_test_minimax = tree_node_light(State0, 0)
    # start = time.perf_counter()

    # PA = root_test_first_expansion.state.getPossibleActions()
    # i = 0
    # for action in PA:

    #     node_temp = take_Action(root_test_first_expansion, action)
    #     # d.draw(node_temp.state.board, f"{i, node_temp.saldo}.png")
    #     print(node_temp.saldo)
    #     i += 1

    # solution = minimax(root_test_minimax, 3)
    # print("best move", solution.saldo)
    # d.draw(solution.state.board, 'solution.png')

    """
    не добавлять уже использованные ноды в потомков 
    переписать ебучие статы 
    возможно сохранять статы из предидущих досок 

    """

    """

    board = [
        ['none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'lldd', 'dlld', 'none', 'none'],
        ['none', 'none', 'lddl', 'ddll', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none'],
        ]

    board_get_action_test = np.array(board_get_action_test)

    State0 = game_state(board_get_action_test)
    start = time.perf_counter()
    with cProfile.Profile() as pr:
        # root = tree_node_light(game_state(board_get_action_test), 0)
        for _ in range(1000):
            print(State0.cycles_lines2_0())
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    # stats.dump_stats(filename= "profiling_cycles_deeper.prof")
    end = time.perf_counter()


    # print(root.saldo)
    print("time", end - start)
    sys.exit()

    """
    p1 = Player(board, "player1", 'l')
    p2 = Player(board, "player2", 'd')

    def main_2(p1, p2):
        idx = 0
        while True:

            rmove = p1.move()

            print(p1.myColor, "is making a move", rmove)
            # print(f"{idx}, move took: {end - start}")
            # sys.exit()

            for move in rmove:
                row, col, tile = move
                p1.board[row][col] = tile
                p2.board[row][col] = tile

            # d.draw(p1.board, f"move-{idx}, {p1.myColor}.png")
            idx += 1

            if len(rmove) == 0:
                break
            p1, p2 = p2, p1
    # """
    with cProfile.Profile() as pr:
        main_2(p1, p2)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    stats.dump_stats(filename="profiling.prof")
    # """


"""
 minimax using only 2 depth (last resort)
MCTS using all new functions


"""
