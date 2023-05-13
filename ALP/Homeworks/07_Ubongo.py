from sys import argv, exit
from copy import copy
from itertools import combinations


with open(argv[1], "r", encoding="utf-8") as f:
    inp = [list(map(int, line.split())) for line in f]

global figures
global num_of_columns
global num_of_rows
global answer

answer = []
field = list()
figures = dict()
figure = list()

num_of_columns = inp[0][0]
num_of_rows = inp[0][1]

for i in range(1, num_of_rows + 1):
    field.append(inp[i])


def rotate_figure(fgr):
    rotated = []
    num_of_zerosr = 0
    num_of_zerosc = 0
    size = max(get_max_x(fgr), get_max_y(fgr))
    a = [[0] * (size + 2) for i in range(size + 2)]
    for coord in fgr:
        a[coord[0]][coord[1]] = 1
    a = rotate(a)
    for i in range(len(a)):
        for k in range(len(a[i])):
            if a[i][k] == 1:
                rotated.append([i, k])
    for coord in rotated:
        if coord[0] == 0:
            num_of_zerosr += 1
        if coord[1] == 0:
            num_of_zerosc += 1
    while num_of_zerosr == 0:
        for coord in rotated:
            coord[0] -= 1
        for coord in rotated:
            if coord[0] == 0:
                num_of_zerosr += 1
    while num_of_zerosc == 0:
        for coord in rotated:
            coord[1] -= 1
        for coord in rotated:
            if coord[1] == 0:
                num_of_zerosc += 1

    return rotated


def rotate(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]) - 1, -1, -1)]


def get_max_x(fgr: list):
    max_x = 0
    for coord in fgr:
        if coord[0] > max_x:
            max_x = coord[0]
    return max_x


def get_max_y(fgr: list):
    max_y = 0
    for coord in fgr:
        if coord[1] > max_y:
            max_y = coord[1]
    return max_y


def try_to_place(fgr: list, field: list, figure_index: int):
    i_can = True
    # print("placing here")
    # print(*field, sep="\n")
    # print("this")
    # print(fgr)
    for coord in fgr:
        if field[coord[0]][coord[1]] != 0:
            i_can = False
    # print("can =", i_can)
    if i_can == True:
        for coord in fgr:
            field[coord[0]][coord[1]] = figure_index
    return i_can, field


def remove_figure(field, fgr):
    for coord in fgr:
        field[coord[0]][coord[1]] = 0
    return field


def try_new_block(field: list, figure_index: int, figures):
    global num_of_columns
    global num_of_rows
    global answer
    fgr = figures[figure_index]
    temp_fgr = fgr.copy()
    bottom_border = num_of_columns - get_max_x(fgr)
    right_border = num_of_rows - get_max_y(fgr)

    for r in range(bottom_border):
        for c in range(right_border):
            temp_fgr = fgr.copy()
            for idx, item in enumerate(temp_fgr):
                temp_fgr[idx] = [item[0] + r, item[1] + c]
            i_can, fieldx = try_to_place(temp_fgr, field, figure_index)
            if i_can == True:
                field = fieldx
                if figure_index == len(figures):
                    answer = field
                    for i in answer:
                        print(" ".join(list(map(str, i))))
                    exit()
                try_new_block(field, (figure_index + 1), figures)
                field = remove_figure(field, temp_fgr)
    return False


def print_figure(fgr):
    size = max(get_max_x(fgr), get_max_y(fgr))
    a = [["-"] * (size + 1) for i in range(size + 1)]
    for coord in fgr:
        a[coord[0]][coord[1]] = "X"
    for i in range(len(a)):
        print(" ".join(a[i]))


ind = 1
for i in range(num_of_rows + 1, len(inp)):
    for k in range(0, len(inp[i]), 2):
        figure.append([inp[i][k], inp[i][k + 1]])
    figures[ind] = rotate_figure(figure)
    ind += 1
    figure = []


def toString(List):
    return "".join(List)


def allLexicographicRecur(string, data, last, index):
    length = len(string)

    for i in range(length):

        data[index] = string[i]

        if index == last:
            # print(data)
            figures2 = use_list_for_rot(data)
            try_new_block(field, 1, figures2)
        else:
            allLexicographicRecur(string, data, last, index + 1)


def allLexicographic(string, length):

    data = [""] * (length)

    string = sorted(string)

    allLexicographicRecur(string, data, length - 1, 0)


def use_list_for_rot(comb):
    global figures
    figures2 = figures.copy()
    for idx, item in enumerate(comb):
        for i in range(item):
            figures2[idx + 1] = rotate_figure(figures2[idx + 1])
        # for k in range(len(figures2)):
        # print_figure(figures2[k + 1])
        # print()
    return figures2


number = [0, 1, 2, 3]
allLexicographic(number, len(figures))
