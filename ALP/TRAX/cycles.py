from sys import argv, exit

with open(argv[1], "r", encoding="utf-8") as f:
    inp = [list(map(str, line.split())) for line in f]


global tried_already_light
global tried_already_dark
global cycles_light
global cycles_dark
global max_length_light
global max_length_dark
tried_already_light = {}
tried_already_dark = {}
cycles_light = 0
cycles_dark = 0
max_length_light = 0
max_length_dark = 0


def inside(r, c, fld):
    return 0 <= r < len(fld) and 0 <= c < len(fld[0])


def main(fld, func_light, func_dark) -> None:
    global tried_already
    for line in range(len(fld)):
        for tile in range(len(fld[0])):
            if [line, tile] not in tried_already_light:
                func_light(line, tile, fld, [line, tile], 0)
                tried_already_light[str([line, tile])] = 1
    for line in range(len(fld)):
        for tile in range(len(fld[0])):
            if [line, tile] not in tried_already_dark:
                func_dark(line, tile, fld, [line, tile], 0)
                tried_already_dark[str([line, tile])] = 1


def move_through_light(line, tile, fld, start, length):
    global tried_already_light
    global cycles_light
    global max_length_light
    if [line, tile] == start and length > 3:
        cycles_light += 1
        max_length_light = max(max_length_light, length)
        return True
    length += 1
    if (
        fld[line][tile][2] == "l"
        and inside(line, tile + 1, fld)
        and fld[line][tile + 1][0] == "l"
        and str([line, tile + 1]) not in tried_already_light
    ):
        """Check to the right"""
        tried_already_light[str([line, tile + 1])] = 1
        move_through_light(line, tile + 1, fld, start, length)

    elif (
        fld[line][tile][3] == "l"
        and inside(line + 1, tile, fld)
        and fld[line + 1][tile][1] == "l"
        and str([line + 1, tile]) not in tried_already_light
    ):
        """Check below"""
        tried_already_light[str([line + 1, tile])] = 1
        move_through_light(line + 1, tile, fld, start, length)

    elif (
        fld[line][tile][0] == "l"
        and inside(line, tile - 1, fld)
        and fld[line][tile - 1][2] == "l"
        and str([line, tile - 1]) not in tried_already_light
    ):
        """Check to the left"""
        tried_already_light[str([line, tile - 1])] = 1
        move_through_light(line, tile - 1, fld, start, length)

    elif (
        fld[line][tile][1] == "l"
        and inside(line - 1, tile, fld)
        and fld[line - 1][tile][3] == "l"
        and str([line - 1, tile]) not in tried_already_light
    ):
        """Check above"""
        tried_already_light[str([line - 1, tile])] = 1
        move_through_light(line - 1, tile, fld, start, length)
    else:
        return False


def move_through_dark(line, tile, fld, start, length):
    global tried_already_dark
    global cycles_dark
    global max_length_dark
    if [line, tile] == start and length > 3:
        cycles_dark += 1
        max_length_dark = max(max_length_dark, length)
        return True
    length += 1
    if (
        fld[line][tile][2] == "d"
        and inside(line, tile + 1, fld)
        and fld[line][tile + 1][0] == "d"
        and str([line, tile + 1]) not in tried_already_dark
    ):
        """Check to the right"""
        tried_already_dark[str([line, tile + 1])] = 1
        move_through_dark(line, tile + 1, fld, start, length)

    elif (
        fld[line][tile][3] == "d"
        and inside(line + 1, tile, fld)
        and fld[line + 1][tile][1] == "d"
        and str([line + 1, tile]) not in tried_already_dark
    ):
        """Check below"""
        tried_already_dark[str([line + 1, tile])] = 1
        move_through_dark(line + 1, tile, fld, start, length)

    elif (
        fld[line][tile][0] == "d"
        and inside(line, tile - 1, fld)
        and fld[line][tile - 1][2] == "d"
        and str([line, tile - 1]) not in tried_already_dark
    ):
        """Check to the left"""
        tried_already_dark[str([line, tile - 1])] = 1
        move_through_dark(line, tile - 1, fld, start, length)

    elif (
        fld[line][tile][1] == "d"
        and inside(line - 1, tile, fld)
        and fld[line - 1][tile][3] == "d"
        and str([line - 1, tile]) not in tried_already_dark
    ):
        """Check above"""
        tried_already_dark[str([line - 1, tile])] = 1
        move_through_dark(line - 1, tile, fld, start, length)
    else:
        return False


if __name__ == "__main__":
    main(inp, move_through_light, move_through_dark)
    print(cycles_light, cycles_dark, max_length_light, max_length_dark)
