import draw as Drawer
import sys
import random
import copy
import base as Base

# implement you player here. If you need to define some classes, do it also here. Only this file is to be submitted to Brute.
# define all functions here

class State:
    def __init__(self, board, moves, depth, prev = None):
        self.board = board[:]
        self.moves = str(moves)
        self.depth = depth
        self.prev = prev

    tiles = ["lldd", "dlld", "ddll", "lddl", "dldl", "ldld"]

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

    def inside(self, r, c, where):
        return 0 <= r < len(where) and 0 <= c < len(where[0])

    def AS(self):
        ASlist = []
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if (
                    self.board[r][c] == "none"
                    and self.inside(r, c + 1, self.board)
                    and self.board[r][c + 1] != "none"
                ) or (self.board[r][c] == "none" and self.board[r][c - 1] != "none"):
                    ASlist.append([r, c])
        for c in range(len(self.board[0])):
            for r in range(len(self.board)):
                if (
                    self.board[r][c] == "none"
                    and self.inside(r + 1, c, self.board)
                    and self.board[r + 1][c] != "none"
                ) or (self.board[r][c] == "none" and self.board[r - 1][c] != "none"):
                    ASlist.append([r, c])
        return ASlist

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

    def cycles_lines(self):
        tried_already = set()
        result = {"light":0, "dark":0}
        for color in ["light", "dark"]:
            res = []
            tried_already = set()
            for r in range(len(self.board)):
                for c in range(len(self.board[0])):
                    if str([r, c]) not in tried_already:
                        self.cycles_lines_move_through(r, c, self.board, [r, c], 0, color, "nn", "cycles", self.lookup_closing_lines, tried_already, res)
                        tried_already.add(str([r, c]))
            result[color] += sum(res)
        for color in ["light", "dark"]:
            res = []    
            for direction in ["td", "lr"]:
                tried_already = set()
                if direction == "lr":
                    for r in range(len(self.board)):
                        if str([r, 0]) not in tried_already and  self.board[r][0][0] == color[0]:
                            self.cycles_lines_move_through(r, 0, self.board, 0, 0, color, direction, "lines", self.lookup_closing_lines, tried_already, res)
                            tried_already.add(str([r, 0]))
                else:
                    for c in range(len(self.board[0])):
                        if str([0, c]) not in tried_already and  self.board[0][c][1] == color[0]:
                            self.cycles_lines_move_through(0, c, self.board, 0, 0, color, direction, "lines", self.lookup_closing_lines, tried_already, res)
                            tried_already.add(str([0, c]))
            result[color] += sum(res)
        return result


class Player(Base.BasePlayer):
    def __init__(self, board, name, color):
        Base.BasePlayer.__init__(self, board, name, color)
        self.algorithmName = "My great player"

    def BFS_winning(self):
        State0 = State(self.board, [], 0)
        queue = [State0]
        tried_already = set()
        best_moves = []
        while queue:
            actual = queue.pop(0)
            tried_already.add(str(actual.board))
            newStates = actual.expand()
            for state in newStates:
                end = state.end()
                # print(*state.board, sep="\n")
                # print(end)
                # print()
                if end[1] is False and str(state.board) not in tried_already:
                    queue.append(state)
                elif end[1] is True and ((self.myColor == "l" and (end[0]["light"] > end[0]["dark"])) or (self.myColor == "d" and (end[0]["dark"] > end[0]["light"]))):
                    best_moves.append(state)
                    # if len(best_moves) > :
        if best_moves:
            closest_win = best_moves[0]
            for move in best_moves:
                print(move.end())
                if move.depth < closest_win.depth:
                    closest_win = move
            temp = closest_win
            while temp.depth != 1:
                temp = temp.prev
                print(*temp.board,sep='\n')
            print(self.myColor, "is making a move")
            print(*closest_win.board, sep='\n')
            print(closest_win.end())
            print(temp.moves)
            return temp.moves
        else:
            return []
    
    
    def BFS_losing(self):
        State0 = State(self.board, [], 0)
        queue = [State0]
        tried_already = set()
        while queue:
            actual = queue.pop(0)
            tried_already.add(str(actual.board))
            newStates = actual.expand()
            for state in newStates:
                end = state.end()
                # print(*state.board, sep="\n")
                # print(end)
                # print()
                if end[1] is False and str(state.board) not in tried_already:
                    queue.append(state)
                elif end[1] is True:
                    # if end[0]["light"] == 0 and end[0]["dark"] == 0:
                    #     temp = state
                    #     while temp.depth != 1:
                    #         temp = temp.prev
                    #     print(self.myColor, "ismaking a move")
                    #     print(state.end())
                    #     return temp.moves
                    if self.myColor == "d" and (end[0]["light"] > end[0]["dark"]):
                        temp = state
                        while temp.depth != 1:
                            temp = temp.prev
                        print("dark is making an evil move")
                        print(state.end())
                        good_move = temp.moves
                        if good_move[0][2] == "ddll":
                            # evil_move = State.move("", good_move[0], good_move[1], [], self.board)
                            # evil_move = make_a_move2()

                            """
                        не работет поиск полного хода при известной клетке и шашке, потому что используеться в другом классе
                        нужно переделать возможно перенести эту функцию вне класса чтобы плюс убрать дип копи, и доделать сехму противополодных ходов
                        
                        
                        """



                        return temp.moves
                    elif self.myColor == "l" and (end[0]["dark"] > end[0]["light"]):
                        temp = state
                        while temp.depth != 1:
                            temp = state.prev
                        print("dark is making a move")
                        print(state.end())
                        return temp.moves
        return []


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

