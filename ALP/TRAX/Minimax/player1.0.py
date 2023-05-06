
from __future__ import division

import draw as Drawer
import sys
import random
import copy
import base as Base
import time
import math


def randomPolicy(state):
    while not state.isTerminal():
        try:
            action = random.choice(state.getPossibleActions())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)
    return state.getReward()


class treeNode():
    def __init__(self, state, parent):
        self.state = state
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = self.isTerminal
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}

"""1 / math.sqrt(2):[13.35],   1.41421356237:[17.2, 12.6, 17.9]   3:[15.2 ]""" 
"""(exploration value =  1.41421356237)1 / math.sqrt(2):[],   1.41421356237:[17.25, 16.35, 14.75],   2:[18.4, 14.7, 15.6],  3:[14.15]""" 

class mcts():
    def __init__(self, timeLimit=None, iterationLimit=None, explorationConstant = 3,
                 rolloutPolicy=randomPolicy):
        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy

    def search(self, initialState):
        self.root = treeNode(initialState, None)

        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
        else:
            for i in range(self.searchLimit):
                self.executeRound()

        bestChild = self.getBestChild(self.root, self.explorationConstant)
        return self.getAction(self.root, bestChild)

    def executeRound(self):
        node = self.selectNode(self.root)
        reward = self.rollout(node.state)
        self.backpropogate(node, reward)

    def selectNode(self, node):
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.getPossibleActions()
        for action in actions:
            if action not in node.children.keys():
                newNode = treeNode(node.state.takeAction(action), node)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return newNode
        print(*node.state.board, sep='\n')
        print(actions)
        print(node.children.keys())
        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def getBestChild(self, node, explorationValue):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue = child.totalReward / child.numVisits + explorationValue * math.sqrt(
                2 * math.log(node.numVisits) / child.numVisits)
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)

    def getAction(self, root, bestChild):
        for action, node in root.children.items():
            if node is bestChild:
                return action








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

directions = [
    (0, 1, 2, 0),
    (1, 0, 3, 1),
    (0, -1, 0, 2),
    (-1, 0, 1, 3),
    ]

tiles = ["lldd", "dlld", "ddll", "lddl", "dldl", "ldld"]


class Player(Base.BasePlayer):
    def __init__(self, board, name, color):
        Base.BasePlayer.__init__(self,board, name, color)        
        self.algorithmName = "My great player"

