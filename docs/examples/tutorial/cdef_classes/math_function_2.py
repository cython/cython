@cython.cclass
class Function:
    @cython.ccall
    @cython.locals(x=cython.double)
    def evaluate(self, x) -> cython.double:
        return 0
