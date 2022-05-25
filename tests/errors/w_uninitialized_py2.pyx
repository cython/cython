# cython: language_level=2, warn.maybe_uninitialized=True
# mode: error
# tag: werror

def list_comp(a):
    r = [i for i in a]
    return i

# dict comp is py3 feuture and don't leak here
def dict_comp(a):
    r = {i: j for i, j in a}
    return i, j

def dict_comp2(a):
    r = {i: j for i, j in a}
    print i, j
    i, j = 0, 0


_ERRORS = """
7:11: local variable 'i' might be referenced before assignment
12:11: undeclared name not builtin: i
12:14: undeclared name not builtin: j
16:10: local variable 'i' referenced before assignment
16:13: local variable 'j' referenced before assignment
"""
