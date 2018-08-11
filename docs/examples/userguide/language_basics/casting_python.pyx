from cpython.ref cimport PyObject

cdef extern from *:
    ctypedef Py_ssize_t Py_intptr_t

python_string = "foo"

cdef void* ptr = <void*>python_string
cdef Py_intptr_t adress_in_c = <Py_intptr_t>ptr
address_from_void = adress_in_c        # address_from_void is a python int

cdef PyObject* ptr2 = <PyObject*>python_string
cdef Py_intptr_t address_in_c2 = <Py_intptr_t>ptr2
address_from_PyObject = address_in_c2  # address_from_PyObject is a python int

assert address_from_void == address_from_PyObject == id(python_string)

print(<object>ptr)                     # Prints "foo"
print(<object>ptr2)                    # prints "foo"
