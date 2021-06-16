@cython.cclass
class Function:
    @cython.ccall
    @cython.locals(x=cython.double)
    @cython.exceptval(check=True)
    def evaluate(self, x) -> cython.double:
        return 0
