from sys import argv
from time import time

n = int(argv[1])
inp = list(map(int, input().split()))


def SieveOfEratosthenes(num):
    res = []
    prime = [True] * (num + 1)
    p = 2
    while p * p <= num:
        if prime[p] == True:

            for i in range(p * p, num + 1, p):
                prime[i] = False
        p += 1
    for p in range(2, num + 1):
        if prime[p]:
            res.append(p)
    return res


def findPQ(n, n2):
    primes = SieveOfEratosthenes(n2)
    n3 = n
    factors = []
    for item in primes:
        while n3 % item == 0:
            n3 = n3 / item
            factors.append(item)
    return factors


def findfi(p, q):
    return (p - 1) * (q - 1)


def ExtEuclid(a, b):
    Aa, Ba = 1, 0  # a = 1 * a + 0 * b
    Ab, Bb = 0, 1  # b = 0 * a + 1 * b
    # Prohodíme, je-li třeba
    if b > a:
        a, b = b, a
        Aa, Ab = Ab, Aa
        Ba, Bb = Bb, Ba
    # Zde je vždy a >= b
    while b > 0:
        # Odečteme od proměnné a proměnnou b
        # tolikrát, kolikrát se tam vejde.
        # ("//" značí celočíselné dělení)
        Aa = Aa - (a // b) * Ab
        Ba = Ba - (a // b) * Bb
        # nsd(a % b, b) = nsd(a, b).
        a = a % b
        # Prohodíme
        a, b = b, a
        Aa, Ab = Ab, Aa
        Ba, Bb = Bb, Ba
    # nsd(0, a) = a.
    # Vrátíme také Bézoutovy koeficienty.
    return a, Aa, Ba


def Euclid(a, b):
    # Prohodíme, je-li třeba
    if b > a:
        a, b = b, a

    # Zde je vždy a >= b
    while b > 0:
        # nsd(a % b, b) = nsd(a, b).
        a = a % b
        a, b = b, a

    # nsd(0, a) = a.
    return a


def finde(i, fi):
    return ExtEuclid(i, fi)[0] == 1


def findd(e, fi):
    return ExtEuclid(e, fi)[1] + fi


def decode(x):
    res = []
    for item in x:
        block = []
        for _ in range(0, 4):
            k = item % 256
            if k < 123 and k != 0:
                block.insert(0, chr(k))
            item = item // 256
        res.append("".join(block))
    return "".join(res)


# start = time()

p, q = findPQ(n, int(n**0.5) * 10)
fi = findfi(p, q)
possible_d = []

# end = time()
# print("poisk p q fi", end - start)


# start = time()

for e in range(2**18, 2**20):
    if finde(e, fi):
        possible_d.append(findd(e, fi))

# end = time()
# print("poisk e d", end - start)


matches = {"Tento", "predmet", "proste", "nejlepsi", "genialni"}
temp = str()

# print("zapuskajem deshifrovku...")

# start = time()

for d in possible_d:
    decrypted_ascii = [pow(x, d, n) for x in inp]
    temp = decode(decrypted_ascii)
    print(temp)
    if matches & set(temp.split()):
        if "\0x0" in temp:
            temp.replace("\0x0", "")
        print(temp)
        break


# end = time()
# print("finish", end - start)
