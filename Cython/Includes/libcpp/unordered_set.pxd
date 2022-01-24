from .utility cimport pair

cdef extern from "<unordered_set>" namespace "std" nogil:
    cdef cppclass unordered_set[T,HASH=*,PRED=*,ALLOCATOR=*]:
        ctypedef T value_type
        cppclass iterator:
            T& operator*()
            iterator& operator++()
            bint operator==(const iterator&)
            bint operator!=(const iterator&)
        cppclass const_iterator:
            const_iterator(iterator)
            const T& operator*()
            const_iterator& operator++()
            bint operator==(const const_iterator&)
            bint operator!=(const const_iterator&)
        unordered_set() except +
        unordered_set(unordered_set&) except +
        #unordered_set& operator=(unordered_set&)
        bint operator==(unordered_set&, unordered_set&)
        bint operator!=(unordered_set&, unordered_set&)
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
        iterator insert(const_iterator, const T&) except +
        void insert[InputIt](InputIt, InputIt) except +
        size_t max_size()
        size_t size()
        void swap(unordered_set&)
        #value_compare value_comp()
        void max_load_factor(float)
        float max_load_factor()
        float load_factor()
        void rehash(size_t)
        void reserve(size_t)
        size_t bucket_count()
        size_t max_bucket_count()
        size_t bucket_size(size_t)
        size_t bucket(const T&)

    cdef cppclass unordered_multiset[T,HASH=*,PRED=*,ALLOCATOR=*]:
        ctypedef T value_type

        cppclass iterator:
            T& operator*()
            iterator& operator++()
            bint operator==(const iterator&)
            bint operator!=(const iterator&)
        cppclass const_iterator:
            const_iterator(iterator)
            const T& operator*()
            const_iterator& operator++()
            bint operator==(const const_iterator&)
            bint operator!=(const const_iterator&)

        unordered_multiset() except +
        unordered_multiset(unordered_multiset&) except +
        #unordered_multiset& operator=(unordered_multiset&)
        bint operator==(unordered_multiset&, unordered_multiset&)
        bint operator!=(unordered_multiset&, unordered_multiset&)
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
        iterator insert(const_iterator, const T&) except +
        void insert[InputIt](InputIt, InputIt) except +
        size_t max_size()
        size_t size()
        void swap(unordered_multiset&)
        #value_compare value_comp()
        void max_load_factor(float)
        float max_load_factor()
        float load_factor()
        void rehash(size_t)
        void reserve(size_t)
        size_t bucket_count()
        size_t max_bucket_count()
        size_t bucket_size(size_t)
        size_t bucket(const T&)