def print_board(board, name):
    d = Drawer.Drawer()        
    d.draw(board, name)

def inside(r, c, where):
        return 0 <= r < len(where) and 0 <= c < len(where[0])

def make_a_move(tile, r, c, board, moves):
    # Check if tile can be legally placed at the specified position
    if (
        (r == 0 or board[r - 1][c] == "none" or board[r - 1][c][3] == tile[1])
        and (c == len(board[0]) - 1 or board[r][c + 1] == "none" or board[r][c + 1][0] == tile[2])
        and (r == len(board) - 1 or board[r + 1][c] == "none" or board[r + 1][c][1] == tile[3])
        and (c == 0 or board[r][c - 1] == "none" or board[r][c - 1][2] == tile[0])
        and board[r][c] == 'none'
    ):
        # Place tile on board and record the move
        board[r][c] = tile
        moves.append([r, c, tile])
    else:
        return False

    # Check for forced moves in the eight positions surrounding the tile
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
        main, temp, r_offset_main, c_offset_main, r_offset, c_offset = item
        if (
            inside(r + r_offset, c + c_offset, board)
            and board[r + r_offset_main][c + c_offset_main] == "none"
            and board[r + r_offset][c + c_offset][temp] == tile[main]
        ):
            make_a_move(lookup_forced_moves[tile[main] +  str(idx + 1)], r + r_offset_main, c + c_offset_main, board, moves)

    return board, moves

def end_stats(state):
    temp_end = False
    temp_stat = state.cycles_lines()
    if temp_stat["light"] != 0 or temp_stat["dark"] != 0 or ("none" not in str(state.board)):
        temp_end = True
    return [temp_stat, temp_end]

def has_duplicates(matrix_list):
    count = 0
    for i in range(len(matrix_list)):
        for j in range(i+1, len(matrix_list)):
            if all(matrix_list[i][k] == matrix_list[j][k] for k in range(len(matrix_list[i]))):

                count += 1
    return count




def expand(state):
        res = []
        ASs = state.AS()
        tried_already = set()
        boardCopy = state.board
        for AvailableSpot in ASs:
            r = AvailableSpot[0]
            c = AvailableSpot[1]
            for tile in state.tiles:
                new = State([], [], state.depth + 1, state)
                move = make_a_move(tile, r, c, boardCopy, [])
                if move:
                    new.board = move[0]
                    new.moves = move[1]
                    if str(move[0]) not in tried_already:
                        res.append(new)
                        tried_already.add(str(move[0]))
                boardCopy = copy.deepcopy(state.board)
        return res

