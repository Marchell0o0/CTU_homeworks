import draw as Drawer
import sys
import random
import copy
import base as Base
import time
import math
from collections import deque

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
        # print(*node.state.board, sep='\n')
        # print(actions)
        # print(node.children.keys())
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

class treeNode_BFS():
    def __init__(self, state, parent, action, depth):
        self.state = state
        self.isTerminal = state.isTerminal()
        self.parent = parent
        self.action = action 
        self.depth = depth



class BFS():
    def __init__(self, timeLimit=None):
        if timeLimit == None:
            raise ValueError("there should be a time limit")
        else:
            self.timeLimit = timeLimit
            self.limitType = 'time'
        


    def search(self, initialState):
        root = treeNode_BFS(initialState, None, None, 0)
        timeLimit = time.time() + self.timeLimit / 1000
        closest_winning = []
        closest_loosing = []
        queue = [root]
        tried_already = set()
        while queue and time.time() < timeLimit:
            current_node = queue.pop(0)
            tried_already.add(str(current_node.state.board))
            newNodes = self.expand(current_node)
            for newNode in newNodes:
                # print(newNode.state.cycles_lines(newNode.state.board)[0])
                # print(newNode.depth)
                # d.draw(newNode.state.board, f"{newNode.depth, newNode.action}.png")
                if newNode.isTerminal:

                    # print("is terminal ")
                    win = newNode.state.getReward()
                    if win == 1 and not closest_winning:
                        closest_winning = [newNode, newNode.depth]
                    elif win == 0 and not closest_loosing:
                        closest_loosing = [newNode, newNode.depth]
                    elif win == 0.5:
                        continue
                else:
                    if str(newNode.state.board) not in tried_already:
                        queue.append(newNode)
            if closest_loosing and closest_winning:
                # print("nearest loosing move", closest_loosing[1], "nearest winning move",closest_winning[1])
                if closest_loosing[1] >= closest_winning[1]:
                    temp = closest_winning[0]
                    while temp.depth != 1:
                        temp = temp.parent
                    return temp.action
                else:
                    temp = closest_loosing[0]
                    while temp.depth != 1:
                        temp = temp.parent
                    avoid = temp.action
                    # print(avoid)
                    r_temp, c_temp, tile_temp = avoid[0]
                    if tile_temp == "lddl":
                        # print("chose best")
                        best = initialState.get_a_move(r_temp, c_temp, "ldld")
                        if best:
                            return best
                        best = initialState.get_a_move(r_temp, c_temp, "ddll")
                        if best:
                            return best
                        if best:
                            best = initialState.get_a_move(r_temp, c_temp, "lldd")
                            return best
                    if tile_temp == "lldd":
                        # print("chose best")
                        best = initialState.get_a_move(r_temp, c_temp, "dlld")
                        if best:
                            return best
                        best = initialState.get_a_move(r_temp, c_temp, "ldld")
                        if best:
                            return best
                    # print()
                    # print("returning the worst action")
                    # print()
                    return avoid
        return []

    def expand(self, node): 
        newNodes = []
        actions = node.state.getPossibleActions()
        if actions:
            for action in actions:
                newNode = treeNode_BFS(node.state.takeAction(action), node, action, node.depth+1)
                newNodes.append(newNode)
            return newNodes
        else:
            raise ValueError("expansion of terminal state")

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

class Player(Base.BasePlayer):
    def __init__(self, board, name, color):
        Base.BasePlayer.__init__(self,board, name, color)        
        self.algorithmName = "My great player"

    def move(self):
        board_temp = tuple(map(tuple, self.board))
        State0 = game_state(board_temp, self.myColor)
        rmove = []
        if not State0.isTerminal():
            # print("using BFS")
            BFS_tree = BFS(timeLimit=950)
            action = BFS_tree.search(initialState=State0)
            if action:
                for move in action:
                    r, c, tile = move
                    rmove.append([r,c,tile])
            else:
                # print("BFS could not make it")
                actions_brute = State0.getPossibleActions()
                if actions_brute:
                    action_brute = random.choice(actions_brute)
                    for move in action_brute:
                        r, c, tile = move
                        rmove.append([r,c,tile])
                else:
                    return []
        else:
            # print("game is done, using brute")
            actions_brute = State0.getPossibleActions()
            if actions_brute:
                action_brute = random.choice(actions_brute)
                for move in action_brute:
                    r, c, tile = move
                    rmove.append([r,c,tile])
            else:
                # print("board is full")
                return []
        return rmove
        
        """
        board_temp = tuple(map(tuple, self.board))
        State0 = game_state(board_temp, self.myColor)
        rmove = []
        if not State0.isTerminal():
            print("using mcts")
            mcts_tree = mcts(timeLimit=800)
            action = mcts_tree.search(initialState=State0)
            for move in action:
                r, c, tile = move
                rmove.append([r,c,tile])
        else:
            print("using brute")
            actions_brute = State0.getPossibleActions()
            if actions_brute:
                action_brute = random.choice(actions_brute)
                for move in action_brute:
                    r, c, tile = move
                    rmove.append([r,c,tile])
            else:
                return []
        return rmove
        """

