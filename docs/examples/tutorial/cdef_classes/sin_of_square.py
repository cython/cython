if cython.compiled:
    from cython.cimports.libc.math import sin
else:
    from math import sin

@cython.cclass
class Function:
    @cython.ccall
    @cython.locals(x=cython.double)
    def evaluate(self, x) -> cython.double:
        return 0

@cython.cclass
class SinOfSquareFunction(Function):
    @cython.ccall
    @cython.locals(x=cython.double)
    def evaluate(self, x) -> cython.double:
        return sin(x ** 2)
