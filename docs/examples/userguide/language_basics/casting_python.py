from cython.cimports.cpython.ref import PyObject

def main():

    python_string = "foo"

    ptr: p_void = cython.cast(cython.p_void, python_string)
    adress_in_c: Py_intptr_t= cython.cast(Py_intptr_t, ptr)
    address_from_void = adress_in_c        # address_from_void is a python int

    ptr2: cython.pointer(PyObject) = cython.cast(cython.pointer(PyObject), python_string)
    address_in_c2: Py_intptr_t= cython.cast(Py_intptr_t, ptr2)
    address_from_PyObject = address_in_c2  # address_from_PyObject is a python int

    assert address_from_void == address_from_PyObject == id(python_string)

    print(cython.cast(object, ptr))                     # Prints "foo"
    print(cython.cast(object, ptr2))                    # prints "foo"
