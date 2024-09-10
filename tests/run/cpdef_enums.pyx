"""
>>> import sys

>>> ANON_A, ANON_B, ANON_X
(2, 3, 5)

>>> ONE, TEN, HUNDRED
(1, 10, 100)
>>> THOUSAND        # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'THOUSAND' is not defined

>>> PyxEnum.TWO == 2 or PyxEnum.TWO
True
>>> PyxEnum.THREE == 3 or PyxEnum.THREE
True
>>> PyxEnum.FIVE == 5 or PyxEnum.FIVE
True
>>> cpdefPyxDocEnum.ELEVEN == 11 or cpdefPyxDocEnum.ELEVEN
True

>>> SEVEN           # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'SEVEN' is not defined
>>> SecretPyxEnum   # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'SecretPyxEnum' is not defined
>>> PxdSecretEnum   # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'PxdSecretEnum' is not defined
>>> cdefPxdDocEnum   # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'cdefPxdDocEnum' is not defined

>>> FOUR == 4 or FOUR
True
>>> EIGHT == 8 or EIGHT
True
>>> SIXTEEN        # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'SIXTEEN' is not defined

>>> RANK_0         # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'RANK_0' is not defined

>>> PxdEnum.RANK_0 == 11 or PxdEnum.RANK_0
True
>>> PxdEnum.RANK_1 == 37 or PxdEnum.RANK_1
True
>>> PxdEnum.RANK_2 == 389 or PxdEnum.RANK_2
True
>>> cpdefPxdDocEnum.RANK_6 == 159 or cpdefPxdDocEnum.RANK_6
True
>>> cpdefPxdDocLineEnum.RANK_7 == 889 or cpdefPxdDocLineEnum.RANK_7
True
>>> PxdEnum.RANK_3         # doctest: +ELLIPSIS
Traceback (most recent call last):
AttributeError: ...RANK_3...

>>> set(PyxEnum) == {PyxEnum.TWO, PyxEnum.THREE, PyxEnum.FIVE}
True
>>> str(PyxEnum.TWO).split(".")[-1]  if sys.version_info < (3,11) else  "TWO" # Py3.10/11 changed the output here
'TWO'
>>> str(PyxEnum.TWO)  if sys.version_info >= (3,11) else  "2" # Py3.10/11 changed the output here
'2'
>>> PyxEnum.TWO + PyxEnum.THREE == PyxEnum.FIVE
True
>>> PyxEnum(2) is PyxEnum["TWO"] is PyxEnum.TWO
True

# not leaking into module namespace
>>> IntEnum        # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'IntEnum' is not defined
"""

cdef extern from *:
    cpdef enum: # ExternPyx
        ONE "1"
        TEN "10"
        HUNDRED "100"

    cdef enum: # ExternSecretPyx
        THOUSAND "1000"

cpdef enum:
    # Anonymous enum values should appear in the module namespace.
    ANON_A = 2
    ANON_B = 3
    ANON_X = 5

cpdef enum PyxEnum:
    TWO = 2
    THREE = 3
    FIVE = 5

cpdef enum cpdefPyxDocEnum:
    """Home is where...
    """
    ELEVEN = 11

cpdef enum cpdefPyxDocLineEnum:
    """Home is where..."""
    FOURTEEN = 14

cdef enum SecretPyxEnum:
    SEVEN = 7

cdef enum cdefPyxDocEnum:
    """the heart is.
    """
    FIVE_AND_SEVEN = 5077

cdef extern from *:
    """
    enum ExternHasDuplicates {
        EX_DUP_A,
        EX_DUP_B=EX_DUP_A,
        EX_DUP_C=EX_DUP_A
    };
    """
    # Cython doesn't know about the duplicates though
    cpdef enum ExternHasDuplicates:
        EX_DUP_A
        EX_DUP_B
        EX_DUP_C


cpdef enum CyDefinedHasDuplicates1:
    CY_DUP1_A
    CY_DUP1_B = 0x00000000


cpdef enum CyDefinedHasDuplicates2:
    CY_DUP2_A
    CY_DUP2_B = CY_DUP2_A

cpdef enum CyDefinedHasDuplicates3:
    CY_DUP3_A = 1
    CY_DUP3_B = 0
    CY_DUP3_C  # = 1


