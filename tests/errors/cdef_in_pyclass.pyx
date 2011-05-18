class Pyclass(object):
    cdef bad(self):
        pass

_ERRORS = """
 2:9: cdef statement not allowed here
"""
