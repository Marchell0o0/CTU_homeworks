import random
from collections import Counter

p = {1: 0, 2: 7/36, 3: 1/36, 4: 8/36, 5: 2/36, 6: 9/36, 7:3/36, 8: 2/36, 9: 2/36, 10:1/36, 11: 1/36}

def roll_die():
    return random.randint(1,6)

def throw():
    result = roll_die()
    if result % 2 == 0:
        return result
    else:
        return result + roll_die()

def expected_value(c: Counter):
    return sum(i*c[i] for i in c.keys()) / sum(c.values())

if __name__ == "__main__":
    N = int(1e6)
    prec = 4
    c = Counter(throw() for _ in range(N))
    print(c)
    for i in range(1, 7):
        print(f"p_H({i})     | Theory: {p[i]:.{prec}f}    |   Sim: {c[i]/N:.{prec}f}")
    print(f"\n Expected value    | Theory: {189/36:.{prec}f}    |   Sim: {expected_value(c):.{prec}f}")