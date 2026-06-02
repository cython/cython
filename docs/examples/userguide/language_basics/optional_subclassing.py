@cython.cclass
class A:
    @cython.cfunc
    def foo(self):
        print("A")

@cython.cclass
class B(A):
    @cython.cfunc
    def foo(self, x=None):
        print("B", x)

@cython.cclass
class C(B):
    @cython.ccall
    def foo(self, x=True, k:cython.int = 3):
        print("C", x, k)
