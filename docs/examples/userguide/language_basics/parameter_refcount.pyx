from __future__ import print_function

from cpython.ref cimport PyObject

import sys

python_string = "foo"
python_string_refcount = sys.getrefcount(python_string)

cdef owned_reference(object obj):
    refcount = sys.getrefcount(python_string)
    print('Inside owned_reference: {refcount}'.format(refcount=refcount))

cdef borrowed_reference(PyObject * obj):
    refcount = obj.ob_refcnt
    print('Inside borrowed_reference: {refcount}'.format(refcount=refcount))

print('Initial refcount: {refcount}'.format(refcount=python_string_refcount))
owned_reference(python_string)
borrowed_reference(<PyObject *>python_string)
