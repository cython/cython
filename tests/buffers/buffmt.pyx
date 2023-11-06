from __future__ import unicode_literals
import struct

# Tests buffer format string parsing.


from libc cimport stdlib

def little_endian():
    cdef unsigned int n = 1
    return (<unsigned char*>&n)[0] != 0

if little_endian():
    current_endian = '<'
    other_endian = '>'
else:
    current_endian = '>'
    other_endian = '<'

cdef struct align_of_float_helper:
    char ch
    float d
cdef struct align_of_int_helper:
    char ch
    int i
float_align = sizeof(align_of_float_helper) - sizeof(float)
int_align = sizeof(align_of_int_helper) - sizeof(int)
if float_align != 4 or sizeof(float) != 4:
    raise RuntimeError("Alignment or size of float is %d on this system, please report to cython-dev for a testcase fix" % float_align)
if int_align != 4 or sizeof(int) != 4:
    raise RuntimeError("Alignment or size of int is %d on this system, please report to cython-dev for a testcase fix" % int_align)


cdef class MockBuffer:
    cdef Py_ssize_t zero
    cdef Py_ssize_t minusone
    cdef bytes format
    cdef object itemsize

    def __init__(self, format, itemsize):
        self.format = unicode(format).encode(u"ASCII")
        self.itemsize = itemsize
        self.zero = 0
        self.minusone = -1

    def __getbuffer__(self, Py_buffer* info, int flags):
        info.buf = NULL
        info.strides = &self.zero
        info.suboffsets = &self.minusone
        info.shape = &self.zero
        info.ndim = 1
        info.format = self.format
        info.itemsize = self.itemsize

def _int(fmt):
    """
    >>> _int("i")

    >>> _int("b")
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'int' but got 'signed char'

    >>> _int("if")
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected end but got 'float'

    >>> _int("$$")
    Traceback (most recent call last):
       ...
    ValueError: Does not understand character buffer dtype format string ('$')
    """
    cdef object[int] buf = MockBuffer(fmt, sizeof(int))

def _ulong(fmt):
    """
    >>> _ulong("L")
    """
    cdef object[unsigned long] buf = MockBuffer(fmt, sizeof(unsigned long))

def wrongsize():
    """
    >>> wrongsize()
    Traceback (most recent call last):
       ...
    ValueError: Item size of buffer (1 byte) does not match size of 'float' (4 bytes)

    """
    cdef object[float] buf = MockBuffer("f", 1)

def _obj(fmt):
    """
    >>> _obj("O")
    >>> _obj("i")
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'Python object' but got 'int'
    """
    cdef object[object] buf = MockBuffer(fmt, sizeof(void*))


cdef struct ComplexFloat:
    float real
    float imag

ctypedef struct Char3Int:
    char a
    int b
    int c
    int d

ctypedef struct LongString:
    char[90198] c

cdef struct CharIntCFloat:
    char a
    int b
    ComplexFloat c
    float d

cdef struct UnpackedStruct1:
    char a
    int b
    ComplexFloat c
    float c2
    Char3Int d

ctypedef struct UnpackedStruct2:
    CharIntCFloat a
    Char3Int b

ctypedef struct UnpackedStruct3:
    CharIntCFloat a
    char b
    int c, d, e

cdef struct UnpackedStruct4:
    char a
    int b
    ComplexFloat c
    float c2
    char d
    int e, f, g

def char3int(fmt):
    """
    >>> char3int("ciii")
    >>> char3int("c1i1i1i")
    >>> char3int("c3i")
    >>> char3int("ci2i")

    >>> char3int("c@i@2i")

    Extra pad bytes (assuming int size is 4 or more)
    >>> char3int("cxiii")
    >>> char3int("c3xiii")
    >>> char3int("cxxxiii")

    Standard alignment (assuming int size is 4)
    >>> char3int("=c3xiii")
    >>> char3int("=ciii")
    Traceback (most recent call last):
        ...
    ValueError: Buffer dtype mismatch; next field is at offset 1 but 4 expected

    >>> char3int("=cxxx@iii")

    Error:
    >>> char3int("cii")
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'int' but got end in 'Char3Int.d'
    """
    cdef object obj = MockBuffer(fmt, sizeof(Char3Int))
    cdef object[Char3Int, ndim=1] buf = obj


