# Tests buffer format string parsing.

__test__ = {}
def testcase(func):
    __test__[func.__name__] = func.__doc__
    return func

cimport stdlib

def little_endian():
    cdef unsigned int n = 1
    return (<unsigned char*>&n)[0] != 0

if little_endian():
    current_endian = '<'
    other_endian = '>'
else:
    current_endian = '>'
    other_endian = '<'

cdef struct align_of_double_helper:
    char ch
    double d    
cdef struct align_of_int_helper:
    char ch
    int i
double_align = sizeof(align_of_double_helper) - sizeof(double)
int_align = sizeof(align_of_int_helper) - sizeof(int)
if double_align != 8:
    raise RuntimeError("Alignment of double is %d on this system, please report to cython-dev for a testcase fix" % double_align)
if int_align != 4:
    raise RuntimeError("Alignment of int is %d on this system, please report to cython-dev for a testcase fix" % int_align)

 
cdef class MockBuffer:
    cdef Py_ssize_t zero
    cdef Py_ssize_t minusone
    cdef object format
    cdef object itemsize
    
    def __init__(self, format, itemsize):
        self.format = format
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

@testcase
def _int(fmt):
    """
    >>> _int("i")

    >>> _int("b")
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'int' but got 'char'
    
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

@testcase
def _ulong(fmt):
    """
    >>> _ulong("L")
    """
    cdef object[unsigned long] buf = MockBuffer(fmt, sizeof(unsigned long))

@testcase
def wrongsize():
    """
    >>> wrongsize()
    Traceback (most recent call last):
       ...
    ValueError: Item size of buffer (1 byte) does not match size of 'unsigned long' (8 bytes)

    """    
    cdef object[unsigned long] buf = MockBuffer("L", 1)

@testcase
def _obj(fmt):
    """
    >>> _obj("O")
    >>> _obj("i")
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'Python object' but got 'int'
    """
    cdef object[object] buf = MockBuffer(fmt, sizeof(void*))


cdef struct ComplexDouble:
    double real
    double imag

ctypedef struct Char3Int:
    char a
    int b
    int c
    int d

cdef struct CharIntCDouble:
    char a
    int b
    ComplexDouble c
    double d

cdef struct UnpackedStruct1:
    char a
    int b
    ComplexDouble c
    double c2
    Char3Int d

ctypedef struct UnpackedStruct2:
    CharIntCDouble a
    Char3Int b

ctypedef struct UnpackedStruct3:
    CharIntCDouble a
    char b
    int c, d, e

cdef struct UnpackedStruct4:
    char a
    int b
    ComplexDouble c
    double c2
    char d
    int e, f, g

@testcase
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

    Standard alignment (assming int size is 4)
    >>> char3int("=c3xiii")
    >>> char3int("=cxxx@iii")
    >>> char3int("=ciii")
    Traceback (most recent call last):
        ...
    ValueError: Buffer dtype mismatch; next field is at offset 1 but 4 expected
    
    Error:
    >>> char3int("cii")
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'int' but got end in 'Char3Int.d'
    """
    obj = MockBuffer(fmt, sizeof(Char3Int))
    cdef object[Char3Int, ndim=1] buf = obj

#@testcase
def unpacked_struct(fmt):
    """
    Native formats:
    >>> unpacked_struct("biZddbiii")
    >>> unpacked_struct("@bi3db3i")
    >>> unpacked_struct("@biZddbi2i")
    >>> unpacked_struct("bidT{biii}")
    >>> unpacked_struct("bT{idddb2i}i")
    >>> unpacked_struct("bidb3T{i}")
    >>> unpacked_struct("T{b}T{T{iZddT{bi}}}2T{T{i}}")
    """

    assert (sizeof(UnpackedStruct1) == sizeof(UnpackedStruct2)
            == sizeof(UnpackedStruct3) == sizeof(UnpackedStruct4))
    obj = MockBuffer(fmt, sizeof(UnpackedStruct1))
    cdef object[UnpackedStruct1, ndim=1] buf1 = obj
    cdef object[UnpackedStruct2, ndim=1] buf2 = obj
    cdef object[UnpackedStruct3, ndim=1] buf3 = obj
    cdef object[UnpackedStruct4, ndim=1] buf4 = obj

cdef struct ComplexTest:
    ComplexDouble a, b, c

@testcase
def complex_test(fmt):
    """
    >>> complex_test("ZdZdZd")
    >>> complex_test("3Zd")
    >>> complex_test("6d")
    >>> complex_test("3T{Zd}")
    
    >>> complex_test("dZdZdd")
    Traceback (most recent call last):
       ...
    ValueError: Buffer dtype mismatch, expected 'double' but got 'complex double' in 'ComplexDouble.imag'
    
    """
    obj = MockBuffer(fmt, sizeof(ComplexTest))
    cdef object[ComplexTest] buf1 = obj
    

@testcase
def alignment_string(fmt, exc=None):
    """
    >>> alignment_string("@i")
    >>> alignment_string("@i@@")
    >>> alignment_string("%si" % current_endian)
    >>> alignment_string("%si" % other_endian, "X-endian buffer not supported on X-endian compiler")
    >>> alignment_string("=i")
    """
    cdef object[int] buf
    try:
        buf = MockBuffer(fmt, sizeof(int))
    except ValueError, e:
        msg = e.message.replace("Big", "X").replace("Little", "X").replace("big", "X").replace("little", "X")
        if msg != exc:
            print msg
            print "  is not equal to"
            print exc
        return
    if exc:
        print "fail"


@testcase
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
    long double real
    float imag

@testcase
def mixed_complex_struct():
    """
    Triggering a specific execution path for this case.
 
    >>> mixed_complex_struct()
    Traceback (most recent call last):
        ...
    ValueError: Buffer dtype mismatch, expected 'long double' but got 'complex double' in 'MixedComplex.real'
    """
    cdef object[MixedComplex] buf = MockBuffer("Zd", sizeof(MixedComplex))

 
# TODO: empty struct
# TODO: Incomplete structs
