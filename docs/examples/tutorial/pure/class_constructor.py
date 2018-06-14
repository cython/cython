import cython

class A:
    cython.declare(a=cython.int, b=cython.int)

    def __init__(self, b=0):
        self.a = 3
        self.b = b
