from cpython.ref cimport PyObject, _Py_REFCNT

import sys

python_dict = {"abc": 123}
python_dict_refcount = sys.getrefcount(python_dict)


cdef owned_reference(object obj):
    refcount = sys.getrefcount(python_dict)
    print('Inside owned_reference: {refcount}'.format(refcount=refcount))


cdef borrowed_reference(PyObject * obj):
    # use _Py_REFCNT instead of Py_REFCNT to avoid creating a new owned
    # reference just to get the reference count
    refcount = _Py_REFCNT(obj)
    print('Inside borrowed_reference: {refcount}'.format(refcount=refcount))


print('Initial refcount: {refcount}'.format(refcount=python_dict_refcount))
owned_reference(python_dict)
borrowed_reference(<PyObject *>python_dict)
