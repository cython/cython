# mode: run

# This test abuses the cname feature to modify the utility code so we can find out
# if the indexing functions are being called with unsafe_shared set.
# Then it checks if that matches our expectations.

# Don't worry about actually compiling with OpenMP though.
from cython.parallel cimport prange

# Intercept list indexing calls and record whether "unsafe_shared" was set
cdef extern from *:
    """
    static int unsafe_shared_set;

    static PyObject *__Pyx_GetItemInt_List_Fast(PyObject *o, Py_ssize_t i,
                                                int wraparound, int boundscheck, int unsafe_shared);
    static PyObject *Call_GetItemInt_List_Fast(PyObject *o, Py_ssize_t i,
                                                int wraparound, int boundscheck, int unsafe_shared) {
        int unique = (unsafe_shared == __Pyx_ReferenceSharing_DefinitelyUnique) || 
                     (unsafe_shared == __Pyx_ReferenceSharing_OwnStrongReference);
        unsafe_shared_set = !unique;
        return __Pyx_GetItemInt_List_Fast(o, i, wraparound, boundscheck, unsafe_shared);
    }

    #define do_nothing()
    """
    bint unsafe_shared_set
    void undef_getitemint_list_fast "#undef __Pyx_GetItemInt_List_Fast \n do_nothing" ()
    void define_new_getitemint_list_fast "#define __Pyx_GetItemInt_List_Fast(o, i, wraparound, boundscheck, unsafe_shared) Call_GetItemInt_List_Fast(o, i, wraparound, boundscheck, unsafe_shared) \n do_nothing" ()


def dummy_func():
    # abuse cname feature to redefine __Pyx_GetItemInt_List_Fast so that we can intercept the call
    define_new_getitemint_list_fast()

def local_var():
    """
    >>> local_var()
    False
    """
    global unsafe_shared_set
    unsafe_shared_set = False
    cdef list l = [None]
    x = l[0]
    return unsafe_shared_set

def closure1():
    """
    >>> closure1()
    True
    """
    global unsafe_shared_set
    unsafe_shared_set = False
    l = [None]

    def function_that_captures_l():
        return l
    x = l[0]
    return unsafe_shared_set

def closure2():
    """
    >>> closure2()
    True
    """
    global unsafe_shared_set
    unsafe_shared_set = False
    l = [None]

    def function_that_captures_l():
        return l[0]
    x = function_that_captures_l()
    return unsafe_shared_set

cdef class ListAttr:
    cdef list l
    def __init__(self):
        self.l = [None]

    def test_list_attr(self):
        """
        >>> ListAttr().test_list_attr()
        True
        """
        global unsafe_shared_set
        unsafe_shared_set = False
        x = self.l[0]
        return unsafe_shared_set


def in_prange():
    """
    >>> in_prange()
    True
    """
    global unsafe_shared_set
    unsafe_shared_set = False
    l = [None]
    for i in prange(1, nogil=True):
        with gil:
            x = l[0]
    return unsafe_shared_set


def dummy_func2():
    # abuse cname feature to undefine our override to allow the utility code to be generated
    undef_getitemint_list_fast()
