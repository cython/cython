# mode: run

def f(x, y):
    x = y


cdef void g(int i, float f, char *p):
    f = i


cdef h(int i, obj):
    i = obj


def z(a, b, c):
    """
    >>> z(1,9.2, b'test')
    """
    f(a, b)
    f(a, b,)
    g(1, 2.0, "spam")
    g(a, b, c)


def fail0(a, b):
    """
    >>> fail0(1,2)
    Traceback (most recent call last):
    TypeError: f() takes exactly 2 positional arguments (0 given)
    """
    f()


def fail1(a, b):
    """
    >>> fail1(1,2)
    Traceback (most recent call last):
    TypeError: f() takes exactly 2 positional arguments (1 given)
    """
    f(a)


def failtype():
    """
    >>> failtype()
    Traceback (most recent call last):
    TypeError: an integer is required
    """
    h(42, "eggs")
