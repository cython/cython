# mode: error

cdef class Foo:
    pass

def ext_type(Foo x not None = None):
    pass

def builtin_type(str s not None = None):
    pass

def untyped(x not None = None):
    pass

def object_type(object o not None = None):
    pass

# This should remain valid (no not None)
def valid_default(Foo x = None):
    pass

# This should remain valid (not None without default)
def valid_not_none(Foo x not None):
    pass

# This should remain valid (or None with default)
def valid_or_none(Foo x or None = None):
    pass

_ERRORS = u"""
6:13: Parameter 'x' is declared 'not None' but has a default value of None
9:17: Parameter 's' is declared 'not None' but has a default value of None
12:12: Parameter 'x' is declared 'not None' but has a default value of None
15:16: Parameter 'o' is declared 'not None' but has a default value of None
"""
