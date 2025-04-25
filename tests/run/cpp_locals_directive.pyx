# mode: run
# tag: cpp, cpp17, no-cpp-locals
# no-cpp-locals because the test is already run with it explicitly set

# cython: cpp_locals=True

cimport cython

from libcpp cimport bool as cppbool

cdef extern from *:
    r"""
    static void print_MoveableC_destructor();
    static void print_NonMoveableC_constructor1(int);
    static void print_NonMoveableC_constructor2(int, int);

    class NoThrowTag{};

    class MoveableC {
        public:
            MoveableC() = delete; // look! No default constructor
            MoveableC(int x, bool print_destructor=true) : x(x), print_destructor(print_destructor) {}
            MoveableC(NoThrowTag, int x, bool print_destructor) : MoveableC(x, print_destructor) {}
            MoveableC(MoveableC&& rhs) : x(rhs.x), print_destructor(rhs.print_destructor) {
                rhs.print_destructor = false; // moved-from instances are deleted silently
            }
            // also test that we don't require the assignment operator
            MoveableC& operator=(MoveableC&& rhs) = delete;
            MoveableC(const MoveableC& rhs) = delete;
            MoveableC& operator=(const MoveableC& rhs) = default;
            ~MoveableC() {
                if (print_destructor) print_MoveableC_destructor();
            }

            int getX() const { return x; }

        private:
            int x;
            bool print_destructor;
    };

    MoveableC make_MoveableC(int x) {
        return MoveableC(x);
    }

    class NonMoveableC {
        public:
            NonMoveableC() = delete; // look! No default constructor
            NonMoveableC(int a) { print_NonMoveableC_constructor1(a); }
            NonMoveableC(int a, int b) { print_NonMoveableC_constructor2(a, b); }
            NonMoveableC(const NonMoveableC&) = delete;
            NonMoveableC(NonMoveableC&&) = delete;

            NonMoveableC& operator=(const NonMoveableC&) = delete;
            NonMoveableC& operator=(NonMoveableC&&) = delete;
    };
    """
    cdef cppclass NoThrowTag:
        NoThrowTag()
    cdef cppclass MoveableC:
        # These don't really through, but test the code generation as if they did
        MoveableC(int) except +
        MoveableC(int, cppbool) except +
        MoveableC(NoThrowTag, int, cppbool)
        int getX() const
    MoveableC make_MoveableC(int) except +  # needs a temp to receive
    cdef cppclass NonMoveableC:
        NonMoveableC(int)
        NonMoveableC(int, int)

# this function just makes sure the output from the destructor can be captured by doctest
cdef void print_MoveableC_destructor "print_MoveableC_destructor" () with gil:
    print("~MoveableC()")

cdef void print_NonMoveableC_constructor1 "print_NonMoveableC_constructor1" (int a) with gil:
    print(f"NonMoveableC({a})")

cdef void print_NonMoveableC_constructor2 "print_NonMoveableC_constructor2" (int a, int b) with gil:
    print(f"NonMoveableC({a}, {b})")

def maybe_assign_infer(assign, value, do_print):
    """
    >>> maybe_assign_infer(True, 5, True)
    5
    ~MoveableC()
    >>> maybe_assign_infer(False, 0, True)
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'x' referenced before assignment
    >>> maybe_assign_infer(False, 0, False)  # no destructor call here
    """
    if assign:
        x = MoveableC(value)
    if do_print:
        print(x.getX())

def maybe_assign_cdef(assign, value):
    """
    >>> maybe_assign_cdef(True, 5)
    5
    ~MoveableC()
    >>> maybe_assign_cdef(False, 0)
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'x' referenced before assignment
    """
    cdef MoveableC x
    if assign:
        x = MoveableC(value)
    print(x.getX())

def maybe_assign_annotation(assign, value):
    """
    >>> maybe_assign_annotation(True, 5)
    5
    ~MoveableC()
    >>> maybe_assign_annotation(False, 0)
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'x' referenced before assignment
    """
    x: MoveableC
    if assign:
        x = MoveableC(value)
    print(x.getX())

def maybe_assign_directive1(assign, value):
    """
    >>> maybe_assign_directive1(True, 5)
    5
    ~MoveableC()
    >>> maybe_assign_directive1(False, 0)
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'x' referenced before assignment
    """
    x = cython.declare(MoveableC)
    if assign:
        x = MoveableC(value)
    print(x.getX())

