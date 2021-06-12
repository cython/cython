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

def maybe_assign(assign, value):
    """
    >>> maybe_assign(True, 5)
    5
    >>> maybe_assign(False, 0)
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
    >>> maybe_assign(True, 5)
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