class game_state:
    def __init__(self, board, player_color) -> None:
        self.board = board
        self.player_color = player_color

    def inside(self, r, c, where):
        return 0 <= r < len(where) and 0 <= c < len(where[0])

    def getPossibleActions(self):
        edge_tiles = []
        res = []
        board = self.board
        # print("getting possible moves from this board")
        # print(*self.board, sep='\n')

        # board = board_state.tup
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

    def takeAction(self, move):
        what, where = move
        temp_board = self.board
        queue = [[what, where]]
        while queue:
            move = queue.pop()
            r = move[1][0]
            c = move[1][1]
            tile = move[0]
            temp_board = temp_board[:r] + ((temp_board[r][:c] + (tile,) +temp_board[r][c+1:]),) + temp_board[ r + 1:]
            for idx, item in enumerate(
                (
                (1, 2,-1, 0,-1,-1),
                (1, 3,-1, 0,-2, 0),
                (1, 0,-1, 0,-1, 1),
                (2, 3, 0, 1,-1, 1),
                (2, 0, 0, 1, 0, 2),
                (2, 1, 0, 1, 1, 1),
                (3, 0, 1, 0, 1, 1),
                (3, 1, 1, 0, 2, 0),
                (3, 2, 1, 0, 1,-1),
                (0, 1, 0,-1, 1,-1),
                (0, 2, 0,-1, 0,-2),
                (0, 3, 0,-1,-1,-1)
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
        return game_state(temp_board, self.player_color)

    def cycles_lines(self, board):
        result = {"light":0, "dark":0}
        lines = 0
        cycles = {"light":0, "dark":0}
        # lines =  {"light":[], "dark":[]}
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
                                        cycles[color] += 1
                                        # cycles[color].append(length)
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
                                lines += 1
                                # lines[color].append(length)
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
                                lines += 1
                                # lines[color].append(length)
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

    
    def isTerminal(self):
        stats = self.cycles_lines(self.board)[0]
        return stats["light"] != 0 or stats["dark"] != 0 or (not any('none' in i for i  in self.board))

    def getReward(self):
        stats = self.cycles_lines(self.board)
        cycles = stats[1]
        lines = stats[2]
        if (stats[0]['light'] != 0) and (stats[0]['dark'] != 0):
            if lines >= 2 or (cycles['light'] == 0 and cycles['dark'] == 0):
                if self.player_color == 'l':
                    if stats[0]["light"]*2 > stats[0]["dark"]:
                        winner = "l"
                    elif stats[0]["light"]*2 < stats[0]["dark"]:
                        winner = "d"
                    else:
                        winner = None
                if self.player_color == 'd':
                    if stats[0]["light"] > stats[0]["dark"]*2:
                        winner = "l"
                    elif stats[0]["light"]*2 < stats[0]["dark"]*2:
                        winner = "d"
                    else:
                        winner = None
            else:
                if stats[0]["light"] > stats[0]["dark"]:
                    winner = "l"
                elif stats[0]["light"] < stats[0]["dark"]:
                    winner = "d"
                else:
                    winner = None
        elif (stats[0]['light'] != 0) or (stats[0]['dark'] != 0):
            if stats[0]["light"] > stats[0]["dark"]:
                winner = "l"
            elif stats[0]["light"] < stats[0]["dark"]:
                winner = "d"
        else:
            winner = None



       

        # if stats['dark'] > stats['light']:
        #     winner = "d"
        # elif stats['dark'] < stats['light']:
        #     winner = "l"
        # else:
        #     winner = None

        if (self.player_color == "l" and winner == "d") or (self.player_color == "d" and winner == "l"):
            return 0  # Your opponent has just won. Bad.
        elif (self.player_color == "l" and winner == "l") or (self.player_color == "d" and winner == "d"):
            return 1
        elif winner is None:
            return 0.5  # Board is a tie


def inside(r, c, where):
        return 0 <= r < len(where) and 0 <= c < len(where[0])

def get_moves_for_action(action, board):
    what, where = action
    temp_board = board
    moves = []
    queue = [[what, where]]
    while queue:
        move = queue.pop()
        r = move[1][0]
        c = move[1][1]
        tile = move[0]
        temp_board = temp_board[:r] + ((temp_board[r][:c] + (tile,) +temp_board[r][c+1:]),) + temp_board[ r + 1:]
        moves.append([r, c, tile])
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
                inside(r + r_offset, c + c_offset, temp_board)
                and temp_board[r + r_offset_main][c + c_offset_main] == "none"
                and temp_board[r + r_offset][c + c_offset][temp_side_color] == tile[main_side_color]
            ):
                forced_move = [lookup_forced_moves[tile[main_side_color] +  str(idx + 1)], [r + r_offset_main, c + c_offset_main]]
                queue.append(forced_move)
    return moves

if __name__ == "__main__":
    # average_moves = 0
    # for i in range(20):
    # """
    boardRows = 10
    boardCols = boardRows
    board = [ ["none"]*boardCols for _ in range(boardRows) ]

    board[boardRows//2][boardCols//2] = ["lldd","dlld","ddll","lddl","dldl","ldld"][ random.randint(0,5) ]
    # """

    # board_test = [
    #     ["none", "none","none"],
    #     ["dlld", "ldld","lldd"],
    #     ["none", "none","none"],
    # ]

    d = Drawer.Drawer()

    p1 = Player(board,"player1", 'l')
    p2 = Player(board,"player2", 'd')
    
    

    idx = 0
    while True:


        board_temp = tuple(map(tuple, p1.board))



        State0 = game_state(board_temp, p1.myColor)
        if State0.isTerminal():
            actions_brute = State0.getPossibleActions()
            if actions_brute:
                action_brute = random.choice(actions_brute)
                rmove = get_moves_for_action(action_brute, board_temp)
            else:
                rmove = []
            # print(f"game: {i}, loser: {p1.myColor}, on this move: {idx}, with this stats: {State0.cycles_lines(board_temp)}")
            # d.draw(board_temp, f"{i} game ending.png")
            # average_moves += idx
        else:
            mcts_tree = mcts(timeLimit=800)
            action = mcts_tree.search(initialState=State0)
            rmove = get_moves_for_action(action, board_temp)


        # if p1.myColor == "l":
        #     print("light is making a move")
        # else:
        #     print("dark is making a move")
        # print(rmove)

        for move in rmove:
            row,col, tile = move
            p1.board[row][col] = tile
            p2.board[row][col] = tile
        d.draw(p1.board, "move-{:04d}.png".format(idx))
        idx+=1

        if len(rmove) == 0:
            # print("End of game")
            break
        p1,p2 = p2,p1  #switch players
    # print(f"average amount of moves is {average_moves/20}")




