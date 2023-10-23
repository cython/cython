# mode: error

class Pyclass(object):
    fn bad(self):
        pass

_ERRORS = """
 4:4: cdef statement not allowed here
"""
