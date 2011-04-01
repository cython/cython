# ticket: 228

__doc__ = u"""
>>> def py_iterator():
...    if True: return
...    yield None

>>> list(py_iterator())
[]
>>> list(cy_iterator())
[]

>>> try:
...     raise ValueError
... except:
...     print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
...     a = list(py_iterator())
...     print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
True
True

>>> print(sys.exc_info()[0] is None or sys.exc_info()[0])
True

>>> try:
...     raise ValueError
... except:
...     print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
...     a = list(py_iterator())
...     print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
...     a = list(cy_iterator())
...     print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
True
True
True

>>> print(sys.exc_info()[0] is None or sys.exc_info()[0])
True

>>> double_raise(py_iterator)
True
True
True

>>> print(sys.exc_info()[0] is None or sys.exc_info()[0])
True
"""

import sys
if sys.version_info[0] < 3:
    sys.exc_clear()

cdef class cy_iterator(object):
    def __iter__(self):
        return self
    def __next__(self):
        raise StopIteration

def double_raise(py_iterator):
    try:
        raise ValueError
    except:
        print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
        a = list(py_iterator())
        print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
        a = list(cy_iterator())
        print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