def test_as_variable_from_cython():
    """
    >>> test_as_variable_from_cython()
    """
    assert list(PyxEnum) == [TWO, THREE, FIVE], list(PyxEnum)
    assert list(PxdEnum) == [RANK_0, RANK_1, RANK_2], list(PxdEnum)

cdef int verify_pure_c() nogil:
    cdef int x = TWO
    cdef int y = PyxEnum.THREE
    cdef int z = SecretPyxEnum.SEVEN
    return x + y + z

# Use it to suppress warning.
verify_pure_c()

def verify_resolution_GH1533():
    """
    >>> verify_resolution_GH1533()
    3
    """
    THREE = 100
    return int(PyxEnum.THREE)


def check_docs():
    """
    >>> PxdEnum.__doc__ not in ("Home is where...\\n    ", "Home is where...")
    True
    >>> PyxEnum.__doc__ not in ("Home is where...\\n    ", "Home is where...")
    True
    >>> cpdefPyxDocEnum.__doc__ == "Home is where...\\n    "
    True
    >>> cpdefPxdDocEnum.__doc__ == "Home is where...\\n    "
    True
    >>> cpdefPyxDocLineEnum.__doc__
    'Home is where...'
    >>> cpdefPxdDocLineEnum.__doc__
    'Home is where...'
    """
    pass


def to_from_py_conversion(PxdEnum val):
    """
    >>> to_from_py_conversion(PxdEnum.RANK_1) is PxdEnum.RANK_1
    True

    C enums are commonly enough used as flags that it seems reasonable
    to allow it in Cython
    >>> to_from_py_conversion(PxdEnum.RANK_1 | PxdEnum.RANK_2) == (PxdEnum.RANK_1 | PxdEnum.RANK_2)
    True
    """
    return val


def to_from_py_conversion_with_duplicates1(ExternHasDuplicates val):
    """
    Mainly a compile-time test - we can't optimize to a switch here
    >>> to_from_py_conversion_with_duplicates1(ExternHasDuplicates.EX_DUP_A) == ExternHasDuplicates.EX_DUP_A
    True
    """
    return val


def to_from_py_conversion_with_duplicates2(CyDefinedHasDuplicates1 val):
    """
    Mainly a compile-time test - we can't optimize to a switch here
    >>> to_from_py_conversion_with_duplicates2(CyDefinedHasDuplicates1.CY_DUP1_A) == CyDefinedHasDuplicates1.CY_DUP1_A
    True
    """
    return val


def to_from_py_conversion_with_duplicates3(CyDefinedHasDuplicates2 val):
    """
    Mainly a compile-time test - we can't optimize to a switch here
    >>> to_from_py_conversion_with_duplicates3(CyDefinedHasDuplicates2.CY_DUP2_A) == CyDefinedHasDuplicates2.CY_DUP2_A
    True
    """
    return val


def to_from_py_conversion_with_duplicates4(CyDefinedHasDuplicates3 val):
    """
    Mainly a compile-time test - we can't optimize to a switch here
    >>> to_from_py_conversion_with_duplicates4(CyDefinedHasDuplicates3.CY_DUP3_C) == CyDefinedHasDuplicates3.CY_DUP3_C
    True
    """
    return val


def test_pickle():
    """
    >>> from pickle import loads, dumps
    >>> import sys

    Python 3.11.4 has a bug that breaks pickling: https://github.com/python/cpython/issues/105332

    >>> if sys.version_info[:3] == (3,11,4):
    ...     loads = dumps = lambda x: x

    >>> loads(dumps(PyxEnum.TWO)) == PyxEnum.TWO
    True
    >>> loads(dumps(PxdEnum.RANK_2)) == PxdEnum.RANK_2
    True
    """
    pass

def test_as_default_value(PxdEnum val=PxdEnum.RANK_1):
    """
    In order to work, this requires the utility code to be evaluated
    before the function definition
    >>> test_as_default_value()
    True
    >>> test_as_default_value(PxdEnum.RANK_2)
    False
    >>> test_as_default_value.__defaults__[0] == PxdEnum.RANK_1
    True
    """
    return val == PxdEnum.RANK_1
