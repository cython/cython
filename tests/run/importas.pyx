__doc__ = u"""
>>> import sys as sous
>>> import distutils.core as corey
>>> from copy import deepcopy as copey

>>> sous is _sous
True
>>> corey is _corey
True
>>> copey is _copey
True

>>> _sous is not None
True
>>> _corey is not None
True
>>> _copey is not None
True

>>> print(_sous.__name__)
sys
>>> print(sous.__name__)
sys
>>> print(_corey.__name__)
distutils.core
>>> print(corey.__name__)
distutils.core
>>> print(_copey.__name__)
deepcopy
>>> print(copey.__name__)
deepcopy
"""

import sys as _sous
import distutils.core as _corey
from copy import deepcopy as _copey
