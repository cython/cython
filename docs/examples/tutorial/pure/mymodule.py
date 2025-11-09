if not cython.compiled:
    
    from math import sin

# calls sin() from math.h when compiled with Cython and math.sin() in Python
print(sin(0))