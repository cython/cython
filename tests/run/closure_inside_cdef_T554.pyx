# mode: run
# tag: closures
# ticket: 554

def call_f(x):
    """
    >>> call_f(2)
    4
    """
    return f(x)

cdef f(x):                # def  here => works fine
   def g(y): return y*x  # cdef here => compile error
   return g(x)           # faults@ INCREF(.*cur_scope->.*v_x
