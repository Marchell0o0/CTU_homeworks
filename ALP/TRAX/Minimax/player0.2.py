
import draw as Drawer
import sys
import random
import copy
import base as Base

from collections import defaultdict, namedtuple
import math
from random import choice
from abc import abstractmethod, ABC


class MCTS:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."

    def __init__(self, player_color, exploration_weight=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight
        self.player_color = player_color

    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        
        """Didnt find that move"""
        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        return max(self.children[node], key=score)

    def do_rollout(self, node):
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children(node)

    def _simulate(self, node):
        "Returns the reward for a random simulation (to completion) of `node`"
        while True:
            # if node.is_terminal(node):
            if node.terminal:
                return node.reward(self.player_color)
            node = node.find_random_child(node)

    def _backpropagate(self, path, reward):
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)



class Node(ABC):
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.
    """

    @abstractmethod
    def find_children(self):
        "All possible successors of this board state"
        return set()

    @abstractmethod
    def find_random_child(self):
        "Random successor of this board state (for more efficient simulation)"
        return None

    @abstractmethod
    def is_terminal(self):
        "Returns True if the node has no children"
        return True

    @abstractmethod
    def reward(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        return 0

    @abstractmethod
    def __hash__(self):
        "Nodes must be hashable"
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):
        "Nodes must be comparable"
        return True

lookup_forced_moves = {
        'l1': 'lddl',
        'l2': 'dldl',
        'l3': 'ddll',
        'l4': 'lldd',
        'l5': 'ldld',
        'l6': 'lddl',
        'l7': 'dlld',
        'l8': 'dldl',
        'l9': 'lldd',
        'l10': 'ddll',
        'l11': 'ldld',
        'l12': 'dlld',
        'd1': 'dlld',
        'd2': 'ldld',
        'd3': 'lldd',
        'd4': 'ddll',
        'd5': 'dldl',
        'd6': 'dlld',
        'd7': 'lddl',
        'd8': 'ldld',
        'd9': 'ddll',
        'd10': 'lldd',
        'd11': 'dldl',
        'd12': 'lddl'
    }

lookup_closing_lines = {
    ('lr', 'light', 'ldld'): True,
    ('lr', 'light', 'ddll'): True,
    ('lr', 'light', 'dlld'): True,
    ('lr', 'light', 'dldl'): False,
    ('lr', 'light', 'lddl'): False,
    ('lr', 'light', 'lldd'): False,
    ('lr', 'dark', 'ldld'): False,
    ('lr', 'dark', 'ddll'): False,
    ('lr', 'dark', 'dlld'): False,
    ('lr', 'dark', 'dldl'): True,
    ('lr', 'dark', 'lddl'): True,
    ('lr', 'dark', 'lldd'): True,
    ('td', 'light', 'ldld'): False,
    ('td', 'light', 'ddll'): True,
    ('td', 'light', 'dlld'): False,
    ('td', 'light', 'dldl'): True,
    ('td', 'light', 'lddl'): True,
    ('td', 'light', 'lldd'): False,
    ('td', 'dark', 'ldld'): True,
    ('td', 'dark', 'ddll'): False,
    ('td', 'dark', 'dlld'): True,
    ('td', 'dark', 'dldl'): False,
    ('td', 'dark', 'lddl'): False,
    ('td', 'dark', 'lldd'): True
    }

tiles = ["lldd", "dlld", "ddll", "lddl", "dldl", "ldld"]

T_B = namedtuple("Trax_board", "tup winner terminal")


class State_of_a_game(T_B, Node):
    """
    A representation of a single board state.
    MCTS works by constructing a tree of these Nodes.
    Could be e.g. a chess or checkers board state.
    """

    def find_children(self, board_state):
        if board_state.terminal:  # If the game is finished then no moves can be made
            return set()



        res = set()
        board = board_state.tup
        Available_moves = self.AM(board)

        for move in Available_moves:
            res.add(self.make_a_move(move[0], move[1], board))

        return res 

    def find_random_child(self, board_state):
        "Random successor of this board_state state (for more efficient simulation)"


        if board_state.terminal:
            return None  # If the game is finished then no moves can be made

        board = board_state.tup
        Available_moves = self.AM(board)
        move = choice(Available_moves)

        return self.make_a_move(move[0], move[1], board)

    def inside(self, r, c, where):
        return 0 <= r < len(where) and 0 <= c < len(where[0])

    def AM(self, board):
        edge_tiles = []
        res = []
        # board = board_state.tup
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] != 'none':
                    if r > 0 and board[r-1][c] == 'none':
                        edge_tiles.append((r-1, c))
                    if r < len(board) - 1 and board[r+1][c] == 'none':
                        edge_tiles.append((r+1, c))
                    if c > 0 and board[r][c-1] == 'none':
                        edge_tiles.append((r, c - 1))
                    if c < len(board[0]) - 1 and board[r][c+1] == 'none':
                        edge_tiles.append((r, c + 1))
        for edge in edge_tiles:
            r = edge[0]
            c = edge[1]
            for tile in tiles:
                if (
                    (r == 0 or board[r - 1][c] == "none" or board[r - 1][c][3] == tile[1])
                    and (c == len(board[0]) - 1 or board[r][c + 1] == "none" or board[r][c + 1][0] == tile[2])
                    and (r == len(board) - 1 or board[r + 1][c] == "none" or board[r + 1][c][1] == tile[3])
                    and (c == 0 or board[r][c - 1] == "none" or board[r][c - 1][2] == tile[0])
                    and board[r][c] == 'none'
                ):
                    res.append((tile, edge))
        return res

    def cycles_lines_move_through(self, r, c, board, start, length, color, direction, mode, lookup, tried_already, res):
        if mode == "cycles":
            if [r, c] == start and length > 3:
                res.append(length)
                return True
        if mode == "lines":
            if (c == len(board) - 1 and direction == "lr") or (
                r == len(board) - 1 and direction == "td"
            ):
                if lookup[(direction, color, board[r][c])]:
                    res.append(length+1)
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
                self.inside(r + dr, c + dc, board)
                and board[r][c][pos1] == color[0]
                and board[r + dr][c + dc][pos2] == color[0]
                and str([r + dr, c + dc]) not in tried_already
            ):
                tried_already.add(str([r + dr, c + dc]))
                self.cycles_lines_move_through(r + dr, c + dc, board, start, length, color, direction, mode, lookup, tried_already, res)
                break
        else:
            return False

    def cycles_lines(self, board):
        tried_already = set()
        result = {"light":0, "dark":0}
        for color in ["light", "dark"]:
            res = []
            tried_already = set()
            for r in range(len(board)):
                for c in range(len(board[0])):
                    if str([r, c]) not in tried_already:
                        self.cycles_lines_move_through(r, c, board, [r, c], 0, color, "nn", "cycles", lookup_closing_lines, tried_already, res)
                        tried_already.add(str([r, c]))
            result[color] += sum(res)
        for color in ["light", "dark"]:
            res = []    
            for direction in ["td", "lr"]:
                tried_already = set()
                if direction == "lr":
                    for r in range(len(board)):
                        if str([r, 0]) not in tried_already and  board[r][0][0] == color[0]:
                            self.cycles_lines_move_through(r, 0, board, 0, 0, color, direction, "lines", lookup_closing_lines, tried_already, res)
                            tried_already.add(str([r, 0]))
                else:
                    for c in range(len(board[0])):
                        if str([0, c]) not in tried_already and  board[0][c][1] == color[0]:
                            self.cycles_lines_move_through(0, c, board, 0, 0, color, direction, "lines", lookup_closing_lines, tried_already, res)
                            tried_already.add(str([0, c]))
            result[color] += sum(res)
        if result['light'] > result['dark']:
            return "l"
        elif result['dark'] > result['light']:
            return "d"
        else:
            return None

    def make_a_move(self, what, where, board):
        moves = []
        # temp_board = copy.deepcopy(board_state) 
        temp_board = board
        queue = [[what, where]]
        while queue:
            move = queue.pop()
            r = move[1][0]
            c = move[1][1]
            tile = move[0]
            temp_board = temp_board[:r] + ((temp_board[r][:c] + (tile,) +temp_board[r][c+1:]),) + temp_board[ r + 1:]
            moves.append([tile, [r, c]])
            for idx, item in enumerate(
                (
                (1, 2, -1, 0, -1, -1),
                (1, 3, -1, 0, -2, 0),
                (1, 0, -1, 0, -1, 1),
                (2, 3, 0, 1, -1, 1),
                (2, 0, 0 , 1, 0, 2),
                (2, 1, 0, 1, 1, 1),
                (3, 0, 1, 0, 1, 1),
                (3, 1, 1, 0, 2, 0),
                (3, 2, 1, 0, 1, -1),
                (0, 1, 0, -1, 1, -1),
                (0, 2, 0, -1, 0, -2),
                (0, 3, 0, -1,-1, -1)
                )
                ):
                main_side_color, temp_side_color, r_offset_main, c_offset_main, r_offset, c_offset = item
                if (
                    self.inside(r + r_offset, c + c_offset, temp_board)
                    and temp_board[r + r_offset_main][c + c_offset_main] == "none"
                    and temp_board[r + r_offset][c + c_offset][temp_side_color] == tile[main_side_color]
                ):
                    forced_move = [lookup_forced_moves[tile[main_side_color] +  str(idx + 1)], [r + r_offset_main, c + c_offset_main]]
                    queue.append(forced_move)

        winner = self.cycles_lines(temp_board)
        is_terminal = (winner is not None) or not any('none' in i for i  in temp_board)
        return T_B(temp_board, winner, is_terminal)

    def is_terminal(self, board_state):
        "Returns True if the node has no children"
        return board_state.terminal

    def reward(self, board_state, player_color):
        if not board_state.terminal:
            raise RuntimeError(f"reward called on nonterminal board_state {board_state}")
        if board_state.winner is board_state.turn:
            # It's your turn and you've already won. Should be impossible.
            raise RuntimeError(f"reward called on unreachable board_state {board_state}")



        if player_color == "l" and board_state.winner == "d" or player_color == "d" and board_state.winner == "l":
            return 0  # Your opponent has just won. Bad.
        if player_color == "l" and board_state.winner == "l" or player_color == "d" and board_state.winner == "d":
            return 1
        if board_state.winner is None:
            return 0.5  # Board is a tie
        

        # The winner is neither True, False, nor None
        raise RuntimeError(f"board_state has unknown winner type {board_state.winner}")

    def __hash__(self):
        "Nodes must be hashable"
        return 123456789

    def __eq__(node1, node2):
        "Nodes must be comparable"
        return True







class Player(Base.BasePlayer):
    def __init__(self, board, name, color):
        Base.BasePlayer.__init__(self,board, name, color)        
        self.algorithmName = "My great player"



def play_a_move(board, player_color):
    tree = MCTS(player_color)
    State0 = State_of_a_game(tup = board, winner = None, terminal = False )
    # You can train as you go, or only at the beginning.
    # Here, we train as we go, doing fifty rollouts each turn.
    for _ in range(50):
        tree.do_rollout(State0)
    moves = tree.choose(State0).moves
    return moves


if __name__ == "__main__":


    """
    boardRows = 10
    boardCols = boardRows
    board = [ ["none"]*boardCols for _ in range(boardRows) ]

    board[boardRows//2][boardCols//2] = ["lldd","dlld","ddll","lddl","dldl","ldld"][ random.randint(0,5) ]
    # """

    board = [
        ["none", "none","none"],
        ["dlld", "ldld","lldd"],
        ["none", "none","none"],
    ]

    d = Drawer.Drawer()

    p1 = Player(board,"player1", 'l'); 
    p2 = Player(board,"player2", 'd');
    
    board_tuple = tuple(map(tuple, p1.board))
    print(*board_tuple, sep='\n')

    State0 = State_of_a_game(board_tuple, None, False)
    print(State0.make_a_move("ldld", [0, 1], board_tuple))
    print(State0.AM(board_tuple))

    
    rmove = play_a_move(board_tuple, p1.myColor)

    sys.exit()
    idx = 0
    while True:


        for move in rmove:
            row,col, tile = move
            p1.board[row][col] = tile
            p2.board[row][col] = tile

        #make png with resulting board
        d.draw(p1.board, "move-{:04d}.png".format(idx))
        idx+=1

        if len(rmove) == 0:
            print("End of game")
            break
        p1,p2 = p2,p1  #switch players