class game_state:
    def __init__(self, board, player_color) -> None:
        self.board = board
        self.player_color = player_color


    def inside(self, r, c, where):
        return 0 <= r < len(where) and 0 <= c < len(where[0])



    def getPossibleActions(self):
        board = self.board
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
                move = self.get_a_move(edge[0], edge[1], tile)
                if move:
                    res.append(tuple(move))
        return res

    def get_a_move(self, r, c, tile):
        temp_board = self.board
        res = []
        if self.isLegal(r, c, tile):

            queue = deque([(r, c, tile)])
            res.append((r, c, tile))

            while queue:
                r_temp, c_temp, tile_temp = queue.popleft()
                # print("current tile",r_temp, c_temp, tile_temp)
                temp_board = temp_board[:r_temp] + ((temp_board[r_temp][:c_temp] + (tile_temp,) +temp_board[r_temp][c_temp+1:]),) + temp_board[ r_temp + 1:]

                for idx, shift in enumerate(shifts):
                    r_shift = shift[0] + r_temp
                    c_shift = shift[1] + c_temp
                    color_of_main_tile = tile_temp[idx]
                    if self.inside(r_shift, c_shift, temp_board) and temp_board[r_shift][c_shift] == 'none':
                        # print("current shift tile", r_shift, c_shift)
                        colors_of_checked_tiles = ['','','']
                        for i, item in enumerate([shifts   [indexes[(idx + 3) % 4] [0]], shifts  [indexes[(idx + 3) % 4] [1]],  shifts   [indexes[(idx + 3) % 4] [2] ]]):
                        # print("this is a possible shift tile", r_shift, c_shift, "direction", shift, idx)
                            r_d, c_d = item
                            forced = False
                            r_d_shift = r_d + r_shift
                            c_d_shift = c_d + c_shift
                            if self.inside(r_d_shift, c_d_shift, temp_board) and temp_board[r_d_shift][c_d_shift] != 'none':
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
        temp_board = self.board

        for move in moves:
            r_temp, c_temp, tile_temp = move
            temp_board = temp_board[:r_temp] + ((temp_board[r_temp][:c_temp] + (tile_temp,) +temp_board[r_temp][c_temp+1:]),) + temp_board[ r_temp + 1:]

        return game_state(temp_board, self.player_color)



    def cycles_lines(self, board):
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
                                if (self.inside(r_temp + dr, c_temp + dc, board) and
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
                                    self.inside(r_temp + dr, c_temp + dc, board)
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
                                    self.inside(r_temp + dr, c_temp + dc, board)
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
        if (self.player_color == "l" and winner == "d") or (self.player_color == "d" and winner == "l"):
            return 0  
        elif (self.player_color == "l" and winner == "l") or (self.player_color == "d" and winner == "d"):
            return 1
        elif winner is None:
            return 0.5 

if __name__ == "__main__":
    boardRows = 10
    boardCols = boardRows
    board = [ ["none"]*boardCols for _ in range(boardRows) ]

    board[boardRows//2][boardCols//2] = ["lldd","dlld","ddll","lddl","dldl","ldld"][ random.randint(0,5) ]


    board = [
        ['none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'ldld', 'none', 'none', 'none'],
        ['none', 'none', 'dldl', 'ddll', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none', 'none'],
        ['none', 'none', 'none', 'none', 'none', 'none', 'none']
        ]

    board_test = [
        ['lddl', 'dldl', 'dlld', 'lldd', 'dldl', 'dldl', 'ddll'],
        ['lldd', 'dlld', 'ldld', 'lddl', 'dldl', 'dlld', 'lldd'],
        ['none', 'none', 'lddl', 'dldl', 'dldl', 'ddll', 'lddl'],
        ['none', 'none', 'lldd', 'dldl', 'dlld', 'lldd', 'dldl'],
        ['lldd', 'ddll', 'lddl', 'dlld', 'ldld', 'lddl', 'dlld'],
        ['lddl', 'dldl', 'dlld', 'ldld', 'lddl', 'dlld', 'ldld'],
        ['none', 'dldl', 'ddll', 'lddl', 'dlld', 'lddl', 'ddll']
        ]


    board_test = tuple(map(tuple, board_test))
    State0 = game_state(board_test, "l")
    print(*State0.getPossibleActions(), sep='\n')
    sys.exit()
    d = Drawer.Drawer()

    p1 = Player(board,"player1", 'l')
    p2 = Player(board,"player2", 'd')
    '''

    BFS_tree = BFS(timeLimit = 800)
    root = treeNode_BFS(State0, None, None, 0)
    expansion = BFS_tree.expand(root)
    for action, node in root.children.items():
        d.draw(node.state.board, f"{action, node.state.cycles_lines(node.state.board)[0]}.png")
        # print(action, node.state.cycles_lines(node.state.board)[0])
    # for exp in expansion:
        print(*exp.state.board, sep='\n')
        print()
    
    board_test = tuple(map(tuple, board_test))

    State0 = game_state(board_test, 'l')
    start = time.perf_counter()
    PA = State0.getPossibleActions()
    end = time.perf_counter()
    # print("time for possible moves", end - start)
    # print(*PA, sep='\n')
    rmove = []
    for move in PA[0]:
        r, c, tile = move
        rmove.append([r, c, tile])
    # print("making this move", rmove)
    start = time.perf_counter()
    next_state = State0.takeAction(PA[0])
    end = time.perf_counter()
    # print("time for making a move", end - start)
    # print(*next_state.board, sep='\n')
    # '''

    idx = 0
    while True:
    # for _ in range(10):
        # print(*p1.board,sep='\n')
        # print()
        # print(p1.myColor, "is making a move")
        rmove = p1.move()
        # print(rmove)
        # sys.exit()
        for move in rmove:
            row,col, tile = move
            p1.board[row][col] = tile
            p2.board[row][col] = tile
        # d.draw(p1.board, "move-{:04d}.png".format(idx))
        idx+=1
        if len(rmove) == 0:
            break
        p1,p2 = p2,p1  #switch players