def long_string(fmt):
    """
    >>> long_string("90198s")
    """
    cdef object obj = MockBuffer(fmt, sizeof(LongString))
    cdef object[LongString, ndim=1] buf = obj


def unpacked_struct(fmt):
    """
    Native formats:
    >>> unpacked_struct("ciZffciii")
    >>> unpacked_struct("@ci3fc3i")
    >>> unpacked_struct("@ciZffci2i")
    >>> unpacked_struct("ciZffT{ciii}")
    >>> unpacked_struct("cT{ifffc2i}i")
    >>> unpacked_struct("ciZffc3T{i}")
    >>> unpacked_struct("T{c}T{T{iZffT{ci}}}2T{T{i}}")
    """

    assert (sizeof(UnpackedStruct1) == sizeof(UnpackedStruct2)
            == sizeof(UnpackedStruct3) == sizeof(UnpackedStruct4))
    cdef object obj = MockBuffer(fmt, sizeof(UnpackedStruct1))
    cdef object[UnpackedStruct1, ndim=1] buf1 = obj
    cdef object[UnpackedStruct2, ndim=1] buf2 = obj
    cdef object[UnpackedStruct3, ndim=1] buf3 = obj
    cdef object[UnpackedStruct4, ndim=1] buf4 = obj

cdef struct ComplexTest:
    ComplexFloat a, b, c

def complex_test(fmt):
    """
    >>> complex_test("ZfZfZf")
    >>> complex_test("3Zf")
    >>> complex_test("6f")
    >>> complex_test("3T{Zf}")

    >>> complex_test("fZfZff")
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'float' but got 'complex float' in 'ComplexFloat.imag'

    """
    cdef object obj = MockBuffer(fmt, sizeof(ComplexTest))
    cdef object[ComplexTest] buf1 = obj


def alignment_string(fmt, exc=None):
    """
    >>> alignment_string("@i")
    >>> alignment_string("%si" % current_endian)
    >>> alignment_string("%si" % other_endian, "X-endian buffer not supported on X-endian compiler")
    >>> alignment_string("=i")
    """
    cdef object[int] buf
    try:
        buf = MockBuffer(fmt, sizeof(int))
    except ValueError, e:
        msg = unicode(e).replace("Big", "X").replace("Little", "X").replace("big", "X").replace("little", "X")
        if msg != exc:
            print msg
            print "  is not equal to"
            print exc
        return
    if exc:
        print "fail"


def int_and_long_are_same():
    """
    >>> int_and_long_are_same()
    """
    cdef object[int] intarr
    cdef object[long] longarr
    if sizeof(int) == sizeof(long):
        intarr = MockBuffer("l", sizeof(int))
        longarr = MockBuffer("i", sizeof(int))

cdef struct MixedComplex:
    double real
    float imag

def mixed_complex_struct():
    """
    Triggering a specific execution path for this case.

    >>> mixed_complex_struct()
    Traceback (most recent call last):
        ...
    ValueError: Buffer dtype mismatch, expected 'double' but got 'complex double' in 'MixedComplex.real'
    """
    cdef object[MixedComplex] buf = MockBuffer("Zd",
        sizeof(MixedComplex))


cdef packed struct PackedSubStruct:
    char x
    int y

cdef struct UnpackedSubStruct:
    char x
    int y

cdef packed struct PackedStruct:
    char a
    int b
    PackedSubStruct sub

cdef struct PartiallyPackedStruct:
    char a
    int b
    PackedSubStruct sub

cdef packed struct PartiallyPackedStruct2:
    char a
    UnpackedSubStruct sub
    char b
    int c

def packed_struct(fmt):
    """
    Assuming int is four bytes:

    >>> packed_struct("^cici")
    >>> packed_struct("=cici")

    However aligned access won't work:

    >>> packed_struct("^c@i^ci")
    Traceback (most recent call last):
        ...
    ValueError: Buffer dtype mismatch; next field is at offset 4 but 1 expected

    >>> packed_struct("@cici")
    Traceback (most recent call last):
        ...
    ValueError: Buffer dtype mismatch; next field is at offset 4 but 1 expected

    """
    cdef object[PackedStruct] buf = MockBuffer(fmt, sizeof(PackedStruct))

