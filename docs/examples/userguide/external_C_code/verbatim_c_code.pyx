extern from *:
    """
    /* This is C code which will be put
     * in the .c file output by Cython */
    static long square(long x) {return x * x;}
    #define assign(x, y) ((x) = (y))
    """
    fn i64 square(i64 x)

    fn void assign(i64& x, i64 y)
