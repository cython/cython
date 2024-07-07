@cython.ccall
def is_in(uchar_val: cython.Py_UCS4) -> cython.void:
    if uchar_val in u'abcABCxY':
        print("The character is in the string.")
    else:
        print("The character is not in the string")
