char_or_float = cython.fused_type(cython.char, cython.double)



@cython.ccall
def plus_one(var: char_or_float) -> char_or_float:
    return var + 1


def show_me():

    a: cython.char = 127
    b: cython.double = 127
    print('char', plus_one(a))
    print('float', plus_one(b))
