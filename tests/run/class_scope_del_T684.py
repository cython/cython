# mode:run
# tag: class, scope, del
# ticket: t684

class DelInClass(object):
    """
    >>> DelInClass.y
    5
    >>> DelInClass.x
    Traceback (most recent call last):
    AttributeError: type object 'DelInClass' has no attribute 'x'
    """
    x = 5
    y = x
    del x
