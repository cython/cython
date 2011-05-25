# mode: error

with gil:
    pass

with nogil:
    with nogil:
        pass

cdef void without_gil() nogil:
   # This is not an error, as 'func' *may* be called without the GIL, but it
   # may also be held.
    with nogil:
        pass

cdef void with_gil() with gil:
    # This is an error, as the GIL is acquired already
    with gil:
        pass

def func():
    with gil:
        pass

_ERRORS = u'''
3:5: Trying to acquire the GIL while it is already held.
7:9: Trying to release the GIL while it was previously released.
18:9: Trying to acquire the GIL while it is already held.
22:9: Trying to acquire the GIL while it is already held.
'''
