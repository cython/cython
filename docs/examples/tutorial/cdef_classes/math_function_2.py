@cython.cclass
class Function:
    @cython.ccall
    def evaluate(self, x: cython.double) -> cython.double:
        return 0
