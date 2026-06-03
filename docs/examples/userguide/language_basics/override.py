@cython.cclass
class A:
    @cython.cfunc
    def foo(self):
        print("A")

@cython.cclass
class B(A):
    @cython.ccall
    def foo(self):
        print("B")

class C(B):  # NOTE: no cclass decorator
    def foo(self):
        print("C")
