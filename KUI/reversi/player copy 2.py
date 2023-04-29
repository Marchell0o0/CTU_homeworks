import random
import time
import sys
import copy
import bisect

positional_advantage = [[
    [60, -10, 10, 10, -10, 60],
    [-10, -20, -2, -2, -20, -10],
    [10, -2, 5, 5, -2, 10],
    [10, -2, 5, 5, -2, 10],
    [-10, -20, -2, -2, -20, -10],
    [60, -10, 10, 10, -10, 60]
],
    [
    [120, -20, 20, 5, 5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20, 5, 5, 20, -20, 120]
],
    [
    [120, -20, 20, 5, 5, 5, 5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -5, -5, -40, -20],
    [20, -5, 15, 3, 3, 3, 3, 15, -5, 20],
    [5, -5, 3, 3, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, 3, 3, -5, 5],
    [20, -5, 15, 3, 3, 3, 3, 15, -5, 20],
    [-20, -40, -5, -5, -5, -5, -5, -5, -40, -20],
    [120, -20, 20, 5, 5, 5, 5, 20, -20, 120]
]]


class MyPlayer():
    '''Template Docstring for MyPlayer, look at the TODOs'''  # TODO a short description of your player

    def __init__(self, my_color, opponent_color, board_size=8):
        self.name = 'username'  # TODO: fill in your username
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size
        self.idx = (self.board_size // 2) - 3

    def move(self, starting_board):
        start = time.time()
        best_move = None

        max_depth = 4

        # max_eval = float('-inf') !!!

        possible_moves = self.get_all_valid_moves(
            starting_board, self.my_color)

        if possible_moves:
            if len(possible_moves) == 1:
                return possible_moves[0]
            else:
                while True:
                    if max_depth > self.board_size**2:
                        return best_move
                    max_eval = float('-inf')
                    alpha = float("-inf")
                    beta = float("inf")

                    for move in possible_moves:

                        temp_board = copy.deepcopy(starting_board)
                        temp_board = self.make_move(
                            temp_board, move, self.my_color)

                        eval = self.minimax(
                            temp_board, max_depth, False, alpha, beta, start)
                        print("evaluation of", move, "is",
                              eval, "at this depth", max_depth)
                        if eval == "out of time":
                            print("best move is", best_move,
                                  "evaluated with depths", max_depth)
                            return best_move

                        if eval > max_eval:
                            max_eval = eval
                            temp_best_move = move

                            # alpha = max(alpha, eval)
                            # if beta <= alpha:
                            #     break
                    best_move = temp_best_move
                    max_depth += 1
        else:
            return best_move

    def minimax(self, board, depth, maximizing_player, alpha, beta, start):
        if time.time() - start > 4.990:
            return "out of time"

        if depth == 0 or self.is_game_over(board):
            return self.evaluate(board)

        if maximizing_player:
            max_eval = float('-inf')
            possible_moves = self.get_all_valid_moves(board, self.my_color)
            if possible_moves:
                for move in possible_moves:

                    temp_board = copy.deepcopy(board)
                    temp_board = self.make_move(board, move, self.my_color)

                    eval = self.minimax(
                        temp_board, depth - 1, False, alpha, beta, start)

                    if eval == 'out of time':
                        return eval

                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return max_eval
            else:
                return self.minimax(board, depth-1, False, alpha, beta, start)

        else:
            min_eval = float('inf')
            possible_moves = self.get_all_valid_moves(
                board, self.opponent_color)
            if possible_moves:
                for move in possible_moves:

                    temp_board = copy.deepcopy(board)
                    temp_board = self.make_move(
                        board, move, self.opponent_color)

                    eval = self.minimax(
                        temp_board, depth - 1, True, alpha, beta, start)

                    if eval == 'out of time':
                        return eval

                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return min_eval
            else:
                return self.minimax(board, depth-1, True, alpha, beta, start)

    def is_game_over(self, board):
        if not self.get_all_valid_moves(board, 0) and not self.get_all_valid_moves(board, 1):
            return True
        else:
            return False

    def make_move(self, board, move, player_color):

        temp_board = copy.deepcopy(board)
        temp_board[move[0]][move[1]] = player_color
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(len(dx)):
            if self.__confirm_direction(temp_board, move, dx[i], dy[i], player_color):
                self.change_stones_in_direction(temp_board,
                                                move, dx[i], dy[i], player_color)
        return temp_board

    def __confirm_direction(self, board, move, dx, dy, player_color):

        if player_color == 0:
            opponents_color = 1
        else:
            opponents_color = 0

        posx = move[0]+dx
        posy = move[1]+dy
        if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
            if board[posx][posy] == opponents_color:
                while (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
                    posx += dx
                    posy += dy
                    if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
                        if board[posx][posy] == -1:
                            return False
                        if board[posx][posy] == player_color:
                            return True

        return False

    def change_stones_in_direction(self, board, move, dx, dy, player_color):
        posx = move[0]+dx
        posy = move[1]+dy
        while (not (board[posx][posy] == player_color)):
            board[posx][posy] = player_color
            posx += dx
            posy += dy

    def evaluate(self, board):
        board_eval = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] != -1:
                    if board[i][j] == 0:
                        board_eval -= positional_advantage[self.idx][i][j]
                    else:
                        board_eval += positional_advantage[self.idx][i][j]
        if self.my_color == 0:
            return -board_eval
        else:
            return board_eval

    def __is_correct_move(self, move, board, player_color):
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(len(dx)):
            if self.__confirm_direction(board, move, dx[i], dy[i], player_color):
                return True,
        return False

    def get_all_valid_moves(self, board, player_color):

        valid_moves = []

        for x in range(self.board_size):
            for y in range(self.board_size):
                if (board[x][y] == -1) and self.__is_correct_move([x, y], board, player_color):
                    valid_moves.append(
                        (x, y, positional_advantage[self.idx][x][y]))

        if len(valid_moves) <= 0:
            # print('No possible move!')
            return None

        return sorted(valid_moves, key=lambda x: x[2], reverse=True)


# class Node():
#     def __init__(self, board, parent=None) -> None:
#         self.board = board
#         self.parent = parent


if __name__ == "__main__":
    board = [
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, 1, -1, -1, -1],
        [-1, -1, -1, 1, 1, -1, -1, -1],
        [-1, -1, -1, 0, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1],
    ]

    player = MyPlayer(0, 1, 8)
    print(player.get_all_valid_moves(board, 0))
    print(player.get_all_valid_moves(board, 1))
    print(player.evaluate(board))
    print(player.is_game_over(board))
    # print(*player.make_move(board, (4, 5), 0), sep="\n")
    # print()
    # print(*board, sep="\n")
    move = player.move(board)
    print(move)


"""
better evaluation function

check if evaluation and everything is correct (maybe even propagating)

"""
