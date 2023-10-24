extern from "<forward_list>" namespace "std" nogil:
    cdef cppclass forward_list[T,ALLOCATOR=*]:
        ctypedef T value_type
        ctypedef ALLOCATOR allocator_type

        # these should really be allocator_type.size_type and
        # allocator_type.difference_type to be true to the C++ definition
        # but cython doesn't support deferred access on template arguments
        ctypedef usize size_type
        ctypedef ptrdiff_t difference_type

        cppclass iterator:
            iterator()
            iterator(iterator &)
            T& operator*()
            iterator operator++()
            iterator operator++(i32)
            bint operator==(iterator)
            bint operator!=(iterator)
        cppclass const_iterator(iterator):
            pass
        forward_list() except +
        forward_list(forward_list&) except +
        forward_list(usize, T&) except +
        #forward_list& operator=(forward_list&)
        bint operator==(forward_list&, forward_list&)
        bint operator!=(forward_list&, forward_list&)
        bint operator<(forward_list&, forward_list&)
        bint operator>(forward_list&, forward_list&)
        bint operator<=(forward_list&, forward_list&)
        bint operator>=(forward_list&, forward_list&)
        void assign(usize, T&)
        T& front()
        iterator before_begin()
        const_iterator const_before_begin "before_begin"()
        iterator begin()
        const_iterator const_begin "begin"()
        iterator end()
        const_iterator const_end "end"()
        bint empty()
        usize max_size()
        void clear()
        iterator insert_after(iterator, T&)
        void insert_after(iterator, usize, T&)
        iterator erase_after(iterator)
        iterator erase_after(iterator, iterator)
        void push_front(T&)
        void pop_front()
        void resize(usize)
        void resize(usize, T&)
        void swap(forward_list&)
        void merge(forward_list&)
        void merge[Compare](forward_list&, Compare)
        void splice_after(iterator, forward_list&)
        void splice_after(iterator, forward_list&, iterator)
        void splice_after(iterator, forward_list&, iterator, iterator)
        void remove(const T&)
        void remove_if[Predicate](Predicate)
        void reverse()
        void unique()
        void unique[Predicate](Predicate)
        void sort()
        void sort[Compare](Compare)
