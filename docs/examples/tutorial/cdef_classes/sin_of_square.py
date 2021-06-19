if cython.compiled:
    from cython.cimports.libc.math import sin
else:
    from math import sin

@cython.cclass
class Function:
    @cython.ccall
    def evaluate(self, x: cython.double) -> cython.double:
        return 0

@cython.cclass
class SinOfSquareFunction(Function):
    @cython.ccall
    def evaluate(self, x: cython.double) -> cython.double:
        return sin(x ** 2)
