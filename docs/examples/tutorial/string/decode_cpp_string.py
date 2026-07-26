# distutils: language = c++

from cython.cimports.libcpp.string import string

def get_ustrings():
    s: string = string(b'abcdefg')

    ustring1 = s.decode('UTF-8')
    ustring2 = s[2:-2].decode('UTF-8')
    return ustring1, ustring2
