from pair cimport pair

cdef extern from "<vector>" namespace "std":
    cdef cppclass vector[T]:
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
        #cppclass input_iterator(iterator):
        #    pass
        vector()
        #vector(vector&)
        #vector(size_t, T&)
        #vector[input_iterator](input_iterator, input_iterator)
        T& operator[](size_t)
        #vector& operator=(vector&)
        bool operator==(vector&, vector&)
        bool operator!=(vector&, vector&)
        bool operator<(vector&, vector&)
        bool operator>(vector&, vector&)
        bool operator<=(vector&, vector&)
        bool operator>=(vector&, vector&)
        void assign(size_t, T&)
        #void assign(input_iterator, input_iterator)
        T& at(size_t)
        T& back()
        iterator begin()
        const_iterator begin()
        size_t capacity()
        void clear()
        bool empty()
        iterator end()
        const_iterator end()
        iterator erase(iterator)
        iterator erase(iterator, iterator)
        T& front()
        iterator insert(iterator, T&)
        void insert(iterator, size_t, T&)
        void insert(iterator, iterator, iterator)
        size_t max_size()
        void pop_back()
        void push_back(T&)
        reverse_iterator rbegin()
        const_reverse_iterator rbegin()
        reverse_iterator rend()
        const_reverse_iterator rend()
        void reserve(size_t)
        void resize(size_t, T)
        size_t size()
        void swap(vector&)
