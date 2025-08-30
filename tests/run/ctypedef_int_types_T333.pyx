# ticket: t333
#cython: autotestdict=True

# -------------------------------------------------------------------

cdef extern from "ctypedef_int_types_chdr_T333.h":
     ctypedef int SChar     ## "signed char"
     ctypedef int UChar     ## "unsigned char"
     ctypedef int SShort    ## "signed short"
     ctypedef int UShort    ## "unsigned short"
     ctypedef int SInt      ## "signed int"
     ctypedef int UInt      ## "unsigned int"
     ctypedef int SLong     ## "signed long"
     ctypedef int ULong     ## "unsigned long"
     ctypedef int SLongLong ## "signed PY_LONG_LONG"
     ctypedef int ULongLong ## "unsigned PY_LONG_LONG"

# -------------------------------------------------------------------

SCHAR_MAX = <SChar>((<UChar>-1)>>1)
SCHAR_MIN = (-SCHAR_MAX-1)

def test_schar(SChar x):
   u"""
   >>> test_schar(-129) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: value too large to convert to SChar
   >>> test_schar(-128)
   -128
   >>> test_schar(0)
   0
   >>> test_schar(127)
   127
   >>> test_schar(128) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: value too large to convert to SChar
   """
   return x

def test_add_schar(x, y):
   u"""
   >>> test_add_schar(SCHAR_MIN, -1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: value too large to convert to SChar
   >>> test_add_schar(SCHAR_MIN, 0) == SCHAR_MIN
   True
   >>> test_add_schar(SCHAR_MIN, 1) == SCHAR_MIN+1
   True
   >>> test_add_schar(SCHAR_MAX, -1) == SCHAR_MAX-1
   True
   >>> test_add_schar(SCHAR_MAX, 0) == SCHAR_MAX
   True
   >>> test_add_schar(SCHAR_MAX, 1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: value too large to convert to SChar
   """
   cdef SChar r = x + y
   return r

UCHAR_MAX = <UChar>((<UChar>-1))

def test_uchar(UChar x):
   u"""
   >>> test_uchar(-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: can't convert negative value to UChar
   >>> test_uchar(0)
   0
   >>> test_uchar(1)
   1
   >>> test_uchar(UCHAR_MAX) == UCHAR_MAX
   True
   >>> test_uchar(UCHAR_MAX+1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: value too large to convert to UChar
   """
   return x

def test_add_uchar(x, y):
   u"""
   >>> test_add_uchar(UCHAR_MAX, 0) == UCHAR_MAX
   True
   >>> test_add_uchar(UCHAR_MAX, 1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: value too large to convert to UChar
   """
   cdef UChar r = x + y
   return r

# -------------------------------------------------------------------

SSHORT_MAX = <SShort>((<UShort>-1)>>1)
SSHORT_MIN = (-SSHORT_MAX-1)

def test_sshort(SShort x):
   u"""
   >>> test_sshort(SSHORT_MIN-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: value too large to convert to SShort
   >>> test_sshort(SSHORT_MIN) == SSHORT_MIN
   True
   >>> test_sshort(-1)
   -1
   >>> test_sshort(0)
   0
   >>> test_sshort(1)
   1
   >>> test_sshort(SSHORT_MAX) == SSHORT_MAX
   True
   >>> test_sshort(SSHORT_MAX+1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   """
   return x

def test_add_sshort(x, y):
   u"""
   >>> test_add_sshort(SSHORT_MIN, -1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: value too large to convert to SShort
   >>> test_add_sshort(SSHORT_MIN, 0) == SSHORT_MIN
   True
   >>> test_add_sshort(SSHORT_MIN, 1) == SSHORT_MIN+1
   True
   >>> test_add_sshort(SSHORT_MAX, -1) == SSHORT_MAX-1
   True
   >>> test_add_sshort(SSHORT_MAX, 0) == SSHORT_MAX
   True
   >>> test_add_sshort(SSHORT_MAX, 1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: value too large to convert to SShort
   """
   cdef SShort r = x + y
   return r

