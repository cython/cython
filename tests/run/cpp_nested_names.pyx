# tag: cpp

cimport cpp_nested_names

def test_nested_names():
    """
    >>> test_nested_names()
    B
    """
    cdef cpp_nested_names.A.B b = cpp_nested_names.A.get()
    print(b.get_str().decode('ascii'))
