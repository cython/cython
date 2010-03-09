from pair cimport pair

cdef extern from "<deque>" namespace "std":
    cdef cppclass deque[T]:
        cppclass iterator:
            T operator*()
            iterator operator++()
            bint operator==(iterator)
            bint operator!=(iterator)
        cppclass const_iterator(iterator):
            pass
        cppclass reverse_iterator(iterator):
            pass
        cppclass const_reverse_iterator(iterator):
            pass
        deque()
        deque(deque&)
        deque(size_t, T& val = T())
        #deque(input_iterator, input_iterator)
        TYPE& operator[]( size_type index )
        const TYPE& operator[]( size_type index ) const
        #deque& operator=(deque&)
        bool operator==(deque&, deque&)
        bool operator!=(deque&, deque&)
        bool operator<(deque&, deque&)
        bool operator>(deque&, deque&)
        bool operator<=(deque&, deque&)
        bool operator>=(deque&, deque&)
        void assign(size_t, TYPE&)
        void assign(input_iterator, input_iterator)
        T& at(size_t)
        T& back()
        iterator begin()
        const_iterator begin()
        void clear()
        bool empty()
        iterator end()
        const_iterator end()
        iterator erase(iterator)
        iterator erase(iterator, iterator)
        T& front()
        iterator insert(iterator, T&)
        void insert(iterator, size_t, T&)
        void insert(iterator, input_iterator, input_iterator)
        size_t max_size()
        void pop_back()
        void pop_front()
        void push_back(T&)
        void push_front(T&)
        reverse_iterator rbegin()
        const_reverse_iterator rbegin()
        reverse_iterator rend()
        const_reverse_iterator rend()
        void resize(size_t, T val = T())
        size_t size()
        void swap(deque&)
