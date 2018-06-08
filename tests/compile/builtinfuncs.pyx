# mode: compile

cdef int f() except -1:
    cdef object x, y = 0, z = 0, w = 0
    cdef str sstring
    cdef basestring sustring
    cdef int i
    cdef long lng
    cdef Py_ssize_t s
    x = abs(y)
    delattr(x, 'spam')
    x = dir(y)
    x = divmod(y, z)
    x = getattr(y, 'spam')
    i = hasattr(y, 'spam')
    lng = hash(y)
    x = intern(y)
    i = isinstance(y, z)
    i = issubclass(y, z)
    x = iter(y)
    s = len(x)
    x = open(y, z)
    x = pow(y, z, w)
    x = pow(y, z)
    x = reload(y)
    x = repr(y)
    sstring = repr(x)
    sustring = repr(x)
    setattr(x, y, z)
    #i = typecheck(x, y)
    #i = issubtype(x, y)
    x = abs

def not_called():
    response = raw_input('xyz')

f()
