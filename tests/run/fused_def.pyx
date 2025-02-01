# mode: run

"""
Test Python def functions without extern types
"""

cy = __import__("cython")
cimport cython

cdef extern from *:
    int __Pyx_CyFunction_Check(object)

cdef class Base(object):
    def __repr__(self):
        return type(self).__name__


cdef class ExtClassA(Base):
    pass

cdef class ExtClassB(Base):
    pass

cdef enum MyEnum:
    entry0
    entry1
    entry2
    entry3
    entry4

ctypedef fused fused_t:
    str
    int
    long
    complex
    ExtClassA
    ExtClassB
    MyEnum


ctypedef ExtClassA xxxlast
ctypedef ExtClassB aaafirst


ctypedef fused fused_with_object:
    aaafirst
    object
    xxxlast
    int
    long


f = 5.6
i = 9


def opt_func(fused_t obj, cython.floating myf = 1.2, cython.integral myi = 7,
             another_opt = 2, yet_another_opt=3):
    """
    Test runtime dispatch, indexing of various kinds and optional arguments.
    Use 5 arguments because at one point the optional argument from the
    5th argument was overwriting that of the __pyx_fused dispatcher.
    https://github.com/cython/cython/issues/3511

    >>> opt_func("spam", f, i)
    str object double long
    spam 5.60 9 5.60 9
    >>> opt_func("spam", f, myi=i)
    str object double long
    spam 5.60 9 5.60 9
    >>> opt_func("spam", myf=f, myi=i)
    str object double long
    spam 5.60 9 5.60 9
    >>> opt_func[str, float, int]("spam", f, i)
    str object float int
    spam 5.60 9 5.60 9
    >>> opt_func[str, cy.double, cy.long]("spam", f, i)
    str object double long
    spam 5.60 9 5.60 9
    >>> opt_func[str, cy.double, cy.long]("spam", f, myi=i)
    str object double long
    spam 5.60 9 5.60 9
    >>> opt_func[str, float, cy.int]("spam", f, i)
    str object float int
    spam 5.60 9 5.60 9


    >>> opt_func(ExtClassA(), f, i)
    ExtClassA double long
    ExtClassA 5.60 9 5.60 9
    >>> opt_func[ExtClassA, float, int](ExtClassA(), f, i)
    ExtClassA float int
    ExtClassA 5.60 9 5.60 9
    >>> opt_func[ExtClassA, cy.double, cy.long](ExtClassA(), f, i)
    ExtClassA double long
    ExtClassA 5.60 9 5.60 9

    >>> opt_func(ExtClassB(), f, i)
    ExtClassB double long
    ExtClassB 5.60 9 5.60 9
    >>> opt_func[ExtClassB, cy.double, cy.long](ExtClassB(), f, i)
    ExtClassB double long
    ExtClassB 5.60 9 5.60 9

    >>> opt_func(10, f)
    long double long
    10 5.60 7 5.60 9
    >>> opt_func[int, float, int](10, f)
    int float int
    10 5.60 7 5.60 9

    >>> opt_func(10 + 2j, myf = 2.6)
    double complex double long
    (10+2j) 2.60 7 5.60 9
    >>> opt_func[cy.py_complex, float, int](10 + 2j, myf = 2.6)
    double complex float int
    (10+2j) 2.60 7 5.60 9
    >>> opt_func[cy.doublecomplex, cy.float, cy.int](10 + 2j, myf = 2.6)
    double complex float int
    (10+2j) 2.60 7 5.60 9

    >>> opt_func(object(), f)
    Traceback (most recent call last):
    TypeError: Function call with ambiguous argument types
    >>> opt_func()
    Traceback (most recent call last):
    TypeError: Expected at least 1 argument, got 0
    >>> opt_func("abc", f, i, 5, 5, 5)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...at most 5...
    >>> opt_func[ExtClassA, cy.float, cy.long](object(), f)
    Traceback (most recent call last):
    TypeError: Argument 'obj' has incorrect type (expected fused_def.ExtClassA, got object)
    """
    print cython.typeof(obj), cython.typeof(myf), cython.typeof(myi)
    print obj, "%.2f" % myf, myi, "%.2f" % f, i

def non_fused_opt(fused_t obj, value=5):
    """
    PyObject constants as parts of fused functions weren't being created correctly
    which would lead this to crash
    >>> non_fused_opt(0)
    5
    >>> non_fused_opt("str", 10)
    10
    """
    print value

def run_cyfunction_check():
    """
    tp_base of the fused function was being set incorrectly meaning
    it wasn't being identified as a CyFunction
    >>> run_cyfunction_check()
    fused_cython_function
    1
    """
    print(type(opt_func).__name__.rsplit('.', 1)[-1])
    print(__Pyx_CyFunction_Check(opt_func))  # should be True

def test_opt_func():
    """
    >>> test_opt_func()
    str object double long
    ham 5.60 4 5.60 9
    """
    opt_func("ham", f, entry4)


