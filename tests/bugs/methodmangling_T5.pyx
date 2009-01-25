# this is ticket #5

__doc__ = u"""
>>> class PyTest(object):
...     def __private(self): pass

>>> py = PyTest()
>>> '_PyTest__private' in dir(py)
True
>>> '__private' in dir(py)
False

>>> cy = CyTest()
>>> '_PyTest__private' in dir(cy)
True
>>> '__private' in dir(cy)
False
"""

class CyTest(object):
    def __private(self): pass
