"""
>>> ONE, TEN, HUNDRED
(1, 10, 100)
>>> THOUSAND        # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'THOUSAND' is not defined

>>> TWO, THREE, FIVE
(2, 3, 5)
>>> SEVEN           # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'SEVEN' is not defined

>>> FOUR, EIGHT
(4, 8)
>>> SIXTEEN        # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'SIXTEEN' is not defined

>>> RANK_0, RANK_1, RANK_2
(11, 37, 389)
>>> RANK_3         # doctest: +ELLIPSIS
Traceback (most recent call last):
NameError: ...name 'RANK_3' is not defined
"""


cdef extern from *:
    cpdef enum ExternPyxEnum:
        ONE "1"
        TEN "10"
        HUNDRED "100"

    cdef enum ExternSecretPyxEnum:
        THOUSAND "1000"

cpdef enum PyxEnum:
    TWO = 2
    THREE = 3
    FIVE = 5

cdef enum SecretPyxEnum:
    SEVEN = 7
