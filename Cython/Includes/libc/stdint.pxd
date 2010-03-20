# 7.18 Integer types <stdint.h>
cdef extern from "stdint.h" nogil:

    # 7.18.1 Integer types
    # 7.18.1.1 Exact-width integer types
    ctypedef   signed int  int8_t
    ctypedef   signed int  int16_t
    ctypedef   signed int  int32_t
    ctypedef   signed int  int64_t
    ctypedef unsigned int uint8_t
    ctypedef unsigned int uint16_t
    ctypedef unsigned int uint32_t
    ctypedef unsigned int uint64_t
    # 7.18.1.2 Minimum-width integer types
    ctypedef   signed int  int_least8_t
    ctypedef   signed int  int_least16_t
    ctypedef   signed int  int_least32_t
    ctypedef   signed int  int_least64_t
    ctypedef unsigned int uint_least8_t
    ctypedef unsigned int uint_least16_t
    ctypedef unsigned int uint_least32_t
    ctypedef unsigned int uint_least64_t
    # 7.18.1.3 Fastest minimum-width integer types
    ctypedef   signed int  int_fast8_t
    ctypedef   signed int  int_fast16_t
    ctypedef   signed int  int_fast32_t
    ctypedef   signed int  int_fast64_t
    ctypedef unsigned int uint_fast8_t
    ctypedef unsigned int uint_fast16_t
    ctypedef unsigned int uint_fast32_t
    ctypedef unsigned int uint_fast64_t
    # 7.18.1.4 Integer types capable of holding object pointers
    ctypedef   signed int  intptr_t
    ctypedef unsigned int uintptr_t
    # 7.18.1.5 Greatest-width integer types
    ctypedef signed   int intmax_t
    ctypedef unsigned int uintmax_t

    # 7.18.2 Limits of specified-width integer types
    # 7.18.2.1 Limits of exact-width integer types
    enum:   INT8_T_MIN
    enum:  INT16_T_MIN
    enum:  INT32_T_MIN
    enum:  INT64_T_MIN
    enum:   INT8_T_MAX
    enum:  INT16_T_MAX
    enum:  INT32_T_MAX
    enum:  INT64_T_MAX
    enum:  UINT8_T_MAX
    enum: UINT16_T_MAX
    enum: UINT32_T_MAX
    enum: UINT64_T_MAX
    #7.18.2.2 Limits of minimum-width integer types
    enum:   INT_LEAST8_T_MIN
    enum:  INT_LEAST16_T_MIN
    enum:  INT_LEAST32_T_MIN
    enum:  INT_LEAST64_T_MIN
    enum:   INT_LEAST8_T_MAX
    enum:  INT_LEAST16_T_MAX
    enum:  INT_LEAST32_T_MAX
    enum:  INT_LEAST64_T_MAX
    enum:  UINT_LEAST8_T_MAX
    enum: UINT_LEAST16_T_MAX
    enum: UINT_LEAST32_T_MAX
    enum: UINT_LEAST64_T_MAX
    #7.18.2.3 Limits of fastest minimum-width integer types
    enum:   INT_FAST8_T_MIN
    enum:  INT_FAST16_T_MIN
    enum:  INT_FAST32_T_MIN
    enum:  INT_FAST64_T_MIN
    enum:   INT_FAST8_T_MAX
    enum:  INT_FAST16_T_MAX
    enum:  INT_FAST32_T_MAX
    enum:  INT_FAST64_T_MAX
    enum:  UINT_FAST8_T_MAX
    enum: UINT_FAST16_T_MAX
    enum: UINT_FAST32_T_MAX
    enum: UINT_FAST64_T_MAX
    #7.18.2.4 Limits of integer types capable of holding object pointers
    enum:  INTPTR_MIN
    enum:  INTPTR_MAX
    enum: UINTPTR_MAX
    # 7.18.2.5 Limits of greatest-width integer types
    enum:  INTMAX_T_MAX
    enum:  INTMAX_T_MIN
    enum: UINTMAX_T_MAX

    # 7.18.3 Limits of other integer types
    # ptrdiff_t
    enum: PTRDIFF_MIN
    enum: PTRDIFF_MAX
    # sig_atomic_t
    enum: SIG_ATOMIC_MIN
    enum: SIG_ATOMIC_MAX
    # size_t
    enum: SIZE_MAX
    # wchar_t
    enum: WCHAR_MIN
    enum: WCHAR_MAX
    # wint_t
    enum: WINT_MIN
    enum: WINT_MAX
