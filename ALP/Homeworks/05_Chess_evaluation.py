from sys import argv

board = []
f = open(argv[1], "r", encoding="utf-8")
for line in f:
    board.append(list(map(int, line.split())))


def check_up(lct, brd):
    distance = 0
    for r in range(lct[0] - 1, -1, -1):
        enemy = brd[r][lct[1]]
        if distance == 0 and enemy == 1:
            return True
        if enemy in (2, 3):
            return True
        if enemy != 0:
            return False
        distance += 1
    return False


def check_down(lct, brd):
    distance = 0
    for r in range(lct[0] + 1, 8):
        enemy = brd[r][lct[1]]
        if distance == 0 and enemy == 1:
            return True
        if enemy in (2, 3):
            return True
        if enemy != 0:
            return False
        distance += 1
    return False


def check_left(lct, brd):
    distance = 0
    for c in range(lct[1] - 1, -1, -1):
        enemy = brd[lct[0]][c]
        if distance == 0 and enemy == 1:
            return True
        if enemy in (2, 3):
            return True
        if enemy != 0:
            return False
        distance += 1
    return False


def check_right(lct, brd):
    distance = 0
    for c in range((lct[1] + 1), 8):
        enemy = brd[lct[0]][c]
        if distance == 0 and enemy == 1:
            return True
        if enemy in (2, 3):
            return True
        if enemy != 0:
            return False
        distance += 1
    return False


def check_up_left(lct, brd):
    for cr in range(1, 8):
        if lct[0] - cr < 0 or lct[1] - cr < 0:
            return False
        enemy = brd[lct[0] - cr][lct[1] - cr]
        if enemy == 2 or enemy == 4:
            return True
        if enemy != 0:
            return False
    return False


def check_up_right(lct, brd):
    for cr in range(1, 8):
        if lct[0] - cr < 0 or lct[1] + cr > 7:
            return False
        enemy = brd[lct[0] - cr][lct[1] + cr]
        if enemy == 2 or enemy == 4:
            return True
        if enemy != 0:
            return False
    return False


def check_down_right(lct, brd):
    distance = 0
    for cr in range(1, 8):
        if lct[0] + cr > 7 or lct[1] + cr > 7:
            return False, 0
        enemy = brd[lct[0] + cr][lct[1] + cr]
        if enemy == 2 or enemy == 4:
            return True, 0
        if distance == 0 and enemy == 6:
            return True, 1
        if enemy != 0:
            return False, 0
        distance += 1
    return False, 0


def check_down_left(lct, brd):
    distance = 0
    for cr in range(1, 8):
        if (lct[0] + cr) > 7 or (lct[1] - cr) < 0:
            return False, 0
        enemy = brd[lct[0] + cr][lct[1] - cr]
        if enemy == 2 or enemy == 4:
            return True, 0
        if distance == 0 and enemy == 6:
            return True, 1
        if enemy != 0:
            return False, 0
        distance += 1
    return False, 0


def check_horses(lct, brd):
    spots1 = [-2, -1, 1, 2, 2, 1, -1, -2]
    spots = []
    for idx, item in enumerate(spots1):
        spots.append([item, spots1[idx - 2]])
    for k in range(8):
        temp = spots[k]
        r = lct[0] + temp[0]
        c = lct[1] + temp[1]
        if r < 0 or c < 0 or r > 7 or c > 7:
            continue
        enemy = brd[r][c]
        if enemy == 5:
            return True
    return False


def move_out(brd, lct):
    brd[lct[0]][lct[1]] = 0
    for r in range(-1, 2):
        for c in range(-1, 2):
            if r == 0 and c == 0:
                continue
            rr = lct[0] + r
            cc = lct[1] + c
            if rr < 0 or cc < 0 or rr > 7 or cc > 7:
                continue
            if brd[rr][cc] == 0:
                temploc = [rr, cc]
                if check_danger(brd, temploc)[0] == 0:
                    return True
    return False


def check_danger(brd, lct):
    danger = 0
    dangerlct = ""
    pawns = 0
    if check_right(lct, brd) is True:
        danger += 1
        dangerlct = "right"
    if check_left(lct, brd) is True:
        danger += 1
        dangerlct = "left"
    if check_up(lct, brd) is True:
        danger += 1
        dangerlct = "up"
    if check_down(lct, brd) is True:
        danger += 1
        dangerlct = "down"
    if check_up_left(lct, brd) is True:
        danger += 1
        dangerlct = "up_left"
    if check_up_right(lct, brd) is True:
        danger += 1
        dangerlct = "up_right"
    if check_down_left(lct, brd)[0] is True:
        danger += 1
        dangerlct = "down_left"
    if check_down_right(lct, brd)[0] is True:
        danger += 1
        dangerlct = "down_right"
    if check_horses(lct, brd) is True:
        danger += 1
        dangerlct = "horses"
    pawns = check_down_left(lct, brd)[1] + check_down_right(lct, brd)[1]
    return danger, dangerlct, pawns


