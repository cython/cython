from cython.cimports.sin_of_square import Function, SinOfSquareFunction

def integrate(f: Function, a: cython.double, b: cython.double, N: cython.int):
    i: cython.int

    if f is None:
        raise ValueError("f cannot be None")

    s: cython.double = 0
    dx: cython.double = (b - a) / N

    for i in range(N):
        s += f.evaluate(a + i * dx)

    return s * dx

print(integrate(SinOfSquareFunction(), 0, 1, 10000))
