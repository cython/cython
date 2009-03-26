__doc__ = u"""
>>> try: exc()
... except IndexError:
...     if IS_PY3:
...         print(isinstance(sys.exc_info()[1].__context__, ValueError))
...     else:
...         print(True)
True
"""

import sys
IS_PY3 = sys.version_info[0] >= 3

def exc():
    try:
        raise ValueError
    except ValueError:
        raise IndexError
