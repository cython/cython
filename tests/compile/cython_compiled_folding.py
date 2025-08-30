# mode: compile

# libc sin, cos and sqrt cimported in the pxd file

import cython
from cython import compiled

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
elif compiled:
    pass
else:
    from math import tan

# log10 isn't defined in the pxd file
from math import log10

@cython.test_fail_if_path_exists("//FromImportStatNode//ImportNode")
@cython.test_assert_path_exists("//AddNode")
def import_log(x, y):
    if compiled:
        return x+y
    else:
        from math import log
