# cython: language_level=3, warn.maybe_uninitialized=True
# mode: error
# tag: werror

def ref(obj):
    pass

def list_comp(a):
    r = [i for i in a]
    ref(i)
    i = 0
    return r

def dict_comp(a):
    r = {i: j for i, j in a}
    ref(i)
    i = 0
    return r


_ERRORS = """
10:8: local variable 'i' referenced before assignment
16:8: local variable 'i' referenced before assignment
"""
