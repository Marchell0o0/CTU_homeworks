import draw as Drawer
import sys
import random
import copy
import base as Base
import math
import time
from collections import deque
import numpy as np



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


class mcts():
    def __init__(self, timeLimit=None, iterationLimit=None, explorationConstant= 1.41421356237,
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

        bestChild = self.getBestChild(self.root,  1.41421356237)
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





class Player(Base.BasePlayer):
    def __init__(self, board, name, color):
        Base.BasePlayer.__init__(self,board, name, color)        
        self.algorithmName = "My great player"

    def move(self):
        board_temp = np.array(self.board)
        State0 = game_state(board_temp, self.myColor)
        rmove = []
        if not State0.isTerminal():
            # print("using mcts")
            mcts_tree = mcts(timeLimit=900)
            action = mcts_tree.search(initialState=State0)
            for move in action:
                r, c, tile = move
                rmove.append([r,c,tile])
            return rmove
        else:
            return []

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

shifts = {
    (0, -1, 0): ((1,0,1),(0,-1,2),(-1,0,3)),
    (-1,0,1): ((0,-1,2),(-1,0,3),(0,1,0)),
    (0,1,2): ((-1,0,3),(0,1,0),(1,0,1)),
    (1,0,3): ((0,1,0),(1,0,1),(0,-1,2)),

}
# class game_state:

class game_state:    
    def __init__(self, board, current_player):
        self.board = board
        self.current_player = current_player


    def inside(self, r, c):
        return 0 <= r < len(self.board) and 0 <= c < len(self.board[0])

    def getPossibleActions(self):
        board = self.board
        res = []
        edge_tiles = set()
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] != 'none':
                    if r > 0 and board[r-1][c] == 'none':
                        edge_tiles.add((r-1, c))
                    if r < len(board) - 1 and board[r+1][c] == 'none':
                        edge_tiles.add((r+1, c))
                    if c > 0 and board[r][c-1] == 'none':
                        edge_tiles.add((r, c - 1))
                    if c < len(board[0]) - 1 and board[r][c+1] == 'none':
                        edge_tiles.add((r, c + 1))
        for edge in edge_tiles:
            for tile in tiles:
                move = self.get_a_move(edge[0], edge[1], tile)
                if move and move not in res:
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
                    if self.inside(r_shift, c_shift) and temp_board[r_shift][c_shift] == 'none':
                        for i in range(3):
                            r_d, c_d, color = shifts[shift][i]
                            r_d_shift = r_d + r_shift
                            c_d_shift = c_d + c_shift
                            if self.inside(r_d_shift, c_d_shift):
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
            (r == 0 or board[r - 1][c] == "none" or board[r - 1][c][3] == tile[1])
            and (c == len(board[0]) - 1 or board[r][c + 1] == "none" or board[r][c + 1][0] == tile[2])
            and (r == len(board) - 1 or board[r + 1][c] == "none" or board[r + 1][c][1] == tile[3])
            and (c == 0 or board[r][c - 1] == "none" or board[r][c - 1][2] == tile[0])
        ):
            return True
        else:
            return False
        

    def takeAction(self, moves):
        temp_board = self.board.copy()

        for move in moves:
            r_temp, c_temp, tile_temp = move
            temp_board[r_temp][c_temp] = tile_temp

        if self.current_player == "d":
            return game_state(temp_board, "l")
        else:
            return game_state(temp_board, "d")


    def cycles_lines(self):
        board = self.board
        result = {"light":0, "dark":0}
        lines = 0
        cycles = {"light":0, "dark":0}
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
                            for dr, dc, pos1, pos2 in directions:
                                if (self.inside(r_temp + dr, c_temp + dc) and
                                    board[r_temp][c_temp][pos1] == color[0] and
                                    board[r_temp + dr][c_temp + dc][pos2] == color[0]
                                ):
                                    if (r_temp + dr, c_temp + dc) == start and length > 3:
                                        result[color] += length
                                        cycles[color] += 1
                                        break 
                                    if (r_temp + dr, c_temp + dc) not in tried_already:
                                        queue.append((r_temp + dr, c_temp + dc))
                                        length += 1
                                        break
            tried_already = set()
            for r in range(len(board)):
                if board[r][0][0] == color[0]:
                    queue = [(r, 0)]
                    length = 1
                    while queue:
                        r_temp, c_temp = queue.pop(0)
                        tried_already.add((r_temp, c_temp))
                        if c_temp == len(board[0])-1 and board[r_temp][c_temp][2] == color[0]:
                                result[color] += length
                                lines += 1
                                break
                        for dr, dc, pos1, pos2 in directions:
                                if (
                                    self.inside(r_temp + dr, c_temp + dc)
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
                    queue = [(0, c)]
                    length = 1
                    while queue:
                        r_temp, c_temp = queue.pop(0)
                        tried_already.add((r_temp, c_temp))
                        if r_temp == len(board)-1 and board[r_temp][c_temp][3] == color[0]:
                                result[color] += length
                                lines += 1
                                break
                        for dr, dc, pos1, pos2 in directions:
                                if (
                                    self.inside(r_temp + dr, c_temp + dc)
                                    and board[r_temp][c_temp][pos1] == color[0]
                                    and board[r_temp + dr][c_temp + dc][pos2] == color[0]
                                    and (r_temp + dr, c_temp + dc) not in tried_already
                                ):
                                    queue.append((r_temp + dr, c_temp + dc))
                                    length += 1
                                    break
        return result, cycles, lines
   

    def isTerminal(self):
        stats = self.cycles_lines()[0]
        return stats["light"] != 0 or stats["dark"] != 0 or not self.getPossibleActions() 

    # (not any('none' in i for i  in self.board))

    def getReward(self):
        stats = self.cycles_lines()[0]
        # cycles = stats[1]
        # lines = stats[2]
        # if (stats[0]['light'] != 0) and (stats[0]['dark'] != 0):
        #     if lines >= 2 or (cycles['light'] == 0 and cycles['dark'] == 0):
        #         if self.player_color == 'l':
        #             if stats[0]["light"]*2 > stats[0]["dark"]:
        #                 winner = "l"
        #             elif stats[0]["light"]*2 < stats[0]["dark"]:
        #                 winner = "d"
        #             else:
        #                 winner = None
        #         if self.player_color == 'd':
        #             if stats[0]["light"] > stats[0]["dark"]*2:
        #                 winner = "l"
        #             elif stats[0]["light"]*2 < stats[0]["dark"]*2:
        #                 winner = "d"
        #             else:
        #                 winner = None
        #     else:
        #         if stats[0]["light"] > stats[0]["dark"]:
        #             winner = "l"
        #         elif stats[0]["light"] < stats[0]["dark"]:
        #             winner = "d"
        #         else:
        #             winner = None
        # elif (stats[0]['light'] != 0) or (stats[0]['dark'] != 0):
        #     if stats[0]["light"] > stats[0]["dark"]:
        #         winner = "l"
        #     elif stats[0]["light"] < stats[0]["dark"]:
        #         winner = "d"
        # else:
        #     winner = None
        if stats["light"] > stats["dark"]:
            winner = "l"
        elif stats["light"] < stats["dark"]:
            winner = "d"
        else:
            winner = None
        if (self.current_player == "l" and winner == "d") or (self.current_player == "d" and winner == "l"):
            return -1 
        elif (self.current_player == "l" and winner == "l") or (self.current_player == "d" and winner == "d"):
            return 1
        elif winner is None:
            return 0



if __name__ == "__main__":
    """
    boardRows = 10
    boardCols = boardRows
    board = [ ["none"]*boardCols for _ in range(boardRows) ]
    board[boardRows//2][boardCols//2] = ["lldd","dlld","ddll","lddl","dldl","ldld"][ random.randint(0,5) ]
    """

    d = Drawer.Drawer()
    
    """
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
    State_test = game_state(board_get_action_test, "l")
    start = time.perf_counter()
    moves = State_test.getPossibleActions()
    end = time.perf_counter()
    print("time of a possible moves func", end - start)
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

    """



    board = [
        ['none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'lldd', 'dlld', 'none', 'none', 'none'],
        ['none', 'none', 'lddl', 'ddll', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none', 'none']
        ]

    d.draw(board, "PIZDA.png")
    sys.exit()
    State_test = game_state(board, "d")
    print(State_test.getReward())
    p1 = Player(board,"player1", 'l')
    p2 = Player(board,"player2", 'd')

    # sys.exit()
    idx = 0
    while True:
        print(f"{p1.myColor} is making a move")

        start = time.perf_counter()
        rmove = p1.move()
        end = time.perf_counter()
        print(rmove)
        print(f"{idx}, move took: {end - start}")
        # sys.exit()


        for move in rmove:
            row,col, tile = move
            p1.board[row][col] = tile
            p2.board[row][col] = tile

        d.draw(p1.board, "move-{:04d}.png".format(idx))
        idx+=1

        if len(rmove) == 0:
            break
        p1,p2 = p2,p1 



