# mode: run
# tag: closures
# ticket: t554

def call_f(x):
    """
    >>> call_f(2)
    4
    """
    return f(x)


cdef f(x):                # def  here => works fine
   def g(y): return y*x   # cdef here => compile error
   return g(x)            # faults@ INCREF(.*cur_scope->.*v_x


def closure_in_void():
    """
    >>> genex = closure_in_void()
    >>> list(genex)
    ['a', 'b', 'c']
    """
    l = []
    add_gen(l)
    return l[0]


cdef void add_gen(l):
    x = "abc"
    l.append((c for c in x))


def closure_in_int():
    """
    >>> genex = closure_in_int()
    >>> list(genex)
    ['a', 'b', 'c']
    """
    l = []
    add_gen_int(l)
    return l[0]


cdef int add_gen_int(l):
    x = "abc"
    l.append((c for c in x))
