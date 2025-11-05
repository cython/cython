from cython.cimports.cpython.ref import PyObject

def main():

    python_string = "foo"

    # Note that the variables below are automatically inferred
    # as the correct pointer type that is assigned to them.
    # They do not need to be typed explicitly.

    ptr = cython.cast(cython.p_void, python_string)
    adress_in_c = cython.cast(Py_intptr_t, ptr)
    address_from_void = adress_in_c        # address_from_void is a python int

    ptr2 = cython.cast(cython.pointer[PyObject], python_string)
    address_in_c2 = cython.cast(Py_intptr_t, ptr2)
    address_from_PyObject = address_in_c2  # address_from_PyObject is a python int

    assert address_from_void == address_from_PyObject == id(python_string)

    print(cython.cast(object, ptr))                     # Prints "foo"
    print(cython.cast(object, ptr2))                    # prints "foo"
