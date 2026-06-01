 
cpdef void is_in(Py_UCS4 uchar_val):
    if uchar_val in u'abcABCxY':
        print("The character is in the string.")
    else:
        print("The character is not in the string")