def check_defense(brd, lct, danger_location):
    """Check for defending"""
    tempbrd2 = [8 * [0] for i in range(8)]
    enemy = 0
    templct = []
    for r in range(8):
        for c in range(8):
            if brd[r][c] == -1:
                tempbrd2[r][c] = 0
            else:
                tempbrd2[r][c] = -brd[r][c]
    if danger_location == "right":
        for cc in range(lct[1] + 1, 8):
            enemy = tempbrd2[lct[0]][cc]
            templct = [lct[0], cc]
            if enemy == 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
            if enemy < 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
                return False
    if danger_location == "left":
        for cc in range(lct[1] - 1, -1, -1):
            enemy = tempbrd2[lct[0]][cc]
            templct = [lct[0], cc]
            if enemy == 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
            if enemy < 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
                return False
    if danger_location == "up":
        for rr in range(lct[0] - 1, -1, -1):
            enemy = tempbrd2[rr][lct[1]]
            templct = [rr, lct[1]]
            if enemy == 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
            if enemy < 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
                return False
    if danger_location == "down":
        for rr in range(lct[0] + 1, 8):
            enemy = tempbrd2[rr][lct[1]]
            templct = [rr, lct[1]]
            if enemy == 0:
                if (
                    check_danger(tempbrd2, templct)[0] != 0
                    and (
                        check_danger(tempbrd2, templct)[0]
                        - check_danger(tempbrd2, templct)[2]
                    )
                    != 0
                ):
                    return True
            if enemy < 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
                return False
    if danger_location == "up_right":
        for cr in range(8):
            enemy = tempbrd2[lct[0] - cr][lct[1] + cr]
            templct = [lct[0] - cr, lct[1] + cr]
            if enemy == 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
            if enemy < 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
                return False
    if danger_location == "up_left":
        for cr in range(8):
            enemy = tempbrd2[lct[0] - cr][lct[1] - cr]
            templct = [lct[0] - cr, lct[1] - cr]
            if enemy == 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
            if enemy < 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
                return False
    if danger_location == "down_left":
        for cr in range(1, 8):
            enemy = tempbrd2[lct[0] + cr][lct[1] - cr]
            templct = [lct[0] + cr, lct[1] - cr]
            if enemy == 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
            if enemy < 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
                return False
    if danger_location == "down_right":
        for cr in range(1, 8):
            enemy = tempbrd2[lct[0] + cr][lct[1] + cr]
            templct = [lct[0] + cr, lct[1] + cr]
            if enemy == 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
            if enemy < 0:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
                return False
    if danger_location == "horses":
        spots1 = [-2, -1, 1, 2, 2, 1, -1, -2]
        spots = []
        for idx, item in enumerate(spots1):
            spots.append([item, spots1[idx - 2]])
        for k in range(8):
            temp = spots[k]
            r = lct[0] + temp[0]
            c = lct[1] + temp[1]
            if r < 0 or c < 0 or r > 7 or c > 7:
                continue
            enemy = tempbrd2[r][c]
            templct = [r, c]
            if enemy == -5:
                if check_danger(tempbrd2, templct)[0] != 0:
                    return True
                return False


LOCATION_QUEEN = 0
LOCATION_KING = 0

for row in range(8):
    for col in range(8):
        if board[row][col] == -1:
            LOCATION_KING = [row, col]

for row in range(8):
    for col in range(8):
        if board[row][col] == -2:
            LOCATION_QUEEN = [row, col]


DANGER_FIRST = 0
DANGER_LOCATION = ""


DANGER_FIRST = check_danger(board, LOCATION_KING)[0]
DANGER_LOCATION = check_danger(board, LOCATION_KING)[1]
MOVE = move_out(board, LOCATION_KING)

if DANGER_FIRST == 1:
    DEFENSE = check_defense(board, LOCATION_KING, DANGER_LOCATION)
else:
    DEFENSE = False

if DANGER_FIRST > 0 and MOVE is False and DEFENSE is False:
    print("MAT")
elif DANGER_FIRST > 0:
    print("SACH")
else:
    if LOCATION_QUEEN != 0:
        if check_danger(board, LOCATION_QUEEN)[0] > 0:
            print("GARDE")
        else:
            print("NO")
    else:
        print("NO")
