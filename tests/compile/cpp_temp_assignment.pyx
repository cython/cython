# mode: compile
# tag: cpp, cpp11

cdef extern from *:
    """
    class NoAssign {
        public:
            NoAssign() {}
            NoAssign(NoAssign&) = delete;
            NoAssign(NoAssign&&) {}
            NoAssign& operator=(NoAssign&) = delete;
            NoAssign& operator=(NoAssign&&) { return *this; }
            void func() {}
    };

    NoAssign get_NoAssign_Py() {
        return NoAssign();
    }
    NoAssign get_NoAssign_Cpp() {
        return NoAssign();
    }

    class NoDefaultNoAssign {
        public:
            explicit NoDefaultNoAssign(int) {}
            NoDefaultNoAssign(NoDefaultNoAssign&) = delete;
            NoDefaultNoAssign(NoDefaultNoAssign&&) {}
            NoDefaultNoAssign& operator=(NoDefaultNoAssign&) = delete;
            NoDefaultNoAssign& operator=(NoDefaultNoAssign&&) { return *this; }
            void func() {}
    };

    NoDefaultNoAssign get_NoDefaultNoAssign_Py() {
        return NoDefaultNoAssign(0);
    }
    NoDefaultNoAssign get_NoDefaultNoAssign_Cpp() {
        return NoDefaultNoAssign(0);
    }
    """
    cdef cppclass NoAssign:
        void func()
    cdef cppclass NoDefaultNoAssign:
        void func()

    # might raise Python exception (thus needs a temp)
    NoAssign get_NoAssign_Py() except *
    # might raise C++ exception (thus needs a temp)
    NoAssign get_NoAssign_Cpp() except +
    # might raise Python exception (thus needs a temp)
    NoDefaultNoAssign get_NoDefaultNoAssign_Py() except *
    # might raise C++ exception (thus needs a temp)
    NoDefaultNoAssign get_NoDefaultNoAssign_Cpp() except +

cdef internal_cpp_func(NoDefaultNoAssign arg):
    pass

def test_call_to_function():
    # will fail to compile if move constructors aren't used
    # or if the default constructor is needed
    internal_cpp_func(get_NoDefaultNoAssign_Py())
    internal_cpp_func(get_NoDefaultNoAssign_Cpp())

def test_assignment_to_name():
    # will fail if move constructors aren't used
    cdef NoAssign value
    value = get_NoAssign_Py()
    value = get_NoAssign_Cpp()

def test_assignment_to_scope():
    cdef NoAssign value
    value = get_NoAssign_Py()
    value = get_NoAssign_Cpp()
    def inner():
        value.func()

cdef class AssignToClassAttr:
    cdef NoAssign attr
    def __init__(self):
        self.attr = get_NoAssign_Py()
        self.attr = get_NoAssign_Cpp()
