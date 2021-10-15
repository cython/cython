from .utility cimport pair

cdef extern from "<map>" namespace "std" nogil:
    cdef cppclass map[T, U, COMPARE=*, ALLOCATOR=*]:
        ctypedef T key_type
        ctypedef U mapped_type
        ctypedef pair[const T, U] value_type
        ctypedef COMPARE key_compare
        ctypedef ALLOCATOR allocator_type
        cppclass iterator:
            pair[T, U]& operator*()
            iterator operator++()
            iterator operator--()
            bint operator==(iterator)
            bint operator!=(iterator)
        cppclass reverse_iterator:
            pair[T, U]& operator*()
            iterator operator++()
            iterator operator--()
            bint operator==(reverse_iterator)
            bint operator!=(reverse_iterator)
        cppclass const_iterator(iterator):
            pass
        cppclass const_reverse_iterator(reverse_iterator):
            pass
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
        void clear()
        size_t count(const T&)
        bint empty()
        iterator end()
        const_iterator const_end "end" ()
        pair[iterator, iterator] equal_range(const T&)
        pair[const_iterator, const_iterator] const_equal_range "equal_range"(const T&)
        iterator erase(iterator)
        iterator const_erase "erase"(const_iterator)
        iterator erase(const_iterator, const_iterator)
        size_t erase(const T&)
        iterator find(const T&)
        const_iterator const_find "find" (const T&)
        pair[iterator, bint] insert(const pair[T, U]&) except +
        iterator insert(const_iterator, const pair[T, U]&) except +
        void insert[InputIt](InputIt, InputIt) except +
        #key_compare key_comp()
        iterator lower_bound(const T&)
        const_iterator const_lower_bound "lower_bound"(const T&)
        size_t max_size()
        reverse_iterator rbegin()
        const_reverse_iterator const_rbegin "rbegin"()
        reverse_iterator rend()
        const_reverse_iterator const_rend "rend"()
        size_t size()
        void swap(map&)
        iterator upper_bound(const T&)
        const_iterator const_upper_bound "upper_bound"(const T&)
        #value_compare value_comp()
