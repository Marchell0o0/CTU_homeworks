x = float(input())

def f(a):
    return 2**a

def log(x):
    M = 0
    if x > 1:
        L = 0 
        R = x
    elif x < 1: 
        L = -(1/x)
        R = 0
    else: 
        return 0
    while abs(R-L) > 1e-9:
        M1 = M
        M = (L+R)/2
        if M == M1:
            return M
        if f(M) > x:
            R = M
        if f(M) < x:
            L = M
    return M    
print(log(x))