
def f():
    """
    >>> f()
    >>> g
    42
    >>> x == 'spam'
    True
    >>> y == 'eggs'
    True
    >>> z == 'spameggs'
    True
    """
    pass

g = 42
x = u"spam"
y = u"eggs"
if g:
    z = x + y