USHORT_MAX = <UShort>((<UShort>-1))

def test_ushort(UShort x):
   u"""
   >>> test_ushort(-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: can't convert negative value to UShort
   >>> test_ushort(0)
   0
   >>> test_ushort(1)
   1
   >>> test_ushort(USHORT_MAX) == USHORT_MAX
   True
   >>> test_ushort(USHORT_MAX+1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: value too large to convert to UShort
   """
   return x

def test_add_ushort(x, y):
   u"""
   >>> test_add_ushort(USHORT_MAX, 0) == USHORT_MAX
   True
   >>> test_add_ushort(USHORT_MAX, 1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: value too large to convert to UShort
   """
   cdef UShort r = x + y
   return r

# -------------------------------------------------------------------

SINT_MAX = <SInt>((<UInt>-1)>>1)
SINT_MIN = (-SINT_MAX-1)

def test_sint(SInt x):
   u"""
   >>> test_sint(SINT_MIN-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   >>> test_sint(SINT_MIN) == SINT_MIN
   True
   >>> test_sint(-1)
   -1
   >>> test_sint(0)
   0
   >>> test_sint(1)
   1
   >>> test_sint(SINT_MAX) == SINT_MAX
   True
   >>> test_sint(SINT_MAX+1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   """
   return x

def test_add_sint(x, y):
   u"""
   >>> test_add_sint(SINT_MIN, -1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   >>> test_add_sint(SINT_MIN, 0) == SINT_MIN
   True
   >>> test_add_sint(SINT_MIN, 1) == SINT_MIN+1
   True
   >>> test_add_sint(SINT_MAX, -1) == SINT_MAX-1
   True
   >>> test_add_sint(SINT_MAX, 0) == SINT_MAX
   True
   >>> test_add_sint(SINT_MAX, 1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   """
   cdef SInt r = x + y
   return r

UINT_MAX = <UInt>(<UInt>-1)

def test_uint(UInt x):
   u"""
   >>> test_uint(-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: can't convert negative value to UInt
   >>> print(test_uint(0))
   0
   >>> print(test_uint(1))
   1
   >>> test_uint(UINT_MAX) == UINT_MAX
   True
   >>> test_uint(UINT_MAX+1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   """
   return x

def test_add_uint(x, y):
   u"""
   >>> test_add_uint(UINT_MAX, 0) == UINT_MAX
   True
   >>> test_add_uint(UINT_MAX, 1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   """
   cdef UInt r = x + y
   return r

# -------------------------------------------------------------------

SLONG_MAX = <SLong>((<ULong>-1)>>1)
SLONG_MIN = (-SLONG_MAX-1)

def test_slong(long x):
   u"""
   >>> test_slong(SLONG_MIN-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   >>> test_slong(SLONG_MIN) == SLONG_MIN
   True
   >>> test_slong(-1)
   -1
   >>> test_slong(0)
   0
   >>> test_slong(1)
   1
   >>> test_slong(SLONG_MAX) == SLONG_MAX
   True
   >>> test_slong(SLONG_MAX+1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   """
   return x

def test_add_slong(x, y):
   u"""
   >>> test_add_slong(SLONG_MIN, -1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   >>> test_add_slong(SLONG_MIN, 0) == SLONG_MIN
   True
   >>> test_add_slong(SLONG_MIN, 1) == SLONG_MIN+1
   True
   >>> test_add_slong(SLONG_MAX, -1) == SLONG_MAX-1
   True
   >>> test_add_slong(SLONG_MAX, 0) == SLONG_MAX
   True
   >>> test_add_slong(SLONG_MAX, 1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   """
   cdef SLong r = x + y
   return r

ULONG_MAX = <ULong>(<ULong>-1)

def test_ulong(ULong x):
   u"""
   >>> test_ulong(-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: can't convert negative value to ULong
   >>> print(test_ulong(0))
   0
   >>> print(test_ulong(1))
   1
   >>> test_ulong(ULONG_MAX) == ULONG_MAX
   True
   >>> test_ulong(ULONG_MAX+1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   """
   return x

