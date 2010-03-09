from pair cimport pair

cdef extern from "<set>" namespace "std":
    cdef cppclass set[T]:
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
        set()
        set(set&)
        #set set(key_compare&)
        #set& operator=(set&)
        bool operator==(set&, set&)
        bool operator!=(set&, set&)
        bool operator<(set&, set&)
        bool operator>(set&, set&)
        bool operator<=(set&, set&)
        bool operator>=(set&, set&)
        iterator begin()
        const_iterator begin()
        void clear()
        #size_t count(key_type&)
        bool empty()
        iterator end()
        const_iterator end()
        #pair[iterator, iterator] equal_range(key_type&)
        #pair[const_iterator, const_iterator] equal_range(key_type&)
        void erase(iterator)
        void erase(iterator, iterator)
        #size_t erase(key_type&)
        #iterator find(key_type&)
        #const_iterator find(key_type&)
        #pair[iterator, bool] insert(T&)
        iterator insert(iterator, T&)
        #void insert(input_iterator, input_iterator)
        #key_compare key_comp()
        #iterator lower_bound(key_type&)
        #const_iterator lower_bound(key_type&)
        size_t max_size()
        reverse_iterator rbegin()
        const_reverse_iterator rbegin()
        reverse_iterator rend()
        const_reverse_iterator rend()
        size_t size()
        void swap(set&)
        #iterator upper_bound(key_type&)
        #const_iterator upper_bound(key_type&)
        #value_compare value_comp()
