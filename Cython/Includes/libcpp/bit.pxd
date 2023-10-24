extern from "<bit>" namespace "std" nogil:
    # bit_cast (gcc >= 11.0, clang >= 14.0)
    fn To bit_cast[To, From](From&)

    # byteswap (C++23)
    #cdef T byteswap[T](T)

    # integral powers of 2 (gcc >= 10.0, clang >= 12.0)
    fn bint has_single_bit[T](T)
    fn T bit_ceil[T](T)
    fn T bit_floor[T](T)
    fn i32 bit_width[T](T)

    # rotating (gcc >= 9.0, clang >= 9.0)
    fn T rotl[T](T, i32 shift)
    fn T rotr[T](T, i32 shift)

    # counting (gcc >= 9.0, clang >= 9.0)
    fn i32 countl_zero[T](T)
    fn i32 countl_one[T](T)
    fn i32 countr_zero[T](T)
    fn i32 countr_one[T](T)
    fn i32 popcount[T](T)

    # endian
    cpdef enum class endian(i32):
        little,
        big,
        native
