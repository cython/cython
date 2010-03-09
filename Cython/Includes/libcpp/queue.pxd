from pair cimport pair

cdef extern from "<queue>" namespace "std":
    cdef cppclass queue[T]:
        queue()
        #queue(Container&)
        T& back()
        bool empty()
        T& front()
        void pop()
        void push(T&)
        size_t size()
