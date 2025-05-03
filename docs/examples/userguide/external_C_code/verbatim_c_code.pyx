cdef extern from *:
    """
    /* This is C code which will be put
     * in the .c file output by Cython */
    static long c_square(long x) {return x * x;}
    #define c_assign(x, y) ((x) = (y))
    """
    long c_square(long x)
    void c_assign(long& x, long y)
