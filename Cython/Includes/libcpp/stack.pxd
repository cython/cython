cdef extern from "<stack>" namespace "std":
    cdef cppclass stack[T]:
        stack()
        stack(stack&)
        #stack(Container&)
        bint empty() nogil
        void pop() nogil
        void push(T&) nogil
        size_t size() nogil
        T& top() nogil
