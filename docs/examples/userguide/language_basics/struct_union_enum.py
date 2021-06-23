import cython

Grail = cython.struct(age=cython.int, volume=cython.float)
Food = cython.struct(spam=cython.p_char, eggs=cython.p_float)

# Enum is not supported by pure python mode
