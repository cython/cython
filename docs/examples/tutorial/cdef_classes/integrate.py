from cython.cimports.sin_of_square import Function, SinOfSquareFunction

def integrate(f: Function, a: float, b: float, N: cython.int):
    i: cython.int

    if f is None:
        raise ValueError("f cannot be None")

    s: float = 0
    dx: float = (b - a) / N

    for i in range(N):
        s += f.evaluate(a + i * dx)

    return s * dx

print(integrate(SinOfSquareFunction(), 0, 1, 10000))
