cdef extern from "<stack>" namespace "std":
    cdef cppclass stack[T]:
        stack()
        stack(stack&)
        #stack(Container&)
        bint empty()
        void pop()
        void push(T&)
        size_t size()
        T& top()
