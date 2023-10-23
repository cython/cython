cdef extern from "<bit>" namespace "std" nogil:
    # bit_cast (gcc >= 11.0, clang >= 14.0)
    fn To bit_cast[To, From](From&)

    # byteswap (C++23)
    #cdef T byteswap[T](T)

    # integral powers of 2 (gcc >= 10.0, clang >= 12.0)
    fn bint has_single_bit[T](T)
    fn T bit_ceil[T](T)
    fn T bit_floor[T](T)
    fn int bit_width[T](T)

    # rotating (gcc >= 9.0, clang >= 9.0)
    fn T rotl[T](T, int shift)
    fn T rotr[T](T, int shift)

    # counting (gcc >= 9.0, clang >= 9.0)
    fn int countl_zero[T](T)
    fn int countl_one[T](T)
    fn int countr_zero[T](T)
    fn int countr_one[T](T)
    fn int popcount[T](T)

    # endian
    cpdef enum class endian(int):
        little,
        big,
        native
