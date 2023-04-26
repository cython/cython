# mode: run

# __getattribute__ and __getattr__ special methods for a single class.


cdef class just_getattribute:
    """
    >>> a = just_getattribute()
    >>> a.called
    1
    >>> a.called
    2
    >>> a.bar
    'bar'
    >>> a.called
    4
    >>> try: a.invalid
    ... except AttributeError: pass
    ... else: print("NOT RAISED!")
    >>> a.called
    6
    """
    cdef readonly int called
    def __getattribute__(self,n):
        self.called += 1
        if n == 'bar':
            return n
        elif n == 'called':
            return self.called
        else:
            raise AttributeError


cdef class just_getattr:
    """
    >>> a = just_getattr()
    >>> a.called
    0
    >>> a.called
    0
    >>> a.foo
    10
    >>> a.called
    0
    >>> a.bar
    'bar'
    >>> a.called
    1
    >>> try: a.invalid
    ... except AttributeError: pass
    ... else: print("NOT RAISED!")
    >>> a.called
    2
    """
    cdef readonly int called
    cdef readonly int foo
    def __init__(self):
        self.foo = 10
    def __getattr__(self,n):
        self.called += 1
        if n == 'bar':
            return n
        else:
            raise AttributeError


cdef class both:
    """
    >>> a = both()
    >>> (a.called_getattr, a.called_getattribute)
    (0, 2)
    >>> a.foo
    10
    >>> (a.called_getattr, a.called_getattribute)
    (0, 5)
    >>> a.bar
    'bar'
    >>> (a.called_getattr, a.called_getattribute)
    (1, 8)
    >>> try: a.invalid
    ... except AttributeError: pass
    ... else: print("NOT RAISED!")
    >>> (a.called_getattr, a.called_getattribute)
    (2, 11)
    """
    cdef readonly int called_getattribute
    cdef readonly int called_getattr
    cdef readonly int foo
    def __init__(self):
        self.foo = 10

    def __getattribute__(self,n):
        self.called_getattribute += 1
        if n == 'foo':
            return self.foo
        elif n == 'called_getattribute':
            return self.called_getattribute
        elif n == 'called_getattr':
            return self.called_getattr
        else:
            raise AttributeError

    def __getattr__(self,n):
        self.called_getattr += 1
        if n == 'bar':
            return n
        else:
            raise AttributeError
