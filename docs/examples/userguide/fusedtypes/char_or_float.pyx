from __future__ import print_function

ctypedef fused char_or_float:
    i8
    f32

cpdef char_or_float plus_one(char_or_float var):
    return var + 1

def show_me():
    cdef:
        i8 a = 127
        f32 b = 127
    print('char', plus_one(a))
    print('float', plus_one(b))
