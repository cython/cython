# mode: compile

cdef int f() except -1:
    cdef object x, y = 0, z = 0, w = 0
    cdef int i
    x = abs(y)
    delattr(x, 'spam')
    x = dir(y)
    x = divmod(y, z)
    x = getattr(y, 'spam')
    i = hasattr(y, 'spam')
    i = hash(y)
    x = intern(y)
    i = isinstance(y, z)
    i = issubclass(y, z)
    x = iter(y)
    i = len(x)
    x = open(y, z)
    x = pow(y, z, w)
    x = pow(y, z)
    x = reload(y)
    x = repr(y)
    setattr(x, y, z)
    #i = typecheck(x, y)
    #i = issubtype(x, y)
    x = abs

f()
