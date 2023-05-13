
import draw as Drawer
import base as Base
from collections import deque
import numpy as np
import time

global size


class Player(Base.BasePlayer):
    def __init__(self, board, name, color):
        Base.BasePlayer.__init__(self, board, name, color)
        self.algorithmName = "My great player"

    def move(self):
        global size
        res = []
        board = np.array(self.board)

        size = len(board)
        my_color = self.myColor
        State0 = game_state(board, self.myColor)
        if State0.is_game_over():
            if not any('none' in i for i in board):
                return []
            else:
                rmove = State0.get_legal_actions()[0]
        else:
            rmove = minimax_2(State0, 3, float(
                '-inf'), float('inf'), my_color)
        if rmove:
            for move in rmove:
                r, c, tile = move
                res.append([r, c, tile])
        else:
            return []
        return res


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


def minimax(initial_state, me):
    best_action = None
    max_eval = float('-inf')
    # alpha = float('-inf')
    # beta = float('inf')
    possible_action_1 = initial_state.get_legal_actions()
    if me == 'l':
        for action_1 in possible_action_1:
            child_1 = initial_state.move(action_1)
            if child_1.game_result_minimax('l') == 1:
                return action_1
            else:
                min_eval = float('inf')
                possible_actions_2 = child_1.get_legal_actions()
                for action_2 in possible_actions_2:
                    child_2 = child_1.move(action_2)
                    eval_2 = child_2.game_result_minimax('l')
                    if eval_2 == -1:
                        min_eval = -1
                        break
                    min_eval = min(min_eval, eval_2)
                eval_1 = min_eval
                if eval_1 > max_eval:
                    max_eval = eval_1
                    best_action = action_1

    else:
        for action_1 in possible_action_1:
            child_1 = initial_state.move(action_1)
            if child_1.game_result_minimax('d') == 1:
                return action_1
            else:
                min_eval = float('inf')
                possible_actions_2 = child_1.get_legal_actions()
                for action_2 in possible_actions_2:
                    child_2 = child_1.move(action_2)
                    eval_2 = child_2.game_result_minimax('d')
                    if eval_2 == -1:
                        min_eval = -1
                        break
                    min_eval = min(min_eval, eval_2)
                eval_1 = min_eval
                if eval_1 > max_eval:
                    max_eval = eval_1
                    best_action = action_1
    return best_action


def minimax_2(state, depth, alpha, beta, me):
    best_action = None

    max_eval = float('-inf')
    possible_actions = state.get_legal_actions()
    for action in possible_actions:
        child = state.move(action)
        eval = minimax_2_inner(child, depth - 1, False, alpha, beta, me)

        if eval > max_eval:
            max_eval = eval
            best_action = action

        alpha = max(alpha, eval)
        if beta <= alpha:
            break
    return best_action


def minimax_2_inner(state, depth, maximizing_player, alpha, beta, me):
    if depth == 0 or state.is_game_over():
        if me == 'l':
            return state.game_result_minimax('l')
        else:
            return state.game_result_minimax('d')

    if maximizing_player:
        max_eval = float('-inf')
        possible_actions = state.get_legal_actions()
        for action in possible_actions:
            child = state.move(action)
            eval = minimax_2_inner(child, depth - 1, False, alpha, beta, me)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = float('inf')
        possible_actions = state.get_legal_actions()
        for action in possible_actions:
            child = state.move(action)
            eval = minimax_2_inner(child, depth - 1, True, alpha, beta, me)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


class game_state:
    def __init__(self, board, my_color) -> None:
        self.board = board
        self.my_color = my_color

    def get_legal_actions(self):
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

    def is_game_over(self):
        board = self.board

        if not any('none' in i for i in board):
            return True

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
                                        return True
                                    else:
                                        if (r_s, c_s) not in tried_already:
                                            length += 1
                                            queue.append((r_s, c_s))
                                            break

            tried_already = set()
            for r in range(size):
                if board[r][0][0] == color[0]:
                    queue = deque([(r, 0)])
                    while queue:
                        r_temp, c_temp = queue.popleft()
                        tried_already.add((r_temp, c_temp))
                        if c_temp == size-1 and board[r_temp][c_temp][2] == color[0]:
                            return True
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
                                break

            tried_already = set()
            for c in range(size):
                if board[0][c][1] == color[0]:
                    queue = deque([(0, c)])
                    while queue:
                        r_temp, c_temp = queue.popleft()
                        tried_already.add((r_temp, c_temp))
                        if r_temp == size-1 and board[r_temp][c_temp][3] == color[0]:
                            return True
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
                                break

        return False

    def game_result_minimax(self, color_player):
        global size
        board = self.board
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
                if board[r][0] != 'none' and board[r][0][0] == color[0]:
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
                if board[0][c] != 'none' and board[0][c][1] == color[0]:
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
        if cycles_lines['dark'] == cycles_lines['light']:
            return 0
        elif color_player == 'l':
            if cycles_lines['light'] > cycles_lines['dark']:
                return 1
            else:
                return -1
        elif color_player == 'd':
            if cycles_lines['light'] < cycles_lines['dark']:
                return 1
            else:
                return -1

    def move(self, action):
        temp_board = self.board.copy()
        for tile in action:
            r_temp, c_temp, tile_temp = tile
            temp_board[r_temp][c_temp] = tile_temp
        if self.my_color == 'l':
            return game_state(temp_board, 'd')
        else:
            return game_state(temp_board, 'l')


def inside(r, c):
    global size
    return 0 <= r < size and 0 <= c < size


if __name__ == "__main__":

    board = [
        ['none', 'none', 'none', 'none', 'none',
            'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none',
            'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none',
            'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none',
            'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none',
            'dldl', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none',
            'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none',
            'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none',
            'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none',
            'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none',
            'none', 'none', 'none', 'none', 'none'],
    ]
    p1 = Player(board, "player1", 'l')
    p2 = Player(board, "player2", 'd')

    d = Drawer.Drawer()

    # def main_2(p1, p2):
    idx = 0
    while True:
        start = time.perf_counter()
        rmove = p1.move()
        end = time.perf_counter()
        print(rmove, "move took", end - start)
        # print(p1.myColor, "is making a move", rmove)

        for move in rmove:
            row, col, tile = move
            p1.board[row][col] = tile
            p2.board[row][col] = tile

        d.draw(p1.board, f"move-{idx}, {p1.myColor}.png")
        idx += 1

        if len(rmove) == 0:
            break
        p1, p2 = p2, p1
#    # """
#     with cProfile.Profile() as pr:
#         main_2(p1, p2)
#     stats = pstats.Stats(pr)
#     stats.sort_stats(pstats.SortKey.TIME)
#     # stats.print_stats()
#     stats.dump_stats(filename="profiling.prof")
#     # """
