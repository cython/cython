# ticket: 408

__doc__ = """
>>> call_with_tuple(1, 1.2, 'test', [1,2,3])
(1, 1.2, 'test', [1, 2, 3])

>>> call_with_list(1, 1.2, None, None)
(1, 1.2, None, None)
"""

cdef c_function(int a, float b, c, list d):
    return a,b,c,d

def call_with_tuple(*args):
    return c_function(*args)

def call_with_list(*args):
    args = list(args)
    return c_function(*args)
