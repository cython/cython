# tag: cpp
# mode: compile

cdef extern from *:
    """
    #if __cplusplus >= 201103L
    class NoAssign {
        public:
            NoAssign() {}
            NoAssign(NoAssign&) = delete;
            NoAssign(NoAssign&&) {}
            NoAssign& operator=(NoAssign&) = delete;
            NoAssign& operator=(NoAssign&&) { return *this; }
            void func() {}
    };
    #else
    // the test becomes meaningless
    // (but just declare something to ensure it passes)
    class NoAssign {
        public:
            void func() {}
    };
    #endif

    NoAssign get_NoAssign_Py() {
        return NoAssign();
    }
    NoAssign get_NoAssign_Cpp() {
        return NoAssign();
    }
    """
    cdef cppclass NoAssign:
        void func()

    # might raise Python exception (thus needs a temp)
    NoAssign get_NoAssign_Py() except *
    # might raise C++ exception (thus needs a temp)
    NoAssign get_NoAssign_Cpp() except +

cdef internal_cpp_func(NoAssign arg):
    pass

def test_call_to_function():
    # will fail to compile if move constructors aren't used
    internal_cpp_func(get_NoAssign_Py())
    internal_cpp_func(get_NoAssign_Cpp())

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
