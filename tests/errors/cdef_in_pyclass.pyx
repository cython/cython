# mode: error

class Pyclass(object):
    cdef bad(self):
        pass

_ERRORS = """
 4:9: cdef statement not allowed here
"""
