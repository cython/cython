from libcpp cimport bool

cdef extern from *:
    # Not part of the C++ interface, but declaring this here so it isn't nogil
    ctypedef void (*_once_func_type)() except+

cdef extern from "<mutex>" namespace "std" nogil:
    cppclass mutex:
        # may not be present, and we know nothing about it
        cppclass native_handle_type:
            pass

        void lock() except+
        bool try_lock()
        void unlock()

        native_handle_type native_handle() except+

    cppclass timed_mutex:
        # may not be present, and we know nothing about it
        cppclass native_handle_type:
            pass

        void lock() except+
        bool try_lock()
        bool try_lock_for[T](const T& duration) except+
        bool try_lock_until[T](const T& time_point) except+
        void unlock()

        native_handle_type native_handle() except+

    cppclass recursive_mutex:
        # may not be present, and we know nothing about it
        cppclass native_handle_type:
            pass

        void lock() except+
        bool try_lock()
        void unlock()

        native_handle_type native_handle() except+

    cppclass timed_recursive_mutex:
        # may not be present, and we know nothing about it
        cppclass native_handle_type:
            pass

        void lock() except+
        bool try_lock()
        bool try_lock_for[T](const T& duration) except+
        bool try_lock_until[T](const T& time_point) except+
        void unlock()

        native_handle_type native_handle() except+


    # tags
    cppclass defer_lock_t:
        pass
    defer_lock_t defer_lock
    cppclass try_to_lock_t:
        pass
    try_to_lock_t try_to_lock
    cppclass adopt_lock_t:
        pass
    adopt_lock_t adopt_lock

    # lock_guard is probably unusable without cpp_locals because it
    # can't be default-constructed or moved.
    cppclass lock_guard[T]:
        ctypedef T mutex_type
        lock_guard(mutex_type&) except+
        lock_guard(mutex_type&, adopt_lock_t)

    cppclass unique_lock[T]:
        ctypedef T mutex_type
        unique_lock()
        # This covers both the plain regular constructor, the 3 versions with tags
        # and two std::chrono constructors.  The two templated chrono versions stop
        # us from declaring the overloads explicitly.
        unique_lock(mutex_type&, ...) except+
        #unique_lock(mutex_type&, defer_lock_t)
        #unique_lock(mutex_type&, try_to_lock_t) except+
        ## this feels like it should be noexcet, but cppreference implies it isn't
        #unique_lock(mutex_type&, adopt_lock_t) except+

        void lock() except+
        bool try_lock() except+
        bool try_lock_for[T](const T& duration) except+
        bool try_lock_until[T](const T& time_point) except+
        void unlock() except+

        void swap(unique_lock& other)
        # "release" is definitely not the same as unlock. Noted here because
        # DW always makes this mistake and regrets it and wants to save you
        # from the same fate.
        mutex_type* release()

        mutex_type* mutex()
        bool owns_lock()
        bool operator bool()

    # scoped lock is probably unusable without cpp_locals.
    # It's also a variadic template type so can take potentially unlimited number of
    # arguments. Cython doesn't support this, so if you want more than 26 arguments,
    # you're on your own.
    cppclass scoped_lock[A=*, B=*, C=*, D=*, E=*, F=*, G=*, H=*, I=*, J=*, K=*,
                         L=*, M=*, N=*, O=*, P=*, Q=*, R=*, S=*, T=*, U=*, V=*,
                         W=*, X=*, Y=*, Z=*]:
        scoped_lock(...) except+

    cppclass once_flag:
        pass

    bool try_lock(...) except+
    void lock(...) except+

    # If we're passed a cdef function, make sure that it's specified without Python exceptions.
    void call_once(once_flag&, _once_func_type callable) except +
    void call_once[Callable](once_flag&, Callable& callable,  ...) except +
