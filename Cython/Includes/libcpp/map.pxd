from .utility cimport pair

extern from "<map>" namespace "std" nogil:
    cdef cppclass map[T, U, COMPARE=*, ALLOCATOR=*]:
        ctypedef T key_type
        ctypedef U mapped_type
        ctypedef pair[const T, U] value_type
        ctypedef COMPARE key_compare
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
            # correct would be value_type& but this does not work
            # well with cython's code gen
            pair[T, U]& operator*()
            iterator operator++()
            iterator operator--()
            iterator operator++(i32)
            iterator operator--(i32)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)
        cppclass const_iterator:
            const_iterator() except +
            const_iterator(iterator&) except +
            const_iterator(const_iterator&) except +
            operator=(iterator&) except +
            # correct would be const value_type& but this does not work
            # well with cython's code gen
            const pair[T, U]& operator*()
            const_iterator operator++()
            const_iterator operator--()
            const_iterator operator++(i32)
            const_iterator operator--(i32)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)

        cppclass const_reverse_iterator
        cppclass reverse_iterator:
            reverse_iterator() except +
            reverse_iterator(reverse_iterator&) except +
            # correct would be value_type& but this does not work
            # well with cython's code gen
            pair[T, U]& operator*()
            reverse_iterator operator++()
            reverse_iterator operator--()
            reverse_iterator operator++(i32)
            reverse_iterator operator--(i32)
            bint operator==(reverse_iterator)
            bint operator==(const_reverse_iterator)
            bint operator!=(reverse_iterator)
            bint operator!=(const_reverse_iterator)
        cppclass const_reverse_iterator:
            const_reverse_iterator() except +
            const_reverse_iterator(reverse_iterator&) except +
            operator=(reverse_iterator&) except +
            # correct would be const value_type& but this does not work
            # well with cython's code gen
            const pair[T, U]& operator*()
            const_reverse_iterator operator++()
            const_reverse_iterator operator--()
            const_reverse_iterator operator++(i32)
            const_reverse_iterator operator--(i32)
            bint operator==(reverse_iterator)
            bint operator==(const_reverse_iterator)
            bint operator!=(reverse_iterator)
            bint operator!=(const_reverse_iterator)

        map() except +
        map(map&) except +
        #map(key_compare&)
        U& operator[](const T&)
        #map& operator=(map&)
        bint operator==(map&, map&)
        bint operator!=(map&, map&)
        bint operator<(map&, map&)
        bint operator>(map&, map&)
        bint operator<=(map&, map&)
        bint operator>=(map&, map&)
        U& at(const T&) except +
        const U& const_at "at"(const T&) except +
        iterator begin()
        const_iterator const_begin "begin" ()
        const_iterator cbegin()
        void clear()
        usize count(const T&)
        bint empty()
        iterator end()
        const_iterator const_end "end" ()
        const_iterator cend()
        pair[iterator, iterator] equal_range(const T&)
        pair[const_iterator, const_iterator] const_equal_range "equal_range"(const T&)
        iterator erase(iterator)
        iterator const_erase "erase"(const_iterator)
        iterator erase(const_iterator, const_iterator)
        usize erase(const T&)
        iterator find(const T&)
        const_iterator const_find "find" (const T&)
        pair[iterator, bint] insert(const pair[T, U]&) except +
        iterator insert(const_iterator, const pair[T, U]&) except +
        void insert[InputIt](InputIt, InputIt) except +
        #key_compare key_comp()
        iterator lower_bound(const T&)
        const_iterator const_lower_bound "lower_bound"(const T&)
        usize max_size()
        reverse_iterator rbegin()
        const_reverse_iterator const_rbegin "rbegin"()
        const_reverse_iterator crbegin()
        reverse_iterator rend()
        const_reverse_iterator const_rend "rend"()
        const_reverse_iterator crend()
        usize size()
        void swap(map&)
        iterator upper_bound(const T&)
        const_iterator const_upper_bound "upper_bound"(const T&)
        #value_compare value_comp()
        # C++20
        bint contains(const T&)

    cdef cppclass multimap[T, U, COMPARE=*, ALLOCATOR=*]:
        ctypedef T key_type
        ctypedef U mapped_type
        ctypedef pair[const T, U] value_type
        ctypedef COMPARE key_compare
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
            # correct would be value_type& but this does not work
            # well with cython's code gen
            pair[T, U]& operator*()
            iterator operator++()
            iterator operator--()
            iterator operator++(i32)
            iterator operator--(i32)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)
        cppclass const_iterator:
            const_iterator() except +
            const_iterator(iterator&) except +
            const_iterator(const_iterator&) except +
            operator=(iterator&) except +
            # correct would be const value_type& but this does not work
            # well with cython's code gen
            const pair[T, U]& operator*()
            const_iterator operator++()
            const_iterator operator--()
            const_iterator operator++(i32)
            const_iterator operator--(i32)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)

        cppclass const_reverse_iterator
        cppclass reverse_iterator:
            reverse_iterator() except +
            reverse_iterator(reverse_iterator&) except +
            # correct would be value_type& but this does not work
            # well with cython's code gen
            pair[T, U]& operator*()
            reverse_iterator operator++()
            reverse_iterator operator--()
            reverse_iterator operator++(i32)
            reverse_iterator operator--(i32)
            bint operator==(reverse_iterator)
            bint operator==(const_reverse_iterator)
            bint operator!=(reverse_iterator)
            bint operator!=(const_reverse_iterator)
        cppclass const_reverse_iterator:
            const_reverse_iterator() except +
            const_reverse_iterator(reverse_iterator&) except +
            operator=(reverse_iterator&) except +
            # correct would be const value_type& but this does not work
            # well with cython's code gen
            const pair[T, U]& operator*()
            const_reverse_iterator operator++()
            const_reverse_iterator operator--()
            const_reverse_iterator operator++(i32)
            const_reverse_iterator operator--(i32)
            bint operator==(reverse_iterator)
            bint operator==(const_reverse_iterator)
            bint operator!=(reverse_iterator)
            bint operator!=(const_reverse_iterator)

        multimap() except +
        multimap(const multimap&) except +
        #multimap(key_compare&)
        #multimap& operator=(multimap&)
        bint operator==(const multimap&, const multimap&)
        bint operator!=(const multimap&, const multimap&)
        bint operator<(const multimap&, const multimap&)
        bint operator>(const multimap&, const multimap&)
        bint operator<=(const multimap&, const multimap&)
        bint operator>=(const multimap&, const multimap&)
        iterator begin()
        const_iterator const_begin "begin"()
        const_iterator cbegin()
        void clear()
        usize count(const T&)
        bint empty()
        iterator end()
        const_iterator const_end "end"()
        const_iterator cend()
        pair[iterator, iterator] equal_range(const T&)
        pair[const_iterator, const_iterator] const_equal_range "equal_range"(const T&)
        iterator erase(iterator)
        iterator const_erase "erase"(const_iterator)
        iterator erase(const_iterator, const_iterator)
        usize erase(const T&)
        iterator find(const T&)
        const_iterator const_find "find"(const T&)
        iterator insert(const pair[T, U]&) except +
        iterator insert(const_iterator, const pair[T, U]&) except +
        void insert[InputIt](InputIt, InputIt) except +
        #key_compare key_comp()
        iterator lower_bound(const T&)
        const_iterator const_lower_bound "lower_bound"(const T&)
        usize max_size()
        reverse_iterator rbegin()
        const_reverse_iterator const_rbegin "rbegin"()
        const_reverse_iterator crbegin()
        reverse_iterator rend()
        const_reverse_iterator const_rend "rend"()
        const_reverse_iterator crend()
        usize size()
        void swap(multimap&)
        iterator upper_bound(const T&)
        const_iterator const_upper_bound "upper_bound"(const T&)
        #value_compare value_comp()
        bint contains(const T&)
