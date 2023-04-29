from sys import argv

with open(argv[1], "r", encoding="utf-8") as f:
    inp = [list(map(str, line.split())) for line in f]

global tried_already
global res
res = []
tried_already = set()


def inside(r, c, board):
    return 0 <= r < len(board) and 0 <= c < len(board[0])


def main(board) -> None:
    global tried_already
    global res
    for color in ["light", "dark"]:
        res = []
        for direction in ["td", "lr"]:
            tried_already = set()
            if direction == "lr":
                for r in range(len(board)):
                    if str([r, 0]) not in tried_already:
                        move_through(r, 0, board, 0, color, direction)
                        tried_already.add(str([r, 0]))

            else:
                for c in range(len(board[0])):
                    if str([0, c]) not in tried_already:
                        move_through(0, c, board, 0, color, direction)
                        tried_already.add(str([0, c]))
        print(res, color)


def move_through(r, c, board, length, color, direction):
    global tried_already
    global res
    if c == len(board) - 1 and direction == "lr" and color == "light":
        if board[r][c] == "ldld" or board[r][c] == "ddll" or board[r][c] == "dlld":
            res.append(length + 1)
            return True
    elif c == len(board) - 1 and direction == "lr" and color == "dark":
        if board[r][c] == "dldl" or board[r][c] == "lddl" or board[r][c] == "lldd":
            res.append(length + 1)
            return True
    elif r == len(board) - 1 and direction == "td" and color == "light":
        if board[r][c] == "dldl" or board[r][c] == "ddll" or board[r][c] == "lddl":
            res.append(length + 1)
            return True
    elif r == len(board) - 1 and direction == "td" and color == "dark":
        if board[r][c] == "ldld" or board[r][c] == "lldd" or board[r][c] == "dlld":
            res.append(length + 1)
            return True
    length += 1
    if (
        board[r][c][2] == color[0]
        and inside(r, c + 1, board)
        and board[r][c + 1][0] == color[0]
        and str([r, c + 1]) not in tried_already
    ):
        """Check to the right"""
        tried_already.add(str([r, c + 1]))
        move_through(r, c + 1, board, length, color, direction)
    elif (
        board[r][c][3] == color[0]
        and inside(r + 1, c, board)
        and board[r + 1][c][1] == color[0]
        and str([r + 1, c]) not in tried_already
    ):
        """Check below"""
        tried_already.add(str([r + 1, c]))
        move_through(r + 1, c, board, length, color, direction)
    elif (
        board[r][c][0] == color[0]
        and inside(r, c - 1, board)
        and board[r][c - 1][2] == color[0]
        and str([r, c - 1]) not in tried_already
    ):
        """Check to the left"""
        tried_already.add(str([r, c - 1]))
        move_through(r, c - 1, board, length, color, direction)
    elif (
        board[r][c][1] == color[0]
        and inside(r - 1, c, board)
        and board[r - 1][c][3] == color[0]
        and str([r - 1, c]) not in tried_already
    ):
        tried_already.add(str([r - 1, c]))
        move_through(r - 1, c, board, length, color, direction)
    else:
        return False


if __name__ == "__main__":
    main(inp)
