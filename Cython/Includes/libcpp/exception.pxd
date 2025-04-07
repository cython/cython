from libcpp cimport bool

cdef extern from "<exception>" namespace "std" nogil:
    cdef cppclass exception_ptr:
        bool operator bool()

    exception_ptr make_exception_ptr[E](E e) noexcept
    void rethrow_exception(exception_ptr) except +
    # current_exception skipped because it'll be almost impossible to use from Cython

cdef extern from *:
    """
    CYTHON_UNUSED static void __pyx_deallocate_exception_ptr_capsule(PyObject *c) {
        std::exception_ptr *ptr = static_cast<std::exception_ptr*>(
            PyCapsule_GetPointer(c, "std::exception_ptr wrapper"));
        delete ptr;
        PyErr_Clear();
    }

    CYTHON_UNUSED static void __pyx_to_exception_ptr() {
        try {
            throw;
        } catch (...) {
            std::exception_ptr *current = new std::exception_ptr(std::current_exception());
            PyObject *capsule = PyCapsule_New(
                static_cast<void*>(current),
                "std::exception_ptr wrapper",
                &__pyx_deallocate_exception_ptr_capsule);
            if (!capsule)
                delete current;  // otherwise it'll be leaked
            else
                PyErr_SetObject(PyExc_Exception, capsule);
        }
    }

    CYTHON_UNUSED static std::exception_ptr __pyx_wrapped_exception_ptr_from_exception(PyObject *e) {
        PyObject *args = NULL, *arg0 = NULL;
        std::exception_ptr result;
        Py_ssize_t size;
#if __PYX_LIMITED_VERSION_HEX < 0x030C0000
        args = PyObject_GetAttrString(e, "args");
#else
        args = PyException_GetArgs(e);
#endif
        if (!args)
            goto done;
        size = PyTuple_Size(args);
        if (size == -1)
            goto done;
        if (size != 1) {
            PyErr_SetString(PyExc_ValueError, "exception args were not the expected length of 1");
            goto done;
        }
        arg0 = PyTuple_GetItem(args, 0);
        if (!arg0)
            goto done;
        {
            std::exception_ptr* wrapped = static_cast<std::exception_ptr*>(
                PyCapsule_GetPointer(arg0, "std::exception_ptr wrapper"));
            if (!wrapped) {
                goto done;
            }
            result = *wrapped;
        }

      done:
        Py_XDECREF(args);
        return result;
    }
    """
    # This can be used as `except +exception_ptr_error_handler`.
    # It raises a generic Exception, with a wrapped exception_ptr as its value.
    void exception_ptr_error_handler "__pyx_to_exception_ptr"() except *
    # Extract the exception_ptr from a caught exception
    exception_ptr wrapped_exception_ptr_from_exception "__pyx_wrapped_exception_ptr_from_exception"(e) except *
