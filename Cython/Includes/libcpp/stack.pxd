cdef extern from "<stack>" namespace "std" nogil:
    cdef cppclass stack[T]:
        stack() except +
        stack(stack&) except +
        #stack(Container&)
        bint empty()
        void pop()
        void push(T&)
        size_t size()
        T& top()
