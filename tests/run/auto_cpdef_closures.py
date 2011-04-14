# cython: auto_cpdef=True
# mode:run
# tag: directive,auto_cpdef,closures

def closure_func(x):
    """
    >>> c = closure_func(2)
    >>> c()
    2
    """
    def c():
        return x
    return c

def generator_func():
    """
    >>> for i in generator_func(): print(i)
    1
    2
    """
    yield 1
    yield 2
