x1 = input()
y1 = input()
x = list(map(float, x1.split()))
y = list(map(float, y1.split()))


def mainfunc(x, y):
    return ((x**2) / 2) * ((1 - y) ** 2) + ((x - 2) ** 3) - (2 * y) + x


curmax = mainfunc(x[0], y[0])
curmin = mainfunc(x[0], y[0]) * (x[0] + 2) * (y[0] - 2)
biggest_pair = 0
smallest_pair = 0
count = 0

if len(x) != len(y):
    print("ERROR")
else:
    for i in range(len(x)):
        calc = mainfunc(x[i], y[i])
        calc2 = calc * (x[i] + 2) * (y[i] - 2)
        if curmax < calc:
            curmax = calc
            biggest_pair = i
        if calc < 0:
            count += 1
        if curmin > calc2:
            curmin = calc2
            smallest_pair = i
    print(biggest_pair, count, smallest_pair)
