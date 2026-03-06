# mode: run

cimport cython

cdef extern from *:
    """
    #if __PYX_LIMITED_VERSION_HEX < 0x030C0000
    // Replacement functions for older versions of Python.
    // (It would be better to use functions which are always available
    // but DW didn't realise these were version-dependent when he wrote the
    // tests, and it doesn't really invalidate the tests anyway.)
    static PyObject *PyException_GetArgs(PyObject *ex) {
        return PyObject_GetAttrString(ex, "args");
    }

    static void PyException_SetArgs(PyObject *ex, PyObject *value) {
        if (PyObject_SetAttrString(ex, "args", value) < 0) {
            PyErr_WriteUnraisable(NULL);
            PyErr_Clear();
        }
    }
    #endif
    """

    object PyException_GetArgs(object)
    void PyException_SetArgs(object, object) noexcept

    # Exception is just an easy class to use to test arbitrary getters/setters
    # without needing to define our own class.
    ctypedef class __builtin__.Exception[object PyObject, check_size ignore]:
        @property
        cdef inline args_obj(self):
            return PyException_GetArgs(self)

        @args_obj.setter
        cdef inline void args_obj(self, obj):
            PyException_SetArgs(self, obj)

        @property
        cdef inline int arg0_int(self):
            # Fails if there isn't at least one argument, or it isn't an int
            return PyException_GetArgs(self)[0]

        @arg0_int.setter
        cdef inline void arg0_int(self, int value):
            PyException_SetArgs(self, (value,))

        # This property returns the first arg whatever it is,
        # but only accepts a C string.
        @property
        cdef inline arg0_mixed_str(self):
            # Fails if there isn't at least one argument
            return PyException_GetArgs(self)[0]

        @arg0_mixed_str.setter
        cdef inline void arg0_mixed_str(self, const char* value):
            PyException_SetArgs(self, (value,))

        # This property returns the first argument as a double,
        # but accepts any Python object
        @property
        cdef inline double arg0_mixed_double(self):
            # Fails if there isn't at least one argument and it isn't a double
            return PyException_GetArgs(self)[0]

        @arg0_mixed_double.setter
        cdef inline void arg0_mixed_double(self, value):
            PyException_SetArgs(self, (value,))


@cython.test_assert_path_exists("//SimpleCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_get_obj(Exception e):
    """
    >>> test_get_obj(Exception(1, 2))
    (1, 2)
    >>> test_get_obj(Exception())
    ()
    """
    return e.args_obj

@cython.test_assert_path_exists("//SimpleCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_get_obj_temp(*args):
    """
    >>> test_get_obj_temp(1, 2)
    (1, 2)
    >>> test_get_obj_temp()
    ()
    """
    return Exception(*args).args_obj

@cython.test_assert_path_exists("//SimpleCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_set_obj(o):
    """
    >>> test_set_obj((1, 2))
    Exception(1, 2)
    >>> test_set_obj(())
    Exception()
    """
    e = Exception()
    e.args_obj = o
    return e

def forward(o):
    return o

@cython.test_assert_path_exists("//SimpleCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_set_obj_from_temp(o):
    """
    >>> test_set_obj_from_temp((1, 2))
    Exception(1, 2)
    >>> test_set_obj_from_temp(())
    Exception()
    """
    e = Exception()
    e.args_obj = forward(o)
    return e

@cython.test_assert_path_exists("//SimpleCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_set_obj_temp(*args):
    """
    Setting to a temp isn't hugely useful because we can't check the result
    so it's mostly a no-crash test
    >>> test_set_obj_temp(1, 2)
    >>> test_set_obj_temp()
    """
    Exception().args_obj = args

@cython.test_assert_path_exists("//SimpleCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_get_int(Exception e):
    """
    >>> test_get_int(Exception(10))
    10
    >>> test_get_int(Exception())  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    IndexError: ...
    >>> test_get_int(Exception(None))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: ...
    """
    return e.arg0_int

@cython.test_assert_path_exists("//SimpleCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_set_int(value):
    """
    >>> test_set_int(10)
    Exception(10)
    >>> test_set_int(None)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: ...
    """
    e = Exception()
    e.arg0_int = value
    return e

@cython.test_assert_path_exists("//SimpleCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_mixed_str(const char* s):
    """
    >>> test_mixed_str(b"Hello")
    b'Hello'
    """
    e = Exception()
    e.arg0_mixed_str = s
    return e.arg0_mixed_str

@cython.test_assert_path_exists("//SimpleCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_fail_mixed_str(v):
    """
    >>> test_fail_mixed_str([1, 2, 3])  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: ...
    """
    Exception().arg0_mixed_str = v

@cython.test_assert_path_exists("//SimpleCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_mixed_double(v):
    """
    >>> test_mixed_double(5.5)
    5.5
    """
    e = Exception()
    e.arg0_mixed_double = v
    return e.arg0_mixed_double

@cython.test_assert_path_exists("//SimpleCallNode")
@cython.test_fail_if_path_exists("//AttributeNode")
def test_fail_mixed_double(Exception e):
    """
    >>> test_fail_mixed_double(Exception("not a double"))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: ...
    """
    return e.arg0_mixed_double
