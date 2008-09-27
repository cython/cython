__doc__ = """
sage: get_locals(1,2,3)
{'args': (2, 3), 'kwds': {}, 'x': 1, 'y': 'hi', 'z': 5}
"""

def get_locals(x, *args, **kwds):
    y = "hi"
    cdef int z = 5
    return locals()
