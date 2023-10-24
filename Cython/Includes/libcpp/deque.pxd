extern from "<deque>" namespace "std" nogil:
    cdef cppclass deque[T,ALLOCATOR=*]:
        ctypedef T value_type
        ctypedef ALLOCATOR allocator_type

        # these should really be allocator_type.size_type and
        # allocator_type.difference_type to be true to the C++ definition
        # but cython doesn't support deferred access on template arguments
        ctypedef usize size_type
        ctypedef ptrdiff_t difference_type

        cppclass const_iterator
        cppclass iterator:
            iterator() except +
            iterator(iterator&) except +
            value_type& operator*()
            iterator operator++()
            iterator operator--()
            iterator operator++(i32)
            iterator operator--(i32)
            iterator operator+(size_type)
            iterator operator-(size_type)
            difference_type operator-(iterator)
            difference_type operator-(const_iterator)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)
            bint operator<(iterator)
            bint operator<(const_iterator)
            bint operator>(iterator)
            bint operator>(const_iterator)
            bint operator<=(iterator)
            bint operator<=(const_iterator)
            bint operator>=(iterator)
            bint operator>=(const_iterator)
        cppclass const_iterator:
            const_iterator() except +
            const_iterator(iterator&) except +
            const_iterator(const_iterator&) except +
            operator=(iterator&) except +
            const value_type& operator*()
            const_iterator operator++()
            const_iterator operator--()
            const_iterator operator++(i32)
            const_iterator operator--(i32)
            const_iterator operator+(size_type)
            const_iterator operator-(size_type)
            difference_type operator-(iterator)
            difference_type operator-(const_iterator)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)
            bint operator<(iterator)
            bint operator<(const_iterator)
            bint operator>(iterator)
            bint operator>(const_iterator)
            bint operator<=(iterator)
            bint operator<=(const_iterator)
            bint operator>=(iterator)
            bint operator>=(const_iterator)

        cppclass const_reverse_iterator
        cppclass reverse_iterator:
            reverse_iterator() except +
            reverse_iterator(reverse_iterator&) except +
            value_type& operator*()
            reverse_iterator operator++()
            reverse_iterator operator--()
            reverse_iterator operator++(i32)
            reverse_iterator operator--(i32)
            reverse_iterator operator+(size_type)
            reverse_iterator operator-(size_type)
            difference_type operator-(iterator)
            difference_type operator-(const_iterator)
            bint operator==(reverse_iterator)
            bint operator==(const_reverse_iterator)
            bint operator!=(reverse_iterator)
            bint operator!=(const_reverse_iterator)
            bint operator<(reverse_iterator)
            bint operator<(const_reverse_iterator)
            bint operator>(reverse_iterator)
            bint operator>(const_reverse_iterator)
            bint operator<=(reverse_iterator)
            bint operator<=(const_reverse_iterator)
            bint operator>=(reverse_iterator)
            bint operator>=(const_reverse_iterator)
        cppclass const_reverse_iterator:
            const_reverse_iterator() except +
            const_reverse_iterator(reverse_iterator&) except +
            operator=(reverse_iterator&) except +
            const value_type& operator*()
            const_reverse_iterator operator++()
            const_reverse_iterator operator--()
            const_reverse_iterator operator++(i32)
            const_reverse_iterator operator--(i32)
            const_reverse_iterator operator+(size_type)
            const_reverse_iterator operator-(size_type)
            difference_type operator-(iterator)
            difference_type operator-(const_iterator)
            bint operator==(reverse_iterator)
            bint operator==(const_reverse_iterator)
            bint operator!=(reverse_iterator)
            bint operator!=(const_reverse_iterator)
            bint operator<(reverse_iterator)
            bint operator<(const_reverse_iterator)
            bint operator>(reverse_iterator)
            bint operator>(const_reverse_iterator)
            bint operator<=(reverse_iterator)
            bint operator<=(const_reverse_iterator)
            bint operator>=(reverse_iterator)
            bint operator>=(const_reverse_iterator)

        deque() except +
        deque(deque&) except +
        deque(usize) except +
        deque(usize, T&) except +
        #deque[InputIt](InputIt, InputIt)
        T& operator[](usize)
        #deque& operator=(deque&)
        bint operator==(deque&, deque&)
        bint operator!=(deque&, deque&)
        bint operator<(deque&, deque&)
        bint operator>(deque&, deque&)
        bint operator<=(deque&, deque&)
        bint operator>=(deque&, deque&)
        void assign(usize, T&) except +
        void assign[InputIt](InputIt, InputIt) except +
        T& at(usize) except +
        T& back()
        iterator begin()
        const_iterator const_begin "begin"()
        const_iterator cbegin()
        void clear()
        bint empty()
        iterator end()
        const_iterator const_end "end"()
        const_iterator cend()
        iterator erase(iterator) except +
        iterator erase(iterator, iterator) except +
        T& front()
        iterator insert(iterator, T&) except +
        void insert(iterator, usize, T&) except +
        void insert[InputIt](iterator, InputIt, InputIt) except +
        usize max_size()
        void pop_back()
        void pop_front()
        void push_back(T&) except +
        void push_front(T&) except +
        reverse_iterator rbegin()
        #const_reverse_iterator rbegin()
        const_reverse_iterator crbegin()
        reverse_iterator rend()
        #const_reverse_iterator rend()
        const_reverse_iterator crend()
        void resize(usize) except +
        void resize(usize, T&) except +
        usize size()
        void swap(deque&)

        # C++11 methods
        void shrink_to_fit() except +
