from cython.cimports.cpython.ref import PyObject, _Py_REFCNT

import sys

python_dict = {"abc": 123}
python_dict_refcount = sys.getrefcount(python_dict)

@cython.cfunc
def owned_reference(obj: object):
    refcount = sys.getrefcount(python_dict)
    print('Inside owned_reference: {refcount}'.format(refcount=refcount))

@cython.cfunc
def borrowed_reference(obj: cython.pointer(PyObject)):
    # use _Py_REFCNT instead of Py_REFCNT to avoid creating a new owned
    # reference just to get the reference count
    refcount = _Py_REFCNT(obj)
    print('Inside borrowed_reference: {refcount}'.format(refcount=refcount))

def main():
    print('Initial refcount: {refcount}'.format(refcount=python_dict_refcount))
    owned_reference(python_dict)
    borrowed_reference(cython.cast(cython.pointer(PyObject), python_dict))