def test_opt_func_introspection():
    """
    >>> opt_func.__defaults__
    (1.2, 7, 2, 3)
    >>> opt_func.__kwdefaults__
    >>> opt_func.__annotations__
    {}

    >>> opt_func[str, float, int].__defaults__
    (1.2, 7, 2, 3)
    >>> opt_func[str, float, int].__kwdefaults__
    >>> opt_func[str, float, int].__annotations__
    {}

    >>> opt_func[str, cy.double, cy.long].__defaults__
    (1.2, 7, 2, 3)
    >>> opt_func[str, cy.double, cy.long].__kwdefaults__
    >>> opt_func[str, cy.double, cy.long].__annotations__
    {}
    """


def func_with_object(fused_with_object obj, cython.integral myi = 7):
    """
    >>> func_with_object(1)
    long long
    1 7
    >>> func_with_object(1, 3)
    long long
    1 3
    >>> func_with_object['int', 'int'](1, 3)
    int int
    1 3
    >>> func_with_object(1j, 3)
    Python object long
    1j 3
    >>> func_with_object('abc', 3)
    Python object long
    abc 3
    >>> func_with_object(ExtClassA(), 3)
    xxxlast long
    ExtClassA 3
    >>> func_with_object(ExtClassB(), 3)
    aaafirst long
    ExtClassB 3
    >>> func_with_object['object', 'long'](ExtClassA(), 3)
    Python object long
    ExtClassA 3
    >>> func_with_object['object', 'long'](ExtClassB(), 3)
    Python object long
    ExtClassB 3
    """
    print cython.typeof(obj), cython.typeof(myi)
    print obj, myi



def args_kwargs(fused_t obj, cython.floating myf = 1.2, *args, **kwargs):
    """
    >>> args_kwargs("foo")
    str object double
    foo 1.20 5.60 () {}

    >>> args_kwargs("eggs", f, 1, 2, [], d={})
    str object double
    eggs 5.60 5.60 (1, 2, []) {'d': {}}

    >>> args_kwargs[str, float]("eggs", f, 1, 2, [], d={})
    str object float
    eggs 5.60 5.60 (1, 2, []) {'d': {}}

    """
    print cython.typeof(obj), cython.typeof(myf)
    print obj, "%.2f" % myf, "%.2f" % f, args, kwargs


class BaseClass(object):
    """
    Test fused class/static/normal methods and super() without args
    """

    @staticmethod
    def mystaticmethod(cython.integral arg1):
        print cython.typeof(arg1), arg1

    @classmethod
    def myclassmethod(cls, cython.integral arg1):
        print cls, cython.typeof(arg1), arg1

    def normalmethod(self, cython.integral arg1):
        print self, cython.typeof(arg1), arg1

    def __repr__(self):
        return "<%s.%s object>" % (__name__, type(self).__name__)

class SubClass(BaseClass):

    @staticmethod
    def mystaticmethod(self, cython.integral arg1):
        print cython.typeof(arg1), arg1
        super().mystaticmethod(arg1 + 1)

    @classmethod
    def myclassmethod(cls, cython.integral arg1):
        print cls, cython.typeof(arg1), arg1
        super().myclassmethod(arg1 + 1)

    def normalmethod(self, cython.integral arg1):
        print self, cython.typeof(arg1), arg1
        super().normalmethod(arg1 + 1)

class SubSubClass(SubClass):
    pass

def test_fused_def_super():
    """
    >>> test_fused_def_super()
    long 10
    long 11
    long 11
    long 12
    short 12
    long 13
    short 13
    long 14
    <class 'fused_def.SubClass'> long 14
    <class 'fused_def.SubClass'> long 15
    <class 'fused_def.SubClass'> long 15
    <class 'fused_def.SubClass'> long 16
    <class 'fused_def.SubClass'> short 16
    <class 'fused_def.SubClass'> long 17
    <class 'fused_def.SubClass'> short 17
    <class 'fused_def.SubClass'> long 18
    <fused_def.SubClass object> long 18
    <fused_def.SubClass object> long 19
    <fused_def.SubClass object> long 19
    <fused_def.SubClass object> long 20
    <fused_def.SubClass object> short 20
    <fused_def.SubClass object> long 21
    <fused_def.SubClass object> short 21
    <fused_def.SubClass object> long 22
    """
    obj = SubClass()
    cls = SubClass

    obj.mystaticmethod(obj, 10)
    cls.mystaticmethod(obj, 11)
    obj.mystaticmethod[cy.short](obj, 12)
    cls.mystaticmethod[cy.short](obj, 13)

    obj.myclassmethod(14)
    cls.myclassmethod(15)
    obj.myclassmethod[cy.short](16)
    cls.myclassmethod[cy.short](17)

    obj.normalmethod(18)
    cls.normalmethod(obj, 19)
    obj.normalmethod[cy.short](20)
    cls.normalmethod[cy.short](obj, 21)

