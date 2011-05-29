# cython: warn.unused=True, warn.unused_arg=True, warn.unused_result=True
# mode: error
# tag: werror

def unused_variable():
    a = 1

def unused_cascade(arg):
    a, b = arg.split()
    return a

def unused_arg(arg):
    pass

def unused_result():
    r = 1 + 1
    r = 2
    return r

def unused_nested():
    def unused_one():
        pass

def unused_class():
    class Unused:
        pass

# this should not generate warning
def used(x, y):
    x.y = 1
    y[0] = 1
    lambda x: x

def unused_and_unassigned():
    cdef object foo
    cdef int i

_ERRORS = """
6:6: Unused entry 'a'
9:9: Unused entry 'b'
12:15: Unused argument 'arg'
16:6: Unused result in 'r'
21:4: Unused entry 'unused_one'
25:4: Unused entry 'Unused'
35:16: Unused entry 'foo'
36:13: Unused entry 'i'
"""
