from libc.setjmp cimport *

cdef void check_nonzero(jmp_buf ctx, int x) nogil:
    if x == 0:
        longjmp(ctx, 1)

def nonzero(int x):
    """
    >>> nonzero(-1)
    True
    >>> nonzero(0)
    False
    >>> nonzero(1)
    True
    >>> nonzero(2)
    True

    """
    cdef jmp_buf ctx
    if setjmp(ctx) == 0:
        check_nonzero(ctx, x)
        return True
    else:
        return False


from libc.string cimport strcpy
cdef char[256] error_msg
cdef jmp_buf error_ctx
cdef void error(char msg[]) nogil:
    strcpy(error_msg,msg)
    longjmp(error_ctx, 1)

cdef void c_call(int x) nogil:
    if x<=0:
        error(b"expected a positive value")

def execute_c_call(int x):
    """
    >>> execute_c_call(+2)
    >>> execute_c_call(+1)
    >>> execute_c_call(+0)
    Traceback (most recent call last):
      ...
    RuntimeError: expected a positive value
    >>> execute_c_call(-1)
    Traceback (most recent call last):
      ...
    RuntimeError: expected a positive value
    """
    if not setjmp(error_ctx):
        c_call(x)
    else:
        raise RuntimeError(error_msg.decode())
