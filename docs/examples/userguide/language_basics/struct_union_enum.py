Grail = cython.struct(
    age=cython.int,
    volume=cython.float)

Food = cython.union(
    spam=cython.p_char,
    eggs=cython.p_float)
