# cython: language_level=3, warn.maybe_uninitialized=True
# mode: error
# tag: werror

def list_comp(a):
    r = [i for i in a]
    print(i)
    i = 0
    return r

def dict_comp(a):
    r = {i: j for i, j in a}
    print(i)
    i = 0
    return r


_ERRORS = """
7:11: local variable 'i' referenced before assignment
13:11: local variable 'i' referenced before assignment
"""
