from libcpp cimport bool, nullptr_t, nullptr

cdef extern from "<memory>" namespace "std" nogil:

    cdef cppclass unique_ptr[T]:
        unique_ptr()
        unique_ptr(nullptr_t)
        unique_ptr(T*)
        unique_ptr(unique_ptr[T]&)

        # Modifiers
        T* release()
        void reset()
        void reset(nullptr_t)
        void reset(T*)
        void swap(unique_ptr&)

        # Observers
        T* get()
        T& operator*()
        #T* operator->() # Not Supported
        bool operator bool()
        bool operator!()

        bool operator==(const unique_ptr&)
        bool operator!=(const unique_ptr&)
        bool operator<(const unique_ptr&)
        bool operator>(const unique_ptr&)
        bool operator<=(const unique_ptr&)
        bool operator>=(const unique_ptr&)

        bool operator==(nullptr_t)
        bool operator!=(nullptr_t)

    # Forward Declaration not working ("Compiler crash in AnalyseDeclarationsTransform")
    #cdef cppclass weak_ptr[T]

    cdef cppclass shared_ptr[T]:
        shared_ptr()
        shared_ptr(nullptr_t)
        shared_ptr(T*)
        shared_ptr(shared_ptr[T]&)
        shared_ptr(shared_ptr[T]&, T*)
        shared_ptr(unique_ptr[T]&)
        #shared_ptr(weak_ptr[T]&) # Not Supported

        # Modifiers
        void reset()
        void reset(T*)
        void swap(shared_ptr&)

        # Observers
        T* get()
        T& operator*()
        #T* operator->() # Not Supported
        long use_count()
        bool unique()
        bool operator bool()
        bool operator!()
        #bool owner_before[Y](const weak_ptr[Y]&) # Not Supported
        bool owner_before[Y](const shared_ptr[Y]&)

        bool operator==(const shared_ptr&)
        bool operator!=(const shared_ptr&)
        bool operator<(const shared_ptr&)
        bool operator>(const shared_ptr&)
        bool operator<=(const shared_ptr&)
        bool operator>=(const shared_ptr&)

        bool operator==(nullptr_t)
        bool operator!=(nullptr_t)

    cdef cppclass weak_ptr[T]:
        weak_ptr()
        weak_ptr(weak_ptr[T]&)
        weak_ptr(shared_ptr[T]&)

        # Modifiers
        void reset()
        void swap(weak_ptr&)

        # Observers
        long use_count()
        bool expired()
        shared_ptr[T] lock()
        bool owner_before[Y](const weak_ptr[Y]&)
        bool owner_before[Y](const shared_ptr[Y]&)
