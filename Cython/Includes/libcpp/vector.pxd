cdef extern from "<vector>" namespace "std" nogil:
    cdef cppclass vector[T,ALLOCATOR=*]:
        ctypedef T value_type
        ctypedef ALLOCATOR allocator_type
        cppclass iterator:
            T& operator*()
            iterator operator++()
            iterator operator--()
            iterator operator+(size_t)
            iterator operator-(size_t)
            bint operator==(iterator)
            bint operator!=(iterator)
            bint operator<(iterator)
            bint operator>(iterator)
            bint operator<=(iterator)
            bint operator>=(iterator)
        cppclass reverse_iterator:
            T& operator*()
            iterator operator++()
            iterator operator--()
            iterator operator+(size_t)
            iterator operator-(size_t)
            bint operator==(reverse_iterator)
            bint operator!=(reverse_iterator)
            bint operator<(reverse_iterator)
            bint operator>(reverse_iterator)
            bint operator<=(reverse_iterator)
            bint operator>=(reverse_iterator)
        cppclass const_iterator(iterator):
            pass
        cppclass const_reverse_iterator(reverse_iterator):
            pass
        vector() except +
        vector(vector&) except +
        vector(size_t) except +
        vector(size_t, T&) except +
        #vector[input_iterator](input_iterator, input_iterator)
        T& operator[](size_t)
        #vector& operator=(vector&)
        bint operator==(vector&, vector&)
        bint operator!=(vector&, vector&)
        bint operator<(vector&, vector&)
        bint operator>(vector&, vector&)
        bint operator<=(vector&, vector&)
        bint operator>=(vector&, vector&)
        void assign(size_t, const T&)
        void assign[input_iterator](input_iterator, input_iterator) except +
        T& at(size_t) except +
        T& back()
        iterator begin()
        const_iterator const_begin "begin"()
        size_t capacity()
        void clear()
        bint empty()
        iterator end()
        const_iterator const_end "end"()
        iterator erase(iterator)
        iterator erase(iterator, iterator)
        T& front()
        iterator insert(iterator, const T&) except +
        void insert(iterator, size_t, const T&) except +
        void insert[Iter](iterator, Iter, Iter) except +
        size_t max_size()
        void pop_back()
        void push_back(T&) except +
        reverse_iterator rbegin()
        const_reverse_iterator const_rbegin "rbegin"()
        reverse_iterator rend()
        const_reverse_iterator const_rend "rend"()
        void reserve(size_t)
        void resize(size_t) except +
        void resize(size_t, T&) except +
        size_t size()
        void swap(vector&)

        # C++11 methods
        T* data()
        void shrink_to_fit()
