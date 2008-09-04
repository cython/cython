__doc__ = u"""
>>> a
2
"""

a = 0

try:
    raise KeyError
except AttributeError:
    a = 1
except KeyError:
    a = 2
except:
    a = 3
