import math
base = int(input())
x = list(map(str, (input())))
y = list(map(str, (input())))

def checkCorrect(x, base):
    error = 0
    if x.count('.') > 1:
        error = 1
        return error
    for i in range(len(x)):
        if ord(x[i]) == 46:
            continue
        else:
            if ord(x[i]) > 96:
                x[i] = ord(x[i]) - 87
            if int(x[i]) > base-1:
                error = 1
                return error
    return error

def pointIndex(x):
    if x.count('.') > 0:
        y = x.index('.')
        return y
    else:
        return None

def removePoint(p1, p2, x, y):
    if p1 != None or p2 != None:
        numsAfterDot = (len(x) - p1 - 1) + (len(y) - p2 - 1)
        x.remove('.')
        y.remove('.')
    return numsAfterDot

def swap(x, y):
    if len(x) < len(y):
        x, y = y, x
    


def iteration(x, y, base):
    carry = 0
    mul = 0
    rem = 0
    dct = {}
    iterator = []
    for p in range(1, len(y)+1):
        for o in range(1, len(x)+1):
            mul = int(int(y[-p]) * int(x[-o]))
            mul += carry
            rem = mul % base
            carry = mul // base
            iterator.insert(0, rem)
        iterator.insert(0, carry)
        for i in range(p-1):
            iterator.append(0)
        dct[p-1] = iterator
        iterator = []
        carry = 0
    return dct

def addZeros(dctlen, dct):
    for i in range(dctlen):
        while len(dct[i]) < len(dct[dctlen-1]):
            dct[i].insert(0, 0)

def add(dct, base, dctlen):
    result = []
    iterator = []
    carry = 0
    sum = 0
    p = len(dct[dctlen-1])
    for x in range(1, p+1):
        sum = 0
        for y in range(dctlen):
            iterator = dct[y]
            sum += iterator[-x]
        sum += carry
        rem = sum % base
        carry = sum // base
        result.insert(0, rem)
    return result



def backToLetters(nums):
    for i in range(len(nums)):
        if nums[i] > 9:
            nums[i] = chr(nums[i] + 87)
def setPoint(p1, p2, nums, numsAfterDot):
    if p1 != None or p2 != None:
        nums.insert(len(nums)-numsAfterDot, '.')

def removeZeros(nums):
    for i in range(((nums.index('.')-1))):
        if nums[0] == 0 and ord(str(nums[1])) != 46:
            del nums[0]
        else:
            break
    while nums[-1] == 0:
        del nums[-1]

if checkCorrect(x, base) == 0 and checkCorrect(y, base) == 0:
    p1 = pointIndex(x)
    p2 = pointIndex(y)
    numsAfterDot = removePoint(p1, p2, x, y)
    swap(x, y)
    dctlen = len(y)
    dct = iteration(x, y, base)
    addZeros(dctlen, dct)
    nums = add(dct, base, dctlen)
    backToLetters(nums)
    setPoint(p1,p2,nums,numsAfterDot)
    removeZeros(nums)
    print("".join(map(str, nums)))
else:
    print('ERROR')

    
 

