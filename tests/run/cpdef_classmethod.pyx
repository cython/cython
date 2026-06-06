# mode: run
# tag: cpdef

cimport cython


# ------------------------------------------------------------------
# Test 1: basic explicit cpdef classmethod
# ------------------------------------------------------------------

cdef class Basic:
    @classmethod
    cpdef object tag(cls):
        return cls.__name__

    cdef object c_call_tag(self):
        # Direct C-level call: pass cls explicitly since Cython resolves
        # Basic.tag to the C function rather than the classmethod descriptor.
        return Basic.tag(type(self))


def test_basic():
    """
    >>> test_basic()
    ('Basic', 'Basic', 'Basic')
    """
    obj = Basic()
    # (<object>Basic).tag() forces Python attribute lookup, which invokes
    # the classmethod descriptor and then the Python wrapper (→ C function).
    return (<object>Basic).tag(), (<object>obj).tag(), obj.c_call_tag()


# ------------------------------------------------------------------
# Test 2: cpdef classmethod with multiple args
# ------------------------------------------------------------------

cdef class MultiArgs:
    @classmethod
    cpdef object meth(cls, int x, object y):
        return (cls.__name__, x, y)

    cdef object c_call_meth(self, int x, object y):
        return MultiArgs.meth(type(self), x, y)


def test_multi_args():
    """
    >>> test_multi_args()
    (('MultiArgs', 1, 'hello'), ('MultiArgs', 2, 'world'))
    """
    obj = MultiArgs()
    return (<object>MultiArgs).meth(1, 'hello'), obj.c_call_meth(2, 'world')


# ------------------------------------------------------------------
# Test 3: @cython.final cdef class with cpdef classmethod
# ------------------------------------------------------------------

@cython.final
cdef class FinalCls:
    @classmethod
    cpdef object tag(cls):
        return cls.__name__

    cdef object c_call_tag(self):
        return FinalCls.tag(type(self))


def test_final():
    """
    >>> test_final()
    ('FinalCls', 'FinalCls', 'FinalCls')
    """
    obj = FinalCls()
    return (<object>FinalCls).tag(), (<object>obj).tag(), obj.c_call_tag()


# ------------------------------------------------------------------
# Test 4: 4-level cdef class inheritance
# ------------------------------------------------------------------

cdef class L0:
    @classmethod
    cpdef object tag(cls):
        return 'L0'

    cdef object c_tag(self):
        return L0.tag(type(self))


cdef class L1(L0):
    @classmethod
    cpdef object tag(cls):
        return 'L1'

    cdef object c_tag(self):
        return L1.tag(type(self))


cdef class L2(L1):
    @classmethod
    cpdef object tag(cls):
        return 'L2'

    cdef object c_tag(self):
        return L2.tag(type(self))


cdef class L3(L2):
    @classmethod
    cpdef object tag(cls):
        return 'L3'

    cdef object c_tag(self):
        return L3.tag(type(self))


def test_inheritance():
    """
    >>> test_inheritance()
    ('L0', 'L1', 'L2', 'L3', 'L0', 'L1', 'L2', 'L3')
    """
    l0, l1, l2, l3 = L0(), L1(), L2(), L3()
    return ((<object>L0).tag(), (<object>L1).tag(), (<object>L2).tag(), (<object>L3).tag(),
            l0.c_tag(), l1.c_tag(), l2.c_tag(), l3.c_tag())


# ------------------------------------------------------------------
# Test 5: Python subclass override
# The cpdef C function always runs the defining class body (no
# OverrideCheckNode for classmethods). Python dispatch via the
# classmethod descriptor reaches the Python override correctly.
# ------------------------------------------------------------------

def test_python_subclass_override():
    """
    >>> test_python_subclass_override()
    ('L1', 'PyChild')
    """
    class PyChild(L1):
        @classmethod
        def tag(cls):
            return 'PyChild'

    c_result = L1().c_tag()    # C function always returns 'L1'
    py_result = PyChild.tag()  # Python dispatch reaches the override
    return c_result, py_result


# ------------------------------------------------------------------
# Test 6: python_subclassing=False with cpdef classmethod
# ------------------------------------------------------------------

@cython.python_subclassing(False)
cdef class NoSubclass:
    @classmethod
    cpdef object tag(cls):
        return cls.__name__

    cdef object c_call_tag(self):
        return NoSubclass.tag(type(self))


def test_no_subclassing():
    """
    >>> test_no_subclassing()
    ('NoSubclass', 'NoSubclass')
    """
    obj = NoSubclass()
    return (<object>NoSubclass).tag(), obj.c_call_tag()


def test_no_subclassing_prevents_subclass():
    """
    >>> try:
    ...     class Child(NoSubclass): pass
    ... except TypeError:
    ...     print(True)
    True
    """


# ------------------------------------------------------------------
# Test 7: auto_cpdef promotion of @classmethod def
# ------------------------------------------------------------------

@cython.auto_cpdef(True)
cdef class AutoCls:
    @classmethod
    def tag(cls):
        return cls.__name__

    cdef object c_call_tag(self):
        return AutoCls.tag(type(self))


def test_auto_cpdef():
    """
    >>> test_auto_cpdef()
    ('AutoCls', 'AutoCls', 'AutoCls')
    """
    obj = AutoCls()
    return (<object>AutoCls).tag(), (<object>obj).tag(), obj.c_call_tag()
