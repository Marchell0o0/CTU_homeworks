import random
import time
import sys
import copy


class MyPlayer():
    '''Template Docstring for MyPlayer, look at the TODOs'''  # TODO a short description of your player

    def __init__(self, my_color, opponent_color, board_size=8):
        self.name = 'username'  # TODO: fill in your username
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size

    def move(self, board):
        # TODO: write you method
        # you can implement auxiliary fucntions, of course

        start_node = Node(board, None)
        move = self.minimax(start_node, float(
            "-inf"), float("inf"), time.time())

        return move

    def minimax(self, start_node, alpha, beta, start):
        best_move = None
        i = 2
        max_eval = float('-inf')
        possible_moves = self.get_all_valid_moves(start_node.board)
        if possible_moves:
            while True:

                # max_eval = float('-inf')
                for move in possible_moves:

                    temp_board = self.make_move(start_node.board, move)
                    child = Node(temp_board, start_node)

                    eval = self.minimax_inner(
                        child, i - 1, False, alpha, beta, start)
                    if eval == "end":
                        # print(i)
                        # print(max_eval)
                        return best_move
                    # print(eval)

                    if eval > max_eval:
                        max_eval = eval
                        best_move = move

                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                i += 1
        else:
            return best_move

    def minimax_inner(self, node, depth, maximizing_player, alpha, beta, start):
        if time.time() - start > 1:
            return "end"

        if depth == 0 or self.is_game_over(node.board):
            return self.score(node.board)

        if maximizing_player:
            max_eval = float('-inf')
            possible_moves = self.get_all_valid_moves(node.board)
            if possible_moves:
                for move in possible_moves:

                    temp_board = self.make_move(node.board, move)
                    child = Node(temp_board, node)
                    eval = self.minimax_inner(child, depth - 1, False,
                                              alpha, beta, start)

                    if eval == 'end':
                        return eval

                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return max_eval

        else:
            min_eval = float('inf')
            possible_moves = self.get_all_valid_moves(node.board)
            for move in possible_moves:
                temp_board = self.make_move(node.board, move)
                child = Node(temp_board, node)
                eval = self.minimax_inner(child, depth - 1, True,
                                          alpha, beta, start)

                if eval == 'end':
                    return eval

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def is_game_over(self, board):
        valid_moves_for_me = (self.get_all_valid_moves(board))

        self.my_color, self.opponent_color = self.opponent_color, self.my_color
        valid_moves_for_opponent = self.get_all_valid_moves(board)
        self.my_color, self.opponent_color = self.opponent_color, self.my_color
        if not valid_moves_for_me and not valid_moves_for_opponent:
            return True
        else:
            return False

    def make_move(self, board,  move):

        temp_board = copy.deepcopy(board)
        temp_board[move[0]][move[1]] = self.my_color
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(len(dx)):
            if self.__confirm_direction(temp_board, move, dx[i], dy[i])[0]:
                self.change_stones_in_direction(temp_board,
                                                move, dx[i], dy[i])
        return temp_board

    def confirm_direction_for_move(self, board, move, dx, dy):

        posx = move[0]+dx
        posy = move[1]+dy
        if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
            if board[posx][posy] == self.opponent_color:
                while (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
                    posx += dx
                    posy += dy
                    if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
                        if board[posx][posy] == -1:
                            return False
                        if board[posx][posy] == self.my_color:
                            return True

        return False

    def __confirm_direction(self, board,  move, dx, dy):
        posx = move[0]+dx
        posy = move[1]+dy
        opp_stones_inverted = 0
        if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
            if board[posx][posy] == self.opponent_color:
                opp_stones_inverted += 1
                while (posx >= 0) and (posx <= (self.board_size-1)) and (posy >= 0) and (posy <= (self.board_size-1)):
                    posx += dx
                    posy += dy
                    if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
                        if board[posx][posy] == -1:
                            return False, 0
                        if board[posx][posy] == self.my_color:
                            return True, opp_stones_inverted
                    opp_stones_inverted += 1

        return False, 0

    def change_stones_in_direction(self, board, move, dx, dy):
        posx = move[0]+dx
        posy = move[1]+dy
        while (not (board[posx][posy] == self.my_color)):
            board[posx][posy] = self.my_color
            posx += dx
            posy += dy

    def score(self, board):
        blue = 0
        red = 0
        for row in board:
            blue += row.count(0)
            red += row.count(1)
        if self.my_color == 0:
            return blue - red
        else:
            return red - blue

    def __is_correct_move(self, move, board):
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(len(dx)):
            if self.__confirm_direction(board, move, dx[i], dy[i])[0]:
                return True,
        return False

    def get_all_valid_moves(self, board):
        valid_moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if (board[x][y] == -1) and self.__is_correct_move([x, y], board):
                    valid_moves.append((x, y))

        if len(valid_moves) <= 0:
            # print('No possible move!')
            return None
        return valid_moves


class Node():
    def __init__(self, board, parent=None) -> None:
        self.board = board
        self.parent = parent


# if __name__ == "__main__":
#     board = [
#         [-1, -1, -1, -1, -1, -1, -1, -1],
#         [-1, -1, -1, -1, -1, -1, -1, -1],
#         [-1, -1, -1, -1, -1, -1, -1, -1],
#         [-1, -1, -1, 0, 1, -1, -1, -1],
#         [-1, -1, -1, 1, 0, -1, -1, -1],
#         [-1, -1, -1, -1, -1, -1, -1, -1],
#         [-1, -1, -1, -1, -1, -1, -1, -1],
#         [-1, -1, -1, -1, -1, -1, -1, -1],
#     ]
#     player = MyPlayer(0, 1, 8)
#     print(player.get_all_valid_moves(board))
#     print(player.score(board))
#     print(player.is_game_over(board))
#     print(*player.make_move(board, (2, 4)), sep="\n")
#     print()
#     print(*board, sep="\n")
#     move = player.move(board)
#     print(move)


"""
для каждой ноды вне зависимости от игрока выбираються ходы для текущего цвета 
оценивать доску конечно нужно с одной перспективы но ходы выбирать нет 
придумать что делать если кто то пропускает ход 


"""
