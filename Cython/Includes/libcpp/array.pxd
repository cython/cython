cdef extern from "<array>" namespace "std" nogil:
    cdef cppclass array[T, size_t N]:
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
        array() except +
        array(array&) except +
        array(size_t) except +
        array(size_t, T&) except +
        #array[input_iterator](input_iterator, input_iterator)
        T& operator[](size_t)
        #array& operator=(array&)
        bint operator==(array&, array&)
        bint operator!=(array&, array&)
        bint operator<(array&, array&)
        bint operator>(array&, array&)
        bint operator<=(array&, array&)
        bint operator>=(array&, array&)
        void assign(size_t, const T&)
        void assign[input_iterator](input_iterator, input_iterator) except +
        T& at(size_t) except +
        T& back()
        iterator begin()
        const_iterator const_begin "begin"()
        bint empty()
        iterator end()
        const_iterator const_end "end"()
        T& front()
        size_t max_size()
        void pop_back()
        void push_back(T&) except +
        reverse_iterator rbegin()
        const_reverse_iterator const_rbegin "rbegin"()
        reverse_iterator rend()
        const_reverse_iterator const_rend "rend"()
        size_t size()
        void swap(array&)

        # C++11 methods
        T* data()
