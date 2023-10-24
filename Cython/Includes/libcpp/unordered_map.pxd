from .utility cimport pair

extern from "<unordered_map>" namespace "std" nogil:
    cdef cppclass unordered_map[T, U, HASH=*, PRED=*, ALLOCATOR=*]:
        ctypedef T key_type
        ctypedef U mapped_type
        ctypedef pair[const T, U] value_type
        ctypedef ALLOCATOR allocator_type

        # these should really be allocator_type.size_type and
        # allocator_type.difference_type to be true to the C++ definition
        # but cython doesn't support deferred access on template arguments
        ctypedef usize size_type
        ctypedef ptrdiff_t difference_type

        cppclass iterator
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

        unordered_map() except +
        unordered_map(unordered_map&) except +
        #unordered_map(key_compare&)
        U& operator[](const T&)
        #unordered_map& operator=(unordered_map&)
        bint operator==(unordered_map&, unordered_map&)
        bint operator!=(unordered_map&, unordered_map&)
        bint operator<(unordered_map&, unordered_map&)
        bint operator>(unordered_map&, unordered_map&)
        bint operator<=(unordered_map&, unordered_map&)
        bint operator>=(unordered_map&, unordered_map&)
        U& at(const T&) except +
        const U& const_at "at"(const T&) except +
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
        pair[iterator, bint] insert(const pair[T, U]&) except +
        iterator insert(const_iterator, const pair[T, U]&) except +
        void insert[InputIt](InputIt, InputIt) except +
        #key_compare key_comp()
        iterator lower_bound(const T&)
        const_iterator const_lower_bound "lower_bound"(const T&)
        usize max_size()
        usize size()
        void swap(unordered_map&)
        iterator upper_bound(const T&)
        const_iterator const_upper_bound "upper_bound"(const T&)
        #value_compare value_comp()
        void max_load_factor(float)
        float max_load_factor()
        float load_factor()
        void rehash(usize)
        void reserve(usize)
        usize bucket_count()
        usize max_bucket_count()
        usize bucket_size(usize)
        usize bucket(const T&)
        # C++20
        bint contains(const T&)

    cdef cppclass unordered_multimap[T, U, HASH=*, PRED=*, ALLOCATOR=*]:
        ctypedef T key_type
        ctypedef U mapped_type
        ctypedef pair[const T, U] value_type
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
            iterator operator++(i32)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)
        cppclass const_iterator:
            const_iterator() except +
            const_iterator(iterator&) except +
            operator=(iterator&) except +
            # correct would be const value_type& but this does not work
            # well with cython's code gen
            const pair[T, U]& operator*()
            const_iterator operator++()
            const_iterator operator++(i32)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)

        unordered_multimap() except +
        unordered_multimap(const unordered_multimap&) except +
        #unordered_multimap(key_compare&)
        #unordered_map& operator=(unordered_multimap&)
        bint operator==(const unordered_multimap&, const unordered_multimap&)
        bint operator!=(const unordered_multimap&, const unordered_multimap&)
        bint operator<(const unordered_multimap&, const unordered_multimap&)
        bint operator>(const unordered_multimap&, const unordered_multimap&)
        bint operator<=(const unordered_multimap&, const unordered_multimap&)
        bint operator>=(const unordered_multimap&, const unordered_multimap&)
        iterator begin()
        const_iterator const_begin "begin"()
        const_iterator cbegin()
        #local_iterator begin(usize)
        #const_local_iterator const_begin "begin"(usize)
        void clear()
        usize count(const T&)
        bint empty()
        iterator end()
        const_iterator const_end "end"()
        const_iterator cend()
        #local_iterator end(usize)
        #const_local_iterator const_end "end"(usize)
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
        usize size()
        void swap(unordered_multimap&)
        iterator upper_bound(const T&)
        const_iterator const_upper_bound "upper_bound"(const T&)
        #value_compare value_comp()
        void max_load_factor(float)
        float max_load_factor()
        float load_factor()
        void rehash(usize)
        void reserve(usize)
        usize bucket_count()
        usize max_bucket_count()
        usize bucket_size(usize)
        usize bucket(const T&)
        # C++20
        bint contains(const T&)