def BFS_winning(board, player_color):
        tried_already = set()
        best_moves = []
        boardCopy = copy.deepcopy(board)
        State0 = State(boardCopy, [], 0)
        queue = [State0]
        matrix_list = []
        while queue:
            actual = queue.pop(0)
            tried_already.add(str(actual.board))
            newStates = expand(actual)


            """
            if has_duplicates(matrix_list):
                print("The list contains duplicates")
            else:
                print("The list doesnt contain duplicates")
            """
            
            for state in newStates:
                end = end_stats(state)
                if state.depth > 2:
                    break
                if str(state.board) not in tried_already:
                    matrix_list.append(state.board)
                    print_board(state.board, f"{state.depth}, {state.moves}, {end}.png")
                    queue.append(state)

                # print(f"{state.moves}, {state.depth}")
                # print(end)
                # print(state.moves)
                # print()
                continue
                if end[1] is False and str(state.board) not in tried_already:
                    queue.append(state)
                elif end[1] is True:
                    if player_color == "l" and (end[0]["light"] > end[0]["dark"]):
                        temp = state
                        while temp.depth != 1:
                            temp = temp.prev
                            return temp.moves
                    elif player_color == "d" and (end[0]["dark"] > end[0]["light"]):
                        temp = state
                        while temp.depth != 1:
                            temp = temp.prev
                            return temp.moves
        print(len(tried_already))
        print(has_duplicates(matrix_list))
        return []
                # if len(best_moves) > 5:
                #     break
        if best_moves:
            closest_win = best_moves[0]
            for move in best_moves:
                if move.depth < closest_win.depth:
                    closest_win = move
            temp = closest_win
            while temp.depth != 1:
                temp = temp.prev
                print(*temp.board,sep='\n')
            print(player_color, "is making a move")
            print(*closest_win.board, sep='\n')
            print(closest_win.end())
            print(temp.moves)
            return temp.moves
        else:
            return []




if __name__ == "__main__":
    # call you functions from this block:
    
    """
    # !Debug for correctly placing a tile!

    board = [
        ["none", "none","none"],
        ["dlld", "ldld","lldd"],
        ["none", "none","none"],
    ]
    move = make_a_move("dldl", 0, 0, board, [])
    print_board(move[0], "test.png")
    print(move[1])
    newState = State(move[0], [], 0)
    print(end_stats(newState))
    sys.exit()
    # """
    
    """
    # !Debug for expanding a state!

    board = [
            ["none", "none","none"],
            ["dlld", "ldld","lldd"],
            ["none", "none","none"],
        ]

    State0 = State(board, [], 0)
    print("Zero state is ")
    print(*State0.board, sep="\n")
    print(end_stats(State0))

    newStates = expand(State0)
    for idx, state in enumerate(newStates):
        print(state.moves)
        print_board(state.board, f"Expansion test, moves:{state.moves}.png")
    sys.exit()
    # """

    """
    # !Debug for counting cycles and lines!

    board = [
            ["lddl", "dlld","lldd"],
            ["dlld", "ldld","lddl"],
            ["none", "none","none"]
        ]
    state = State(board, [], 0)
    print(end_stats(state))
    print(state.cycles_lines())
    sys.exit()
    # """

    

    # """
    boardRows = 10
    boardCols = boardRows
    board = [["none"] * boardCols for _ in range(boardRows)]

    board[boardRows // 2][boardCols // 2] = [
        "lldd",
        "dlld",
        "ddll",
        "lddl",
        "dldl",
        "ldld",
    ][random.randint(0, 5)]
    # """
    
    """
    альфа бета прунинг, сохранение дерева исходов и его увеличение каждый ход, 
    система начисления очков через победные состояния и длинну линий в отношении важности(коэффициентов)


    юзать zip


    start = time.perf_counter()
    end = time.perf_counter()
    print(end - start)
    
    """

    board = [
            ["none", "none","none"],
            ["dlld", "ldld","lldd"],
            ["none", "none","none"],
        ]

    d = Drawer.Drawer()
    

    
    p1 = Player(board, "player1", "l")
    p2 = Player(board, "player2", "d")

    idx = 0
    while True:
        # call player for his move

        rmove = BFS_winning(p1.board, p1.myColor)
        sys.exit()

        # if len(rmove) == 0:
        #     rmove = p1.BFS_losing()
        # print(rmove)
        # rmove is: [ [r1,c1,tile1], ... [rn,cn,tile] ]
        # write to board of both players
        for move in rmove:
            row, col, tile = move
            p1.board[row][col] = tile
            p2.board[row][col] = tile

        # make png with resulting board
        d.draw(p1.board, "move-{:04d}.png".format(idx))
        idx += 1

        if len(rmove) == 0:
            print("End of game")
            break
        p1, p2 = p2, p1  # switch players
