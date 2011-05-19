import cython
from cython import cfunc, cclass, ccall

@cython.test_assert_path_exists('//CFuncDefNode')
@cython.cfunc
def ftang():
    x = 0

@cython.test_assert_path_exists('//CFuncDefNode')
@cfunc
def fpure(a):
    return a*2

def test():
    """
    >>> test()
    4
    """
    ftang()
    return fpure(2)

with cfunc:
    @cython.test_assert_path_exists('//CFuncDefNode')
    def fwith1(a):
        return a*3

    @cython.test_assert_path_exists('//CFuncDefNode')
    def fwith2(a):
        return a*4

with cclass:
    @cython.test_assert_path_exists('//CClassDefNode')
    class Egg(object):
        pass
    @cython.test_assert_path_exists('//CClassDefNode')
    class BigEgg(object):
        @cython.test_assert_path_exists('//CFuncDefNode')
        @cython.cfunc
        def f(self, a):
            return a*10

def test_with():
    """
    >>> test_with()
    (3, 4, 50)
    """
    return fwith1(1), fwith2(1), BigEgg().f(5)

@cython.test_assert_path_exists('//CClassDefNode')
@cython.cclass
class PureFoo(object):
    a = cython.declare(cython.double)

    def __init__(self, a):
        self.a = a

    def __call__(self):
        return self.a

    @cython.test_assert_path_exists('//CFuncDefNode')
    @cython.cfunc
    def puremeth(self, a):
        return a*2

def test_method():
    """
    >>> test_method()
    4
    True
    """
    x = PureFoo(2)
    print(x.puremeth(2))
    if cython.compiled:
        print(isinstance(x(), float))
    else:
        print(True)
    return

@cython.ccall
def ccall_sqr(x):
    return x*x

@cclass
class Overidable(object):
    @ccall
    def meth(self):
        return 0

def test_ccall():
    """
    >>> test_ccall()
    25
    >>> ccall_sqr(5)
    25
    """
    return ccall_sqr(5)

def test_ccall_method(x):
    """
    >>> test_ccall_method(Overidable())
    0
    >>> Overidable().meth()
    0
    >>> class Foo(Overidable):
    ...    def meth(self):
    ...        return 1
    >>> test_ccall_method(Foo())
    1
    >>> Foo().meth()
    1
    """
    return x.meth()
