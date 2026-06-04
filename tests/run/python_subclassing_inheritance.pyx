# mode: run
# tag: directive, cpdef

cimport cython


# ============================================================
# 1. Basic late-enable: Base(False), Derived(@True)
#    Python subclass overrides inherited method via trampoline.
# ============================================================

@cython.python_subclassing(False)
cdef class Base1:
    @cython.test_fail_if_path_exists("//OverrideCheckNode")
    cpdef int method(self):
        return 1

    @cython.test_fail_if_path_exists("//OverrideCheckNode")
    cpdef int method2(self):
        return 10


@cython.python_subclassing(True)
cdef class Derived1(Base1):
    pass   # method and method2 inherited; trampolines synthesised automatically


class _PySub1(Derived1):
    def method(self):
        return 99


def test_basic_late_enable():
    """
    >>> test_basic_late_enable()
    99 1 10
    """
    s = _PySub1()
    cdef Derived1 d = Derived1()
    print("%d %d %d" % (s.method(), d.method(), d.method2()))


def test_direct_derived_call():
    """
    >>> test_direct_derived_call()
    1
    """
    cdef Derived1 d = Derived1()
    return d.method()


# ============================================================
# 2. Lock propagation: Base(False), Mid(@True), Leaf (no decorator)
#    Leaf automatically inherits True; Python subclasses of Leaf work.
# ============================================================

@cython.python_subclassing(False)
cdef class Base2:
    cpdef int value(self):
        return 2


@cython.python_subclassing(True)
cdef class Mid2(Base2):
    pass   # trampoline synthesised for value()


cdef class Leaf2(Mid2):
    pass   # inherits locked True; Mid's trampoline covers value()


class _PyLeaf2(Leaf2):
    def value(self):
        return 42


def test_lock_propagation():
    """
    >>> test_lock_propagation()
    42 2
    """
    s = _PyLeaf2()
    cdef Leaf2 d = Leaf2()
    print("%d %d" % (s.value(), d.value()))


def test_leaf_python_subclass_allowed():
    """
    >>> test_leaf_python_subclass_allowed()
    ok
    """
    try:
        class S(Leaf2): pass
        print("ok")
    except TypeError:
        print("failed")


# ============================================================
# 3. Deep gap: A(False), B(False, no override), C(@True)
#    C gets trampolines for A's methods even though B is in between.
# ============================================================

@cython.python_subclassing(False)
cdef class DeepA:
    cpdef int deep_method(self):
        return 3


@cython.python_subclassing(False)
cdef class DeepB(DeepA):
    pass   # does NOT override deep_method


@cython.python_subclassing(True)
cdef class DeepC(DeepB):
    pass   # trampoline synthesised for deep_method (inherited through B from A)


class _PyDeepC(DeepC):
    def deep_method(self):
        return 333


def test_deep_gap():
    """
    >>> test_deep_gap()
    333 3
    """
    s = _PyDeepC()
    cdef DeepC d = DeepC()
    print("%d %d" % (s.deep_method(), d.deep_method()))


# ============================================================
# 4. Mid override: A(False), B(False, overrides method), C(@True)
#    Trampoline in C calls B.method (not A.method).
# ============================================================

@cython.python_subclassing(False)
cdef class MidA:
    cpdef int calc(self):
        return 10


@cython.python_subclassing(False)
cdef class MidB(MidA):
    @cython.test_fail_if_path_exists("//OverrideCheckNode")
    cpdef int calc(self):
        return 20   # B overrides calc (False class — no OverrideCheckNode)


@cython.python_subclassing(True)
cdef class MidC(MidB):
    @cython.test_assert_path_exists("//OverrideCheckNode")
    cpdef int own_method(self):   # user-written method on re-enabled class — must have OverrideCheckNode
        return 42


class _PyMidC(MidC):
    def calc(self):
        return 200


def test_mid_override():
    """
    >>> test_mid_override()
    200 20 42
    """
    s = _PyMidC()
    cdef MidC d = MidC()
    print("%d %d %d" % (s.calc(), d.calc(), d.own_method()))


# ============================================================
# 5. No trampoline when method explicitly overridden in Derived
# ============================================================

@cython.python_subclassing(False)
cdef class ExplBase:
    @cython.test_fail_if_path_exists("//OverrideCheckNode")
    cpdef int m(self):
        return 5


@cython.python_subclassing(True)
cdef class ExplDerived(ExplBase):
    @cython.test_assert_path_exists("//OverrideCheckNode")
    cpdef int m(self):   # explicit override in a re-enabled class — must have OverrideCheckNode
        return 50


class _PyExplDerived(ExplDerived):
    def m(self):
        return 500


def test_explicit_override_no_duplicate():
    """
    >>> test_explicit_override_no_duplicate()
    500 50
    """
    s = _PyExplDerived()
    cdef ExplDerived d = ExplDerived()
    print("%d %d" % (s.m(), d.m()))


# ============================================================
# 6. Cython cclass subclass of locked class works fine
# ============================================================

@cython.python_subclassing(False)
cdef class CBaseF:
    cpdef int n(self):
        return 6


@cython.python_subclassing(True)
cdef class CMidT(CBaseF):
    pass


cdef class CGrandChild(CMidT):
    @cython.test_assert_path_exists("//OverrideCheckNode")
    cpdef int n(self):   # locked True inherited from CMidT — must have OverrideCheckNode
        return 66


def test_cython_subclass_of_locked():
    """
    >>> test_cython_subclass_of_locked()
    66
    """
    cdef CGrandChild g = CGrandChild()
    return g.n()


# ============================================================
# 7. Repeated @python_subclassing(True) — no error, no warning
# ============================================================

@cython.python_subclassing(False)
cdef class RepBase:
    cpdef int v(self):
        return 7


@cython.python_subclassing(True)
cdef class RepMid(RepBase):
    pass


@cython.python_subclassing(True)   # redundant but must not error
cdef class RepLeaf(RepMid):
    @cython.test_assert_path_exists("//OverrideCheckNode")
    cpdef int own_v(self):   # locked True via repeated decorator — must have OverrideCheckNode
        return 700


class _PyRepLeaf(RepLeaf):
    def v(self):
        return 77


def test_repeated_true_no_error():
    """
    >>> test_repeated_true_no_error()
    77
    """
    return _PyRepLeaf().v()