@cython.locals(x=MoveableC)
def maybe_assign_directive2(assign, value):
    """
    >>> maybe_assign_directive2(True, 5)
    5
    ~MoveableC()
    >>> maybe_assign_directive2(False, 0)
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'x' referenced before assignment
    """
    if assign:
        x = MoveableC(value)
    print(x.getX())

def maybe_assign_nocheck(assign, value):
    """
    >>> maybe_assign_nocheck(True, 5)
    5
    ~MoveableC()

    # unfortunately it's quite difficult to test not assigning because there's a decent chance it'll crash
    """
    if assign:
        x = MoveableC(value)
    with cython.initializedcheck(False):
        print(x.getX())

def uses_temp(value):
    """
    needs a temp to handle the result of make_MoveableC - still doesn't use the default constructor
    >>> uses_temp(10)
    10
    ~MoveableC()
    """

    x = make_MoveableC(value)
    print(x.getX())

# c should not be optional - it isn't easy to check this, but we can at least check it compiles
cdef void has_argument(MoveableC c):
    print(c.getX())

def call_has_argument():
    """
    >>> call_has_argument()
    50
    """
    has_argument(MoveableC(50, False))

cdef class HoldsMoveableC:
    """
    >>> inst = HoldsMoveableC(True, False)
    >>> inst.getMoveableCX()
    10
    >>> access_from_function_with_different_directive(inst)
    10
    10
    >>> inst.getMoveableCX()  # it was changed in access_from_function_with_different_directive
    20
    >>> inst = HoldsMoveableC(False, False)
    >>> inst.getMoveableCX()
    Traceback (most recent call last):
        ...
    AttributeError: C++ attribute 'value' is not initialized
    >>> access_from_function_with_different_directive(inst)
    Traceback (most recent call last):
        ...
    AttributeError: C++ attribute 'value' is not initialized
    """
    cdef MoveableC value
    def __cinit__(self, initialize, print_destructor):
        if initialize:
            self.value = MoveableC(10, print_destructor)

    def getMoveableCX(self):
        return self.value.getX()

cdef acceptMoveableC(MoveableC& c):
    return c.getX()

@cython.cpp_locals(False)
def access_from_function_with_different_directive(HoldsMoveableC c):
    # doctest is in HoldsMoveableC class
    print(acceptMoveableC(c.value))  # this originally tried to pass a __Pyx_Optional<MoveableC> as a MoveableC instance
    print(c.value.getX())
    c.value = MoveableC(NoThrowTag(), 20, False) # make sure that we can change it too

def dont_test_on_pypy(f):
    import sys
    if not hasattr(sys, "pypy_version_info"):
        return f

@dont_test_on_pypy  # non-deterministic destruction
def testHoldsMoveableCDestruction(initialize):
    """
    >>> testHoldsMoveableCDestruction(True)
    ~MoveableC()
    >>> testHoldsMoveableCDestruction(False)  # no destructor
    """
    x = HoldsMoveableC(initialize, True)
    del x

cdef MoveableC global_var

def initialize_global_var():
    global global_var
    global_var = MoveableC(-1, False)

def read_global_var():
    """
    >>> read_global_var()
    Traceback (most recent call last):
        ...
    NameError: C++ global 'global_var' is not initialized
    >>> initialize_global_var()
    >>> read_global_var()
    -1
    """
    print(global_var.getX())

def test_nonmoveable(arg1, arg2=None):
    """
    >>> test_nonmoveable(5)
    NonMoveableC(5)
    >>> test_nonmoveable(5, 6)
    NonMoveableC(5, 6)
    """
    cdef NonMoveableC nm
    if arg2 is None:
        nm = NonMoveableC(<int>arg1)
    else:
        nm = NonMoveableC(<int>arg1, <int>arg2)

cdef NonMoveableC global_nonmoveable

def test_global_nonmoveable(arg):
    """
    >>> test_global_nonmoveable(2)
    NonMoveableC(2)
    """
    global global_nonmoveable
    global_nonmoveable = NonMoveableC(arg)

cdef class HoldsNonMoveableC:
    """
    >>> v = HoldsNonMoveableC(None)
    >>> v = HoldsNonMoveableC(10)
    NonMoveableC(10)
    """

    cdef NonMoveableC c

    def __init__(self, arg):
        if arg is not None:
            self.c = NonMoveableC(arg)
