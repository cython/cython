# mymodule.py

import cython

# override with Python import if not in compiled code
if not cython.compiled:
    from math import sin

# calls sin() from math.h when compiled with Cython and math.sin() in Python
print(sin(0))
