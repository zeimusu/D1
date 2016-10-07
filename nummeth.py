def sample_cubic(x):
    return x**3 - 2*x - 1

def Dsample_cubic(x):
    return 3*x**2 - 2

def sign(x):
    if x<0: 
        return -1
    else:
        return 1

def bisection(f,a,b,fa,fb):
    """given a function, f, and an interval [a,b] in which f changes sign
    return a new interval [x,y] in which f changes sign, and the values of 
    f at the end points """
    midpoint = (a + b)/2
    fm = f(midpoint)
    if sign(fa) == sign(fm):
        return midpoint,b,fm,fb
    else:
        return a,midpoint,fa,fm


def interpolation(f,a,b,fa,fb):
    """given a function and an interval [a, b] in which f changes sign, 
    return a new interval [x,y] in which one endpoint is found by 
    interpolation and f changes sign"""
    x = (a - b) * fa / (fb - fa) + a
    fx = f(x)
    if sign(fx) == sign(fa):
        return x,b,fx,fb,x
    else:
        return a,x,fa,fx,x

def NR(f,df,x):
    """"
    Newton Raphson method, given a function and its derivative, and an
    initial estimate use Newton-Raphson to return an improved estimate
    """
    return x - f(x)/df(x)

def test():
    f = sample_cubic
    df = Dsample_cubic
    A, B = 1, 2
    loops = 10
    solution = 1.618033988749895

    print("Bisection")
    a, b= A, B
    fa = f(a)
    fb = f(b)
    for i in range(loops):
        a, b, fa, fb = bisection(f,a,b,fa,fb)
        print( a, b, 100*abs(a - solution)/solution )
    
    print()
    print("interpolation")
    a, b =A, B
    fa, fb = f(a), f(b)
    for i in range(loops):
        a, b,fa,fb,x = interpolation(f,a,b,fa,fb)
        print(x, 100*abs(x-solution)/solution)
    
    print()
    print("Newton Raphson")
    x = A
    for i in range(loops):
        x = NR(f,df,x)
        print(x, 100*abs(x-solution)/solution)
    
test()




