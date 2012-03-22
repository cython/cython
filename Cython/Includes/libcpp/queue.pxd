cdef extern from "<queue>" namespace "std":
    cdef cppclass queue[T]:
        queue()
        queue(queue&)
        #queue(Container&)
        T& back() nogil
        bint empty() nogil
        T& front() nogil
        void pop() nogil
        void push(T&) nogil
        size_t size() nogil
    cdef cppclass priority_queue[T]:
        priority_queue()
        priority_queue(priority_queue&)
        #priority_queue(Container&)
        bint empty() nogil
        void pop() nogil
        void push(T&) nogil
        size_t size() nogil
        T& top() nogil
