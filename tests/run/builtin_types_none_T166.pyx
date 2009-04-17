__doc__ = u"""
>>> l = None
>>> l.append(2)
Traceback (most recent call last):
AttributeError: 'NoneType' object has no attribute 'append'

>>> append_to_none()
Traceback (most recent call last):
AttributeError: 'NoneType' object has no attribute 'append'
"""

def append_to_none():
    cdef list l = None
    l.append(2)
