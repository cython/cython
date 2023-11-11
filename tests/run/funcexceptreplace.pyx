__doc__ = u"""
>>> try: exc()
... except IndexError:
...     print(isinstance(sys.exc_info()[1].__context__, ValueError))
True
"""

import sys


def exc():
    try:
        raise ValueError
    except ValueError:
        raise IndexError
