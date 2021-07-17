# mode: run
# tag: cpp, cpp17

# cython: cpp_locals=True

cimport cython

from libcpp cimport bool as cppbool

cdef extern from *:
    r"""
    static void print_C_destructor();

    class C {
        public:
            C() = delete; // look! No default constructor
            C(int x, bool print_destructor=true) : x(x), print_destructor(print_destructor) {}
            C(C&& rhs) : x(rhs.x), print_destructor(rhs.print_destructor) {
                rhs.print_destructor = false; // moved-from instances are deleted silently
            }
            C& operator=(C&& rhs) {
                x=rhs.x;
                print_destructor=rhs.print_destructor;
                rhs.print_destructor = false; // moved-from instances are deleted silently
                return *this;
            }
            C(const C& rhs) = default;
            C& operator=(const C& rhs) = default;
            ~C() {
                if (print_destructor) print_C_destructor();
            }

            int getX() const { return x; }

        private:
            int x;
            bool print_destructor;
    };

    C make_C(int x) {
        return C(x);
    }
    """
    cdef cppclass C:
        C(int)
        C(int, cppbool)
        int getX() const
    C make_C(int) except +  # needs a temp to receive

# this function just makes sure the output from the destructor can be captured by doctest
cdef void print_C_destructor "print_C_destructor" () nogil:
    print("~C()")

def maybe_assign_infer(assign, value, do_print):
    """
    >>> maybe_assign_infer(True, 5, True)
    5
    ~C()
    >>> maybe_assign_infer(False, 0, True)
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'x' referenced before assignment
    >>> maybe_assign_infer(False, 0, False)  # no destructor call here
    """
    if assign:
        x = C(value)
    if do_print:
        print(x.getX())

def maybe_assign_cdef(assign, value):
    """
    >>> maybe_assign_cdef(True, 5)
    5
    ~C()
    >>> maybe_assign_cdef(False, 0)
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'x' referenced before assignment
    """
    cdef C x
    if assign:
        x = C(value)
    print(x.getX())

def maybe_assign_annotation(assign, value):
    """
    >>> maybe_assign_annotation(True, 5)
    5
    ~C()
    >>> maybe_assign_annotation(False, 0)
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'x' referenced before assignment
    """
    x: C
    if assign:
        x = C(value)
    print(x.getX())

def maybe_assign_directive1(assign, value):
    """
    >>> maybe_assign_directive1(True, 5)
    5
    ~C()
    >>> maybe_assign_directive1(False, 0)
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'x' referenced before assignment
    """
    x = cython.declare(C)
    if assign:
        x = C(value)
    print(x.getX())

@cython.locals(x=C)
def maybe_assign_directive2(assign, value):
    """
    >>> maybe_assign_directive2(True, 5)
    5
    ~C()
    >>> maybe_assign_directive2(False, 0)
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'x' referenced before assignment
    """
    if assign:
        x = C(value)
    print(x.getX())

def maybe_assign_nocheck(assign, value):
    """
    >>> maybe_assign_nocheck(True, 5)
    5
    ~C()

    # unfortunately it's quite difficult to test not assigning because there's a decent chance it'll crash
    """
    if assign:
        x = C(value)
    with cython.initializedcheck(False):
        print(x.getX())

def uses_temp(value):
    """
    needs a temp to handle the result of make_C - still doesn't use the default constructor
    >>> uses_temp(10)
    10
    ~C()
    """

    x = make_C(value)
    print(x.getX())

# c should not be optional - it isn't easy to check this, but we can at least check it compiles
cdef void has_argument(C c):
    print(c.getX())

def call_has_argument():
    """
    >>> call_has_argument()
    50
    """
    has_argument(C(50, False))

cdef class HoldsC:
    """
    >>> inst = HoldsC(True, False)
    >>> inst.getCX()
    10
    >>> inst = HoldsC(False, False)
    >>> inst.getCX()
    Traceback (most recent call last):
        ...
    AttributeError: C++ attribute 'value' is not initialized
    """
    cdef C value
    def __cinit__(self, initialize, print_destructor):
        if initialize:
            self.value = C(10, print_destructor)

    def getCX(self):
        return self.value.getX()

def dont_test_on_pypy(f):
    import sys
    if not hasattr(sys, "pypy_version_info"):
        return f

@dont_test_on_pypy  # non-deterministic destruction
def testHoldsCDestruction(initialize):
    """
    >>> testHoldsCDestruction(True)
    ~C()
    >>> testHoldsCDestruction(False)  # no destructor
    """
    x = HoldsC(initialize, True)
    del x

cdef C global_var

def initialize_global_var():
    global global_var
    global_var = C(-1, False)

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
