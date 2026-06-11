# cython: auto_cpdef=True
# mode:run
# tag: directive,auto_cpdef,closures

# Closure functions ARE now promoted to cpdef with auto_cpdef=True.
def closure_func(x):
    """
    >>> c = closure_func(2)
    >>> c()
    2
    """
    def c():
        return x
    return c

# Generator functions ARE now promoted to cpdef with auto_cpdef=True (Part B).
# The __pyx_f_ function forwards to __pyx_pf_ which creates the generator object.
def generator_func():
    """
    >>> for i in generator_func(): print(i)
    1
    2
    """
    yield 1
    yield 2