def test_add_ulong(x, y):
   u"""
   >>> test_add_ulong(ULONG_MAX, 0) == ULONG_MAX
   True
   >>> test_add_ulong(ULONG_MAX, 1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   """
   cdef ULong r = x + y
   return r

# -------------------------------------------------------------------

SLONGLONG_MAX = <SLongLong>((<ULongLong>-1)>>1)
SLONGLONG_MIN = (-SLONGLONG_MAX-1)

def test_slonglong(long long x):
   u"""
   >>> test_slonglong(SLONGLONG_MIN-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   >>> test_slonglong(SLONGLONG_MIN) == SLONGLONG_MIN
   True
   >>> print(test_slonglong(-1))
   -1
   >>> print(test_slonglong(0))
   0
   >>> print(test_slonglong(1))
   1
   >>> test_slonglong(SLONGLONG_MAX) == SLONGLONG_MAX
   True
   >>> test_slonglong(SLONGLONG_MAX+1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   """
   return x

def test_add_slonglong(x, y):
   u"""
   >>> test_add_slonglong(SLONGLONG_MIN, -1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   >>> test_add_slonglong(SLONGLONG_MIN, 0) == SLONGLONG_MIN
   True
   >>> test_add_slonglong(SLONGLONG_MIN, 1) == SLONGLONG_MIN+1
   True
   >>> test_add_slonglong(SLONGLONG_MAX, -1) == SLONGLONG_MAX-1
   True
   >>> test_add_slonglong(SLONGLONG_MAX, 0) == SLONGLONG_MAX
   True
   >>> test_add_slonglong(SLONGLONG_MAX, 1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   """
   cdef SLongLong r = x + y
   return r

ULONGLONG_MAX = <ULongLong>(<ULongLong>-1)

def test_ulonglong(ULongLong x):
   u"""
   >>> test_ulonglong(-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: can't convert negative value to ULongLong
   >>> print(test_ulonglong(0))
   0
   >>> print(test_ulonglong(1))
   1
   >>> test_ulonglong(ULONGLONG_MAX) == ULONGLONG_MAX
   True
   >>> test_ulonglong(ULONGLONG_MAX+1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   """
   return x

def test_add_ulonglong(x, y):
   u"""
   >>> test_add_ulonglong(ULONGLONG_MAX, 0) == ULONGLONG_MAX
   True
   >>> test_add_ulonglong(ULONGLONG_MAX, 1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   """
   cdef ULongLong r = x + y
   return r

# -------------------------------------------------------------------

cdef class MyClass:
    """
    >>> a = MyClass()

    >>> vals = (SCHAR_MIN,     UCHAR_MAX,
    ...         SSHORT_MIN,    USHORT_MAX,
    ...         SINT_MIN,      UINT_MAX,
    ...         SLONG_MIN,     ULONG_MAX,
    ...         SLONGLONG_MIN, ULONGLONG_MAX)
    >>> a.setvalues(*vals)
    >>> a.getvalues() == vals
    True

    >>> vals = (SCHAR_MAX,     UCHAR_MAX,
    ...         SSHORT_MAX,    USHORT_MAX,
    ...         SINT_MAX,      UINT_MAX,
    ...         SLONG_MAX,     ULONG_MAX,
    ...         SLONGLONG_MAX, ULONGLONG_MAX)
    >>> a.setvalues(*vals)
    >>> a.getvalues() == vals
    True

    >>> vals = (0,) * 10
    >>> a.setvalues(*vals)
    >>> a.getvalues() == vals
    True


    """
    cdef:
       SChar     attr_schar
       UChar     attr_uchar
       SShort    attr_sshort
       UShort    attr_ushort
       SInt      attr_sint
       UInt      attr_uint
       SLong     attr_slong
       ULong     attr_ulong
       SLongLong attr_slonglong
       ULongLong attr_ulonglong

    cpdef setvalues(self,
                    SChar     arg_schar     ,
                    UChar     arg_uchar     ,
                    SShort    arg_sshort    ,
                    UShort    arg_ushort    ,
                    SInt      arg_sint      ,
                    UInt      arg_uint      ,
                    SLong     arg_slong     ,
                    ULong     arg_ulong     ,
                    SLongLong arg_slonglong ,
                    ULongLong arg_ulonglong ):
        self.attr_schar     = arg_schar
        self.attr_uchar     = arg_uchar
        self.attr_sshort    = arg_sshort
        self.attr_ushort    = arg_ushort
        self.attr_sint      = arg_sint
        self.attr_uint      = arg_uint
        self.attr_slong     = arg_slong
        self.attr_ulong     = arg_ulong
        self.attr_slonglong = arg_slonglong
        self.attr_ulonglong = arg_ulonglong

    cpdef getvalues(self):
        return (self.attr_schar     ,
                self.attr_uchar     ,
                self.attr_sshort    ,
                self.attr_ushort    ,
                self.attr_sint      ,
                self.attr_uint      ,
                self.attr_slong     ,
                self.attr_ulong     ,
                self.attr_slonglong ,
                self.attr_ulonglong )


