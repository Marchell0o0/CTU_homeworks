import draw as Drawer
import sys
import random
import copy
import base as Base
import time
import math
from collections import deque, defaultdict
import cProfile
import pstats
import numpy as np

global size
global my_color


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
        State0 = MCTS_state(board, self.myColor)
        if State0.is_game_over():
            return []
        else:
            root = MonteCarloTreeSearchNode(State0, my_color)
            selected_node = root.best_action(1)
            rmove = selected_node.parent_action
            for move in rmove:
                r, c, tile = move
                res.append([r, c, tile])
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


class MonteCarloTreeSearchNode():
    def __init__(self, state, color, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        self.color = color
        return

    def untried_actions(self):

        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):

        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        if self.color == 'l':
            child_node = MonteCarloTreeSearchNode(
                next_state, 'd', parent=self, parent_action=action)
        else:
            child_node = MonteCarloTreeSearchNode(
                next_state, 'l', parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        current_rollout_state = self.state
        count = 0
        if self.color == 'l':
            me, enemy = 'l', 'd'
            while not current_rollout_state.is_game_over():
                # print("propagating...")
                possible_moves = current_rollout_state.get_legal_actions()
                if possible_moves:

                    minimax_action = self.minimax(
                        current_rollout_state, possible_moves, me)

                    if minimax_action:  # making a minimax move
                        current_rollout_state = current_rollout_state.move(
                            minimax_action)
                        # print("making minimax action")

                    else:  # making a random move
                        random_action = self.rollout_policy(possible_moves)
                        current_rollout_state = current_rollout_state.move(
                            random_action)
                        # print("making random action")

                else:
                    break
                # d.draw(current_rollout_state.board,
                    #    f"{count}, {me} rolling out {current_rollout_state.game_result()}.png")
                me, enemy = enemy, me
                count += 1

        return current_rollout_state.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=2):
        # print(self.children)
        choices_weights = [(c.q() / c.n()) + c_param *
                           np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):

        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self, time_limit):
        start = time.time()
        while time.time() - start < time_limit:
            # for _ in range(simulation_no):
            v = self._tree_policy()
            # print("checking this child", v.state.board)
            reward = v.rollout()
            v.backpropagate(reward)
        return self.best_child(c_param=2)

    def minimax(self, rollout_state, possible_action_1, me):
        best_action = None
        found = False
        max_eval = float('-inf')
        # alpha = float('-inf')
        # beta = float('inf')
        if me == 'l':
            for action_1 in possible_action_1:
                child_1 = rollout_state.move(action_1)
                if child_1.game_result_minimax('l') == 1:
                    return action_1
                else:
                    min_eval = float('inf')
                    possible_actions_2 = child_1.get_legal_actions()
                    # d.draw(child_1.board, f"child depth 1 {action_1}.png")
                    for action_2 in possible_actions_2:
                        child_2 = child_1.move(action_2)
                        eval_2 = child_2.game_result_minimax('l')
                        if eval_2 == -1:
                            min_eval = -1
                            break
                        min_eval = min(min_eval, eval_2)
                    eval_1 = min_eval
                    if eval_1 != 0:
                        found = True
                    if eval_1 > max_eval:
                        max_eval = eval_1
                        best_action = action_1
            if found:
                return best_action
            else:
                return None
        else:
            for action_1 in possible_action_1:
                child_1 = rollout_state.move(action_1)
                if child_1.game_result_minimax('d') == 1:
                    return action_1
                else:
                    min_eval = float('inf')
                    possible_actions_2 = child_1.get_legal_actions()
                    # d.draw(child_1.board, f"child depth 1 {action_1}.png")
                    for action_2 in possible_actions_2:
                        child_2 = child_1.move(action_2)
                        eval_2 = child_2.game_result_minimax('d')
                        if eval_2 == -1:
                            min_eval = -1
                            break
                        min_eval = min(min_eval, eval_2)
                    eval_1 = min_eval
                    if eval_1 != 0:
                        found = True
                    if eval_1 > max_eval:
                        max_eval = eval_1
                        best_action = action_1
            if found:
                return best_action
            else:
                return None


class MCTS_state:
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

    def game_result(self):
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
        if cycles_lines['dark'] == cycles_lines['light']:
            return 0
        elif self.my_color == 'l':
            if cycles_lines['light'] > cycles_lines['dark']:
                return 1
            else:
                return -1
        elif self.my_color == 'd':
            if cycles_lines['light'] < cycles_lines['dark']:
                return 1
            else:
                return -1

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
            return MCTS_state(temp_board, 'd')
        else:
            return MCTS_state(temp_board, 'l')


def inside(r, c):
    global size
    return 0 <= r < size and 0 <= c < size


if __name__ == "__main__":

    board = [
        ['none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'ddll', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none'],
    ]

    p1 = Player(board, "player1", 'l')
    p2 = Player(board, "player2", 'd')

    d = Drawer.Drawer()

    """"
    # board = [
    #     ['none', 'none', 'none'],
    #     ['none', 'dldl', 'none'],
    #     ['none', 'none', 'none']
    # ]

    
    board = np.array(board)

    

    size = len(board)
    my_color = 'l'

    d.draw(board, "start.png")

    State0 = MCTS_state(board)
    root = MonteCarloTreeSearchNode(State0, my_color)
    # possible_actions = root.state.get_legal_actions()
    # print("result", root.minimax(root.state, possible_actions, 'l'))
    # print(root.rollout())
    # next_one = root._tree_policy()
    # print(next_one.state.board)
    # print(next_one.rollout())
    # sys.exit()

    selected_node = root.best_action(1)

    for child in root.children:
        action = child.parent_action
        result = child._results
        visited = child._number_of_visits
        # d.draw(child.state.board,
        #    f"{action} wins {result[1]} loses {result[-1]} draws {result[0]} visited {visited}.png")

    print(selected_node.parent_action)
    # d.draw(selected_node.state.board, "best move.png")
    """
    # sys.exit()
    idx = 0
    while True:
        rmove = p1.move()

        print(p1.myColor, "is making a move", rmove)

        for move in rmove:
            row, col, tile = move
            p1.board[row][col] = tile
            p2.board[row][col] = tile

        d.draw(p1.board, f"move-{idx}, {p1.myColor}.png")
        idx += 1

        if len(rmove) == 0:
            break
        p1, p2 = p2, p1
