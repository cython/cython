# mode: run
# tag: cpp, cpp17

# cython: cpp_locals=True

cimport cython

cdef extern from *:
    """
    class C {
        public:
            C() = delete; // look! No default constructor
            C(int x) : x(x) {}

            int getX() const { return x; }

        private:
            int x;
    };

    C make_C(int x) {
        return C(x);
    }
    """
    cdef cppclass C:
        C(int)
        int getX() const
    C make_C(int) except +  # needs a temp to receive

def maybe_assign_infer(assign, value):
    """
    >>> maybe_assign_infer(True, 5)
    5
    >>> maybe_assign_infer(False, 0)
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'x' referenced before assignment
    """
    if assign:
        x = C(value)
    print(x.getX())

def maybe_assign_cdef(assign, value):
    """
    >>> maybe_assign_cdef(True, 5)
    5
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
    >>> maybe_assign_directive2(False, 0)
    Traceback (most recent call last):
        ...
    UnboundLocalError: local variable 'x' referenced before assignment
    """
    if assign:
        x = C(value)
    print(x.getX())

@cython.cpp_locals_nocheck(False)
def maybe_assign_nocheck(assign, value):
    """
    >>> maybe_assign_nocheck(True, 5)
    5

    # unfortunately it's quite difficult to test not assigning because there's a decent change it'll crash
    """
    if assign:
        x = C(value)
    print(x.getX())

def uses_temp(value):
    """
    needs a temp to handle the result of make_C - still doesn't use the default constructor
    >>> uses_temp(10)
    10
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
    has_argument(C(50))

cdef class HoldsC:
    """
    >>> inst = HoldsC(True)
    >>> inst.getCX()
    10
    >>> inst = HoldsC(False)
    >>> inst.getCX()
    Traceback (most recent call last):
        ...
    AttributeError: C++ class attribute is not initialized
    """
    cdef C value
    def __cinit__(self, initialize):
        if initialize:
            self.value = C(10)

    def getCX(self):
        return self.value.getX()

cdef C global_var

def initialize_global_var():
    global global_var
    global_var = C(-1)

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
