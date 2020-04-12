# mode: compile

# libc sin, cos and sqrt cimported in the pxd file

import cython

if not cython.compiled:
    from math import sin

if cython.compiled:
    pass
else:
    from math import cos

if "aa" == "bb":
    pass
elif cython.compiled:
    pass
elif True:
    from math import sqrt

if "aa" == "bb":
    pass
elif cython.compiled:
    pass
else:
    from math import tan
