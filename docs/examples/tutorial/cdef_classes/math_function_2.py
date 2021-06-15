@cython.cclass
class Function:
    @cython.ccall
    @cython.exceptval(check=True)
    def evaluate(self, x: cython.double) -> cython.double:
        return 0
