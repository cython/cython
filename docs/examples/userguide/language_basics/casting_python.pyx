from cpython.ref cimport PyObject
from libc.stdint cimport uintptr_t

python_string = "foo"

cdef void* ptr = <void*>python_string
cdef uintptr_t adress_in_c = <uintptr_t>ptr
address_from_void = adress_in_c        # address_from_void is a python int

cdef PyObject* ptr2 = <PyObject*>python_string
cdef uintptr_t address_in_c2 = <uintptr_t>ptr2
address_from_PyObject = address_in_c2  # address_from_PyObject is a python int

assert address_from_void == address_from_PyObject == id(python_string)

print(<object>ptr)                     # Prints "foo"
print(<object>ptr2)                    # prints "foo"
