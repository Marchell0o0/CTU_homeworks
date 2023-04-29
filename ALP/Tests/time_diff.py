
x = input().replace('h', ' ').replace('m', ' ').replace('s', ' ').split()
y = input().replace('h', ' ').replace('m', ' ').replace('s', ' ').split()


def check_error(x):
    if len(x) != 3:
        return True
    for idx, item in enumerate(x):
        if len(item) != 2:
            return True
        if idx == 0 and int(item) > 12:
            return True
        if idx != 0 and int(item) >= 60:
            return True
        return False


def to_seconds(x):
    return int(x[0])*3600 + int(x[1])*60 + int(x[2])


def from_seconds(x):
    hours = x // 3600
    x -= hours*3600
    minutes = x // 60
    x -= minutes*60
    res = [hours, minutes, x]
    for idx, item in enumerate(res):
        if item < 10:
            res[idx] = str('0' + str(abs(item)))
        else:
            res[idx] = str(abs(item))
    return res[0] + 'h' + res[1] + 'm' + res[2] + 's'


if check_error(x) or check_error(y):
    print("ERROR")
else:
    print(from_seconds(to_seconds(x)-to_seconds(y)))