# -------------------------------------------------------------------

cdef extern from *:
    ctypedef signed   MySInt1 "signed short"
    ctypedef unsigned MyUInt1 "unsigned short"

def test_MySInt1(MySInt1 x):
   u"""
   >>> test_MySInt1(-1)
   -1
   >>> test_MySInt1(0)
   0
   >>> test_MySInt1(1)
   1
   """
   return x

def test_MyUInt1(MyUInt1 x):
   u"""
   >>> test_MyUInt1(-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: ...
   >>> test_MyUInt1(0)
   0
   >>> test_MyUInt1(1)
   1
   """
   return x

cdef extern from *:
    ctypedef signed   MySInt2 "signed short"
    ctypedef unsigned MyUInt2 "unsigned short"

def test_MySInt2(MySInt2 x):
   u"""
   >>> test_MySInt2(-1)
   -1
   >>> test_MySInt2(0)
   0
   >>> test_MySInt2(1)
   1
   """
   return x

def test_MyUInt2(MyUInt2 x):
   u"""
   >>> test_MyUInt2(-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: can't convert negative value to ...
   >>> test_MyUInt2(0)
   0
   >>> test_MyUInt2(1)
   1
   """
   return x

# -------------------------------------------------------------------

cimport ctypedef_int_types_defs_T333 as defs

def test_DefSInt(defs.SInt x):
   u"""
   >>> test_DefSInt(-1)
   -1
   >>> test_DefSInt(0)
   0
   >>> test_DefSInt(1)
   1
   """
   return x

def test_DefUChar(defs.UChar x):
   u"""
   >>> test_DefUChar(-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: can't convert negative value to ...
   >>> test_DefUChar(0)
   0
   >>> test_DefUChar(1)
   1
   """
   return x

def test_ExtSInt(defs.ExtSInt x):
   u"""
   >>> test_ExtSInt(-1)
   -1
   >>> test_ExtSInt(0)
   0
   >>> test_ExtSInt(1)
   1
   """
   return x

def test_ExtUInt(defs.ExtUInt x):
   u"""
   >>> test_ExtUInt(-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: can't convert negative value to ...
   >>> test_ExtUInt(0)
   0
   >>> test_ExtUInt(1)
   1
   """
   return x


ctypedef defs.SShort LocSInt
ctypedef defs.UShort LocUInt

def test_LocSInt(LocSInt x):
   u"""
   >>> test_LocSInt(-1)
   -1
   >>> test_LocSInt(0)
   0
   >>> test_LocSInt(1)
   1
   """
   return x

def test_LocUInt(LocUInt x):
   u"""
   >>> test_LocUInt(-1) #doctest: +ELLIPSIS
   Traceback (most recent call last):
       ...
   OverflowError: can't convert negative value to ...
   >>> test_LocUInt(0)
   0
   >>> test_LocUInt(1)
   1
   """
   return x

# -------------------------------------------------------------------
