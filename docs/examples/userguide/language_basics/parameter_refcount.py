from cython.cimports.cpython.ref import PyObject

import sys

python_dict = {"abc": 123}
python_dict_refcount = sys.getrefcount(python_dict)

@cython.cfunc
def owned_reference(obj: object):
    refcount = sys.getrefcount(python_dict)
    print(f'Inside owned_reference: {refcount}')

@cython.cfunc
def borrowed_reference(obj: cython.pointer(PyObject)):
    refcount = obj.ob_refcnt
    print(f'Inside borrowed_reference: {refcount}')

def main():
    print(f'Initial refcount: {python_dict_refcount}')
    owned_reference(python_dict)
    borrowed_reference(cython.cast(cython.pointer(PyObject), python_dict))
