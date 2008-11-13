__doc__ = u"""
>>> import sys as sous
>>> import distutils.core as corey
>>> from copy import copy as copey

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
"""

import sys as _sous
import distutils.core as _corey
from copy import copy as _copey
