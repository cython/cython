from pair cimport pair

cdef extern from "<set>" namespace "std" nogil:
    cdef cppclass set[T]:
        cppclass iterator:
            T& operator*()
            iterator operator++()
            iterator operator--()
            bint operator==(iterator)
            bint operator!=(iterator)
        cppclass reverse_iterator:
            T& operator*()
            iterator operator++()
            iterator operator--()
            bint operator==(reverse_iterator)
            bint operator!=(reverse_iterator)
        #cppclass const_iterator(iterator):
        #    pass
        #cppclass const_reverse_iterator(reverse_iterator):
        #    pass
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
        #const_iterator begin()
        void clear()
        size_t count(T&)
        bint empty()
        iterator end()
        #const_iterator end()
        pair[iterator, iterator] equal_range(T&)
        #pair[const_iterator, const_iterator] equal_range(T&)
        void erase(iterator)
        void erase(iterator, iterator)
        size_t erase(T&)
        iterator find(T&)
        #const_iterator find(T&)
        pair[iterator, bint] insert(T&)
        iterator insert(iterator, T&)
        #void insert(input_iterator, input_iterator)
        #key_compare key_comp()
        iterator lower_bound(T&)
        #const_iterator lower_bound(T&)
        size_t max_size()
        reverse_iterator rbegin()
        #const_reverse_iterator rbegin()
        reverse_iterator rend()
        #const_reverse_iterator rend()
        size_t size()
        void swap(set&)
        iterator upper_bound(T&)
        #const_iterator upper_bound(T&)
        #value_compare value_comp()