def partially_packed_struct(fmt):
    """
    Assuming int is four bytes:

    >>> partially_packed_struct("^c@i^ci")
    >>> partially_packed_struct("@ci^ci")
    >>> partially_packed_struct("^c@i=ci")
    >>> partially_packed_struct("@ci=ci")
    >>> partially_packed_struct("ci^ci")
    >>> partially_packed_struct("ci=ci")

    Incorrectly aligned accesses won't work:

    >>> partially_packed_struct("^cici")
    Traceback (most recent call last):
        ...
    ValueError: Buffer dtype mismatch; next field is at offset 1 but 4 expected

    >>> partially_packed_struct("=cibi")
    Traceback (most recent call last):
        ...
    ValueError: Buffer dtype mismatch; next field is at offset 1 but 4 expected

    """
    cdef object[PartiallyPackedStruct] buf = MockBuffer(
        fmt, sizeof(PartiallyPackedStruct))

def partially_packed_struct_2(fmt):
    """
    Assuming int is four bytes:

    >>> partially_packed_struct_2("^ccxxxici")
    >>> partially_packed_struct_2("^ccxxxi^ci")
    >>> partially_packed_struct_2("c=cxxxi^ci")
    >>> partially_packed_struct_2("c^cxxxi^ci")
    >>> partially_packed_struct_2("c^cxxxi=ci")
    >>> partially_packed_struct_2("ccxxx^i@c^i")

    Incorrectly aligned accesses won't work:

    >>> partially_packed_struct_2("ccxxxici")
    Traceback (most recent call last):
        ...
    ValueError: Buffer dtype mismatch; next field is at offset 8 but 5 expected

    >>> partially_packed_struct_2("ccici")
    Traceback (most recent call last):
        ...
    ValueError: Buffer dtype mismatch; next field is at offset 4 but 5 expected

    """
    cdef object[PartiallyPackedStruct2] buf = MockBuffer(
        fmt, sizeof(PartiallyPackedStruct2))


cdef packed struct PackedStructWithCharArrays:
    float a
    int b
    char[5] c
    char[3] d


def packed_struct_with_strings(fmt):
    """
    >>> packed_struct_with_strings("T{f:a:i:b:5s:c:3s:d:}")
    """
    cdef object[PackedStructWithCharArrays] buf = MockBuffer(
        fmt, sizeof(PackedStructWithCharArrays))


ctypedef struct PackedStructWithArrays:
    double a[16]
    double b[16]
    double c

ctypedef struct UnpackedStructWithArrays:
    int a
    float b[8]
    float c
    unsigned long long d
    int e[5]
    int f
    int g
    double h[4]
    int i

ctypedef struct PackedStructWithNDArrays:
    double a
    double b[2][2]
    float c
    float d


def packed_struct_with_arrays(fmt):
    """
    >>> packed_struct_with_arrays("T{(16)d:a:(16)d:b:d:c:}")
    """

    cdef object[PackedStructWithArrays] buf = MockBuffer(
        fmt, sizeof(PackedStructWithArrays))


def unpacked_struct_with_arrays(fmt):
    """
    >>> if struct.calcsize('P') == 8:  # 64 bit
    ...     unpacked_struct_with_arrays("T{i:a:(8)f:b:f:c:Q:d:(5)i:e:i:f:i:g:xxxx(4)d:h:i:i:}")
    ... elif struct.calcsize('P') == 4:  # 32 bit
    ...     unpacked_struct_with_arrays("T{i:a:(8)f:b:f:c:Q:d:(5)i:e:i:f:i:g:(4)d:h:i:i:}")
    """

    cdef object[UnpackedStructWithArrays] buf = MockBuffer(
        fmt, sizeof(UnpackedStructWithArrays))


def packed_struct_with_ndarrays(fmt):
    """
    >>> packed_struct_with_ndarrays("T{d:a:(2,2)d:b:f:c:f:d:}")
    """

    cdef object[PackedStructWithNDArrays] buf = MockBuffer(
        fmt, sizeof(PackedStructWithNDArrays))


# TODO: empty struct
# TODO: Incomplete structs
# TODO: mixed structs
