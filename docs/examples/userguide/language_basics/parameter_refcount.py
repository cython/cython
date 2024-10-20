# Py_REFCNT and _Py_REFCNT are the same, except _Py_REFCNT takes
# a raw pointer and Py_REFCNT takes a normal Python object
from cython.cimports.cpython.ref import PyObject, _Py_REFCNT, Py_REFCNT

import sys

python_dict = {"abc": 123}
python_dict_refcount = Py_REFCNT(python_dict)

@cython.cfunc
def owned_reference(obj: object):
    refcount1 = Py_REFCNT(obj)
    print(f'Inside owned_reference initially: {refcount1}')
    another_ref_to_object = obj
    refcount2 = Py_REFCNT(obj)
    print(f'Inside owned_reference after new ref: {refcount2}')

@cython.cfunc
def borrowed_reference(obj: cython.pointer[PyObject]):
    refcount1 = _Py_REFCNT(obj)
    print(f'Inside borrowed_reference initially: {refcount1}')
    another_ptr_to_object = obj
    refcount2 = _Py_REFCNT(obj)
    print(f'Inside borrowed_reference after new pointer: {refcount2}')
    # Casting to a managed reference to call a cdef function doesn't increase the count
    refcount3 = Py_REFCNT(cython.cast(object, obj))
    print(f'Inside borrowed_reference with temporary managed reference: {refcount3}')
    # However calling a Python function may depending on the Python version and the number
    # of arguments.


print(f'Initial refcount: {python_dict_refcount}')
owned_reference(python_dict)
borrowed_reference(cython.cast(cython.pointer[PyObject], python_dict))
