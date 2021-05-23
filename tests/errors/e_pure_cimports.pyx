# mode: error
# tag: pure, import, cimport

import cython.cimportsy     # FIXME: not currently an error?

import cython.cimports
import cython.cimports.libc
import cython.cimports as cim

cimport cython.cimports
cimport cython.cimports.libc
cimport cython.cimports as cim

# ok
from cython.cimports import libc
from cython.cimports cimport libc


_ERRORS = """
6:7: Python cimports must use 'from cython.cimports... import ...', not just 'import ...'
7:7: Python cimports must use 'from cython.cimports... import ...', not just 'import ...'
8:7: Python cimports must use 'from cython.cimports... import ...', not just 'import ...'
10:8: Python cimports must use 'from cython.cimports... import ...', not just 'import ...'
11:8: Python cimports must use 'from cython.cimports... import ...', not just 'import ...'
12:8: Python cimports must use 'from cython.cimports... import ...', not just 'import ...'
"""
