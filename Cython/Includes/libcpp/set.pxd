from .utility cimport pair

cdef extern from "<set>" namespace "std" nogil:
    cdef cppclass set[T]:
        ctypedef T value_type
        cppclass iterator:
            T& operator*()
            iterator& operator++()
            iterator& operator--()
            bint operator==(const iterator &)
            bint operator!=(const iterator &)
        cppclass reverse_iterator:
            T& operator*()
            reverse_iterator& operator++()
            reverse_iterator& operator--()
            bint operator==(const reverse_iterator&)
            bint operator!=(const reverse_iterator&)
        cppclass const_iterator:
            const_iterator(iterator)
            const T& operator*()
            const_iterator& operator++()
            const_iterator& operator--()
            bint operator==(const const_iterator&)
            bint operator!=(const const_iterator&)
        cppclass const_reverse_iterator:
            const_reverse_iterator(reverse_iterator)
            const T& operator*()
            const_reverse_iterator& operator++()
            const_reverse_iterator& operator--()
            bint operator==(const const_reverse_iterator&)
            bint operator!=(const const_reverse_iterator&)
        set() except +
        set(set&) except +
        #set(key_compare&)
        #set& operator=(set&)
        bint operator==(set&, set&)
        bint operator!=(set&, set&)
        bint operator<(set&, set&)
        bint operator>(set&, set&)
        bint operator<=(set&, set&)
        bint operator>=(set&, set&)
        iterator begin()
        const_iterator const_begin "begin"()
        void clear()
        size_t count(const T&)
        bint empty()
        iterator end()
        const_iterator const_end "end"()
        pair[iterator, iterator] equal_range(const T&)
        pair[const_iterator, const_iterator] const_equal_range "equal_range"(const T&)
        iterator erase(iterator)
        iterator const_erase "erase"(const_iterator)
        iterator erase(const_iterator, const_iterator)
        size_t erase(const T&)
        iterator find(const T&)
        const_iterator const_find "find"(const T&)
        pair[iterator, bint] insert(const T&) except +
        iterator insert(iterator, const T&) except +
        iterator const_insert "insert"(const_iterator, const T&) except +
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
        void swap(set&)
        iterator upper_bound(const T&)
        const_iterator const_upper_bound "upper_bound"(const T&)
        #value_compare value_comp()

    cdef cppclass multiset[T]:
        ctypedef T value_type

        cppclass iterator:
            T& operator*()
            iterator& operator++()
            iterator& operator--()
            bint operator==(const iterator&)
            bint operator!=(const iterator&)
        cppclass reverse_iterator:
            T& operator*()
            reverse_iterator& operator++()
            reverse_iterator& operator--()
            bint operator==(const reverse_iterator&)
            bint operator!=(const reverse_iterator&)
        cppclass const_iterator:
            const_iterator(iterator)
            const T& operator*()
            const_iterator& operator++()
            const_iterator& operator--()
            bint operator==(const const_iterator&)
            bint operator!=(const const_iterator&)
        cppclass const_reverse_iterator:
            const_reverse_iterator(reverse_iterator)
            const T& operator*()
            const_reverse_iterator& operator++()
            const_reverse_iterator& operator--()
            bint operator==(const const_reverse_iterator&)
            bint operator!=(const const_reverse_iterator&)

        multiset() except +
        multiset(multiset&) except +
        #multiset(key_compare&)
        #multiset& operator=(multiset&)
        bint operator==(multiset&, multiset&)
        bint operator!=(multiset&, multiset&)
        bint operator<(multiset&, multiset&)
        bint operator>(multiset&, multiset&)
        bint operator<=(multiset&, multiset&)
        bint operator>=(multiset&, multiset&)
        iterator begin()
        const_iterator const_begin "begin"()
        void clear()
        size_t count(const T&)
        bint empty()
        iterator end()
        const_iterator const_end "end"()
        pair[iterator, iterator] equal_range(const T&)
        pair[const_iterator, const_iterator] const_equal_range "equal_range"(const T&)
        iterator erase(iterator)
        iterator const_erase "erase"(const_iterator)
        iterator erase(const_iterator, const_iterator)
        size_t erase(const T&)
        iterator find(const T&)
        const_iterator const_find "find"(const T&)
        iterator insert(const T&) except +
        iterator insert(iterator, const T&) except +
        iterator const_insert "insert"(const_iterator, const T&) except +
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
        void swap(multiset&)
        iterator upper_bound(const T&)
        const_iterator const_upper_bound "upper_bound"(const T&)
