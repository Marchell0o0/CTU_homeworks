import copy


class State:
    def __init__(self, board, moves, end, prev=None):
        self.board = board[:]
        self.moves = moves
        self.end = end
        self.prev = prev

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

    def move(self, tile, r, c, moves, mainBoard):
        boardCopy = mainBoard[:]

        """

        checking and placing the first tile

        """

        if (
            (
                r == 0
                or boardCopy[r - 1][c] == "none"
                or boardCopy[r - 1][c][3] == tile[1]
            )
            and (
                c == len(boardCopy[0]) - 1
                or boardCopy[r][c + 1] == "none"
                or boardCopy[r][c + 1][0] == tile[2]
            )
            and (
                r == len(boardCopy)
                or boardCopy[r + 1][c] == "none"
                or boardCopy[r + 1][c][1] == tile[3]
            )
            and (
                c == 0
                or boardCopy[r][c - 1] == "none"
                or boardCopy[r][c - 1][2] == tile[0]
            )
        ):
            boardCopy[r][c] = tile
            moves.append([r, c, tile])
            print(*board, sep="\n")
            print()
        else:
            return False

        """
        
        checking all its neighbours for a forced move

        """
        if (
            self.inside(r - 1, c - 1, boardCopy)
            and boardCopy[r - 1][c - 1][2] == tile[1]
            and boardCopy[r - 1][c] == "none"
        ):
            if tile[1] == "d":
                self.move("dlld", r - 1, c, moves, boardCopy)
            if tile[1] == "l":
                self.move("lddl", r - 1, c, moves, boardCopy)

        if (
            self.inside(r - 2, c, boardCopy)
            and boardCopy[r - 2][c][3] == tile[1]
            and boardCopy[r - 1][c] == "none"
        ):
            if tile[1] == "d":
                self.move("ldld", r - 1, c, moves, boardCopy)
            if tile[1] == "l":
                self.move("dldl", r - 1, c, moves, boardCopy)

        if (
            self.inside(r - 1, c + 1, boardCopy)
            and boardCopy[r - 1][c + 1][0] == tile[1]
            and boardCopy[r - 1][c] == "none"
        ):
            if tile[1] == "d":
                self.move("lldd", r - 1, c, moves, boardCopy)
            if tile[1] == "l":
                self.move("ddll", r - 1, c, moves, boardCopy)

        if (
            self.inside(r - 1, c + 1, boardCopy)
            and boardCopy[r - 1][c + 1][3] == tile[2]
            and boardCopy[r][c + 1] == "none"
        ):
            if tile[2] == "d":
                self.move("ddll", r, c + 1, moves, boardCopy)
            if tile[2] == "l":
                self.move("lldd", r, c + 1, moves, boardCopy)

        if (
            self.inside(r, c + 2, boardCopy)
            and boardCopy[r][c + 2][0] == tile[2]
            and boardCopy[r][c + 1] == "none"
        ):
            if tile[2] == "d":
                self.move("dldl", r, c + 1, moves, boardCopy)
            if tile[2] == "l":
                self.move("ldld", r, c + 1, moves, boardCopy)

        if (
            self.inside(r + 1, c + 1, boardCopy)
            and boardCopy[r + 1][c + 1][1] == tile[2]
            and boardCopy[r][c + 1] == "none"
        ):
            if tile[2] == "d":
                self.move("dlld", r, c + 1, moves, boardCopy)
            if tile[2] == "l":
                self.move("lddl", r, c + 1, moves, boardCopy)

        if (
            self.inside(r + 1, c + 1, boardCopy)
            and boardCopy[r + 1][c + 1][0] == tile[3]
            and boardCopy[r + 1][c] == "none"
        ):
            if tile[3] == "d":
                self.move("lddl", r + 1, c, moves, boardCopy)
            if tile[3] == "l":
                self.move("ddll", r + 1, c, moves, boardCopy)

        if (
            self.inside(r + 2, c, boardCopy)
            and boardCopy[r + 2][c][1] == tile[3]
            and boardCopy[r + 1][c] == "none"
        ):
            if tile[3] == "d":
                self.move("ldld", r + 1, c, moves, boardCopy)
            if tile[3] == "l":
                self.move("dldl", r + 1, c, moves, boardCopy)

        if (
            self.inside(r + 1, c - 1, boardCopy)
            and boardCopy[r + 1][c - 1][2] == tile[3]
            and boardCopy[r + 1][c] == "none"
        ):
            if tile[3] == "d":
                self.move("ddll", r + 1, c, moves, boardCopy)
            if tile[3] == "l":
                self.move("lldd", r + 1, c, moves, boardCopy)

        if (
            self.inside(r + 1, c - 1, boardCopy)
            and boardCopy[r + 1][c - 1][1] == tile[0]
            and boardCopy[r][c - 1] == "none"
        ):
            if tile[0] == "d":
                self.move("lldd", r, c - 1, moves, boardCopy)
            if tile[0] == "l":
                self.move("ddll", r, c - 1, moves, boardCopy)

        if (
            self.inside(r, c - 2, boardCopy)
            and boardCopy[r][c - 2][2] == tile[0]
            and boardCopy[r][c - 1] == "none"
        ):
            if tile[0] == "d":
                self.move("dldl", r, c - 1, moves, boardCopy)
            if tile[0] == "l":
                self.move("ldld", r, c - 1, moves, boardCopy)

        if (
            self.inside(r - 1, c - 1, boardCopy)
            and boardCopy[r - 1][c - 1][3] == tile[0]
            and boardCopy[r][c - 1] == "none"
        ):
            if tile[0] == "d":
                self.move("lddl", r, c - 1, moves, boardCopy)
            if tile[0] == "l":
                self.move("dlld", r, c - 1, moves, boardCopy)

        return moves, boardCopy


board = [
    ["none", "none", "none", "none"],
    ["none", "none", "none", "none"],
    ["dlld", "lddl", "dldl", "none"],
    ["none", "none", "none", "none"],
]
print(*board, sep="\n")
print()

State0 = State(board, [], False, None)
print(State0.move("dldl", 1, 2, [], board))
