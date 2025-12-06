from libcpp cimport bool

cdef extern from "<exception>" namespace "std" nogil:
    cdef cppclass exception_ptr:
        bool operator bool()

    exception_ptr make_exception_ptr[E](E e) noexcept
    void rethrow_exception(exception_ptr) except +
    exception_ptr current_exception() noexcept

    cdef cppclass exception:
        const char* what() noexcept

cdef extern from "<stdexcept>" namespace "std" nogil:
    # Omitting the constructors of derived exception classes for now.
    # They can't be stack-allocated easily in Cython because they don't have
    # a nullary constructor. They also can't be thrown in Cython.
    # So they're most useful just as class names when implementing
    # exception handlers.
    cdef cppclass logic_error(exception):
        pass
    cdef cppclass invalid_argument(logic_error):
        pass
    cdef cppclass domain_error(logic_error):
        pass
    cdef cppclass length_error(logic_error):
        pass
    cdef cppclass out_of_range(logic_error):
        pass

    cdef cppclass runtime_error(exception):
        pass
    cdef cppclass range_error(runtime_error):
        pass
    cdef cppclass overflow_error(runtime_error):
        pass

    cdef cppclass bad_typeid(exception):
        pass

    cdef cppclass bad_cast(exception):
        pass

    cdef cppclass bad_alloc(exception):
        pass

    cdef cppclass bad_exception(exception):
        pass


cdef extern from *:
    """
    static void __Pyx_CppExn2PyErr(void);

    CYTHON_UNUSED static void __pyx_deallocate_exception_ptr_capsule(PyObject *c) {
        std::exception_ptr *ptr = static_cast<std::exception_ptr*>(
            PyCapsule_GetPointer(c, "std::exception_ptr wrapper"));
        delete ptr;
        PyErr_Clear();
    }

    CYTHON_UNUSED static void __pyx_to_exception_ptr() {
        try {
            __Pyx_CppExn2PyErr(); // First do regular exception conversion
            throw;
        } catch (...) {
            PyObject *type, *value, *tb;
            PyErr_Fetch(&type, &value, &tb);
            Py_XDECREF(value);
            Py_XDECREF(tb);
            std::exception_ptr *current = new std::exception_ptr(std::current_exception());
            PyObject *capsule = PyCapsule_New(
                static_cast<void*>(current),
                "std::exception_ptr wrapper",
                &__pyx_deallocate_exception_ptr_capsule);
            if (!capsule)
                delete current;  // otherwise it'll be leaked
            else
                PyErr_SetObject(type ? type : PyExc_Exception, capsule);
            Py_DECREF(type);
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
        if (size != 1) {
            if (size != -1)
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

# Dummy inline function to force __Pyx_CppExn2PyErr to be included for utility code above
cdef inline void __pyx_call_rethrow_exception "__pyx_call_rethrow_exception"(exception_ptr e) except*:
    rethrow_exception(e)


cdef extern from *:
    """
    namespace {
        #if __cplusplus >= 201703L
        template <typename ExceptionT>
        bool __pyx_call_exception_handler(std::exception_ptr e_ptr, void (*handler)(ExceptionT&)) {
            try {
                std::rethrow_exception(e_ptr);
            } catch(ExceptionT &ex) {
                handler(ex);
                return static_cast<bool>(PyErr_Occurred());
            } catch (...) {
                return false;
            }
        }

        bool __pyx_call_exception_handler(std::exception_ptr e_ptr, void(*handler)()) {
            try {
                std::rethrow_exception(e_ptr);
            } catch (...) {
                handler();
                return static_cast<bool>(PyErr_Occurred());
            }
        }

        template <typename ...HandlerTs>
        void __pyx_delegate_to_exception_handlers(HandlerTs&& ... handlers) {
            auto e_ptr = std::current_exception();
            if (!e_ptr) {
                PyErr_SetString(PyExc_SystemError, "__pyx_delegrate_to_exception_handlers called without a C++ exception");
                return;
            }
            bool handled = (__pyx_call_exception_handler(e_ptr, std::forward<HandlerTs>(handlers)) || ... );
            if (!handled)
                std::rethrow_exception(e_ptr);
        }

        // MSVC defaults to C++14 as of 2025. If set to use a higher standard then it copes
        // fine with the code above. However, it doesn't like to make it easy to detect by
        // default.
        #elif __cplusplus >= 201103L || defined(_MSC_VER)

        bool __pyx_call_exception_handler_recursive(std::exception_ptr) {
            return false;
        }

        template <typename ExceptionT, typename ...HandlerTs>
        bool __pyx_call_exception_handler_recursive(std::exception_ptr e_ptr, void (*first_handler)(ExceptionT&), HandlerTs&& ...handlers);

        template <typename ...HandlerTs>
        bool __pyx_call_exception_handler_recursive(std::exception_ptr e_ptr, void (*first_handler)(), HandlerTs&& ...handlers) {
            try {
                std::rethrow_exception(e_ptr);
            } catch (...) {
                first_handler();
                if (static_cast<bool>(PyErr_Occurred())) return true;
            }
            return __pyx_call_exception_handler_recursive(std::move(e_ptr), std::forward<HandlerTs>(handlers)...);
        }

        template <typename ExceptionT, typename ...HandlerTs>
        bool __pyx_call_exception_handler_recursive(std::exception_ptr e_ptr, void (*first_handler)(ExceptionT&), HandlerTs&& ...handlers) {
            try {
                std::rethrow_exception(e_ptr);
            } catch (ExceptionT& e) {
                first_handler(e);
                if (static_cast<bool>(PyErr_Occurred())) return true;
            } catch (...) {}
            return __pyx_call_exception_handler_recursive(std::move(e_ptr), std::forward<HandlerTs>(handlers)...);
        }

        template <typename ...HandlerTs>
        void __pyx_delegate_to_exception_handlers(HandlerTs&& ... handlers) {
            auto e_ptr = std::current_exception();
            if (!e_ptr) {
                PyErr_SetString(PyExc_SystemError, "__pyx_delegrate_to_exception_handlers called without a C++ exception");
                return;
            }
            bool handled = __pyx_call_exception_handler_recursive(e_ptr, std::forward<HandlerTs>(handlers)...);
            if (!handled)
                std::rethrow_exception(e_ptr);
        }
        #endif
    } // empty namespace
    """
    # Convenience function for writing easy custom C++ exception handlers.
    # Pass it a collection of C++ function pointers taking either an exception reference, or no arguments.
    # The function pointers are tried in order. If their argument type matches the current C++ exception (or if
    # their argument type is empty) then they are called.
    # If they raise a Python exception then the exception handling finishes and that exception is raised.
    # Otherwise the next handler will be called.
    # If no handlers raise a Python exception then the default Cython mechanism will be used.
    void delegate_to_exception_handlers "__pyx_delegate_to_exception_handlers"(...) except+*
