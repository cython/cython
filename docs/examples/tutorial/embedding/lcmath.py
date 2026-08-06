def add(a, b):
    return a + b

@cython.ccall
def sub(a: cython.int, b: cython.int) -> cython.int:
    return a - b