def test_fused_def_classmethod():
    """
    >>> test_fused_def_classmethod()
    <class 'fused_def.SubSubClass'> long 10
    <class 'fused_def.SubSubClass'> long 11
    <class 'fused_def.SubSubClass'> long 11
    <class 'fused_def.SubSubClass'> long 12
    <class 'fused_def.SubSubClass'> short 12
    <class 'fused_def.SubSubClass'> long 13
    <class 'fused_def.SubSubClass'> short 13
    <class 'fused_def.SubSubClass'> long 14
    """
    SubSubClass().myclassmethod(10)
    SubSubClass.myclassmethod(11)

    SubSubClass().myclassmethod[cy.short](12)
    SubSubClass.myclassmethod[cy.short](13)

cdef class CBaseClass(object):
    """
    Test fused def and cpdef methods in cdef classes.

    >>> import cython as cy
    >>> obj = CBaseClass()
    >>> cls = CBaseClass

    >>> obj.mystaticmethod(10)
    long 10
    >>> obj.mystaticmethod[cy.short](10)
    short 10
    >>> cls.mystaticmethod(10)
    long 10
    >>> cls.mystaticmethod[cy.short](10)
    short 10

    >>> obj.myclassmethod(10)
    CBaseClass long 10
    >>> obj.myclassmethod[cy.short](10)
    CBaseClass short 10
    >>> cls.myclassmethod(10)
    CBaseClass long 10
    >>> cls.myclassmethod[cy.short](10)
    CBaseClass short 10

    >>> obj.normalmethod(10, 11, 12)
    <fused_def.CBaseClass object> long 10 11 12
    >>> obj.normalmethod[cy.short](10, 11, 12)
    <fused_def.CBaseClass object> short 10 11 12
    >>> cls.normalmethod(obj, 10, 11, 12)
    <fused_def.CBaseClass object> long 10 11 12
    >>> cls.normalmethod[cy.short](obj, 10, 11, 12)
    <fused_def.CBaseClass object> short 10 11 12

    >>> obj.cpdefmethod(10)
    <fused_def.CBaseClass object> long 10
    >>> obj.cpdefmethod[cy.short](10)
    <fused_def.CBaseClass object> short 10
    >>> cls.cpdefmethod(obj, 10)
    <fused_def.CBaseClass object> long 10
    >>> cls.cpdefmethod[cy.short](obj, 10)
    <fused_def.CBaseClass object> short 10
    """

    @staticmethod
    def mystaticmethod(cython.integral arg1):
        print cython.typeof(arg1), arg1

    @classmethod
    def myclassmethod(cls, cython.integral arg1):
        print cls.__name__, cython.typeof(arg1), arg1

    def normalmethod(self, cython.integral arg1, arg2, arg3):
        print self, cython.typeof(arg1), arg1, arg2, arg3

    cpdef cpdefmethod(self, cython.integral arg1):
        print self, cython.typeof(arg1), arg1

    def __repr__(self):
        return "<%s.%s object>" % (__name__, type(self).__name__)

def getcode(func):
    return getattr(func, '__code__', None) or func.func_code

def test_code_object(cython.floating dummy = 2.0):
    """
    A test for default arguments is in cyfunction_defaults

    >>> test_code_object.__code__ is not test_code_object[float].__code__
    True
    """

def create_dec(value):
    def dec(f):
        if not hasattr(f, 'order'):
            f.order = []
        f.order.append(value)
        return f
    return dec

@create_dec(1)
@create_dec(2)
@create_dec(3)
def test_decorators(cython.floating arg):
    """
    >>> test_decorators.order
    [3, 2, 1]
    """

@cython.binding(True)
def bind_me(self, cython.floating a=1.):
    return a

cdef class HasBound:
    """
    Using default arguments of bound specialized fused functions used to cause a segfault
    https://github.com/cython/cython/issues/3370
    >>> inst = HasBound()
    >>> inst.func()
    1.0
    >>> inst.func(2)
    2.0
    >>> inst.func_fused()
    1.0
    >>> inst.func_fused(2.)
    2.0
    >>> bind_me.__defaults__
    (1.0,)
    >>> inst.func.__defaults__
    (1.0,)
    >>> inst.func_fused.__defaults__
    (1.0,)
    """
    func = bind_me[float]

    func_fused = bind_me



ctypedef fused IntOrFloat1:
    int
    float

ctypedef fused IntOrFloat2:
    int
    float

ctypedef fused IntOrFloat3:
    int
    float

def really_simple_fused_function(IntOrFloat1 a, IntOrFloat2 b, IntOrFloat3 c):
    # Don't use this function for anything except the thread safety stress test.
    # The first call should be from that.
    return (a + 1) * 2 + (b*c)

def run_really_simple_fused_function(start_barrier, n_iters, failed_list):
    # Maximize the chance of failure by waiting until all threads are ready to start
    args = [ n if n % 2 else float(n) for n in range(n_iters) ]
    try:
        start_barrier.wait()
        for a in args:
            really_simple_fused_function(a, a, a)
    except:
        failed_list.append(True)


def stress_test_thread_safety(n_threads):
    """
    >>> stress_test_thread_safety(20)
    """
    from threading import Barrier, Thread
    start_barrier = Barrier(n_threads)

    failed_list = []

    threads = [
        Thread(
            target=run_really_simple_fused_function,
            args=[start_barrier, 30, failed_list]
        ) for _ in range(n_threads) ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not failed_list, len(failed_list)
