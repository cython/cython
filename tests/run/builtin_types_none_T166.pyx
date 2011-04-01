# ticket: 166

__doc__ = u"""
>>> l = None
>>> l.append(2)
Traceback (most recent call last):
AttributeError: 'NoneType' object has no attribute 'append'

"""

def append_to_none():
    """
    >>> append_to_none()
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'append'
    """
    cdef list l = None
    l.append(2)
