cdef extern from *:
    """
    /* This is C code which will be put
     * in the .c file output by Cython */
    static long square(long x) {return x * x;}
    #define assign(x, y) ((x) = (y))
    """
    long square(long x)
    void assign(long& x, long y)
