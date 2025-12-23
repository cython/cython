# coding: utf-8

cdef extern from *:
    const Py_ssize_t PY_SSIZE_T_MIN
    const Py_ssize_t PY_SSIZE_T_MAX

SSIZE_T_MAX = PY_SSIZE_T_MAX
SSIZE_T_MIN = PY_SSIZE_T_MIN


def slice_start_end(unicode s, Py_ssize_t i, Py_ssize_t j):
    """
    >>> slice_start_end('abcdef', 2, 3)
    c
    >>> slice_start_end('abcdef', 2, 10)
    cdef
    >>> slice_start_end('abcdef', 0, 5)
    abcde
    >>> slice_start_end('abcdef', -6, -1)
    abcde
    >>> slice_start_end('abcdef', -6, -7)
    <BLANKLINE>
    >>> slice_start_end('abcdef', -7, -7)
    <BLANKLINE>
    >>> slice_start_end('aАbБcСdДeЕfФ', 2, 8)
    bБcСdД
    >>> slice_start_end('АБСДЕФ', 2, 4)
    СД
    >>> slice_start_end('АБСДЕФ', -4, -2)
    СД
    >>> slice_start_end(None, 2, 4)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> slice_start_end('abcdef', SSIZE_T_MAX, SSIZE_T_MIN)
    <BLANKLINE>
    """
    print(s[i:j])


def slice_start(unicode s, Py_ssize_t i, Py_ssize_t j):
    """
    >>> slice_start('abcdef', 2, 3)
    cdef
    >>> slice_start('abcdef', 2, 10)
    cdef
    >>> slice_start('abcdef', 0, 5)
    abcdef
    >>> slice_start('abcdef', -6, -1)
    abcdef
    >>> slice_start('abcdef', -6, -7)
    abcdef
    >>> slice_start('abcdef', -7, -7)
    abcdef
    >>> slice_start('aАbБcСdДeЕfФ', 2, 8)
    bБcСdДeЕfФ
    >>> slice_start('АБСДЕФ', 2, 4)
    СДЕФ
    >>> slice_start('АБСДЕФ', -4, -2)
    СДЕФ
    >>> slice_start(None, 2, 4)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> slice_start('abcdef', SSIZE_T_MAX, SSIZE_T_MIN)
    <BLANKLINE>
    """
    print(s[i:])


def slice_end(unicode s, Py_ssize_t i, Py_ssize_t j):
    """
    >>> slice_end('abcdef', 2, 3)
    ab
    >>> slice_end('abcdef', 2, 10)
    ab
    >>> slice_end('abcdef', 0, 5)
    <BLANKLINE>
    >>> slice_end('abcdef', -6, -1)
    <BLANKLINE>
    >>> slice_end('abcdef', -6, -7)
    <BLANKLINE>
    >>> slice_end('abcdef', -7, -7)
    <BLANKLINE>
    >>> slice_end('aАbБcСdДeЕfФ', 2, 8)
    aА
    >>> slice_end('АБСДЕФ', 2, 4)
    АБ
    >>> slice_end('АБСДЕФ', -4, -2)
    АБ
    >>> slice_end(None, 2, 4)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> slice_end('abcdef', SSIZE_T_MAX, SSIZE_T_MIN)
    abcdef
    """
    print(s[:i])


def slice_all(unicode s, Py_ssize_t i, Py_ssize_t j):
    """
    >>> slice_all('abcdef', 2, 3)
    abcdef
    >>> slice_all('abcdef', 2, 10)
    abcdef
    >>> slice_all('abcdef', 0, 5)
    abcdef
    >>> slice_all('abcdef', -6, -1)
    abcdef
    >>> slice_all('abcdef', -6, -7)
    abcdef
    >>> slice_all('abcdef', -7, -7)
    abcdef
    >>> slice_all('aАbБcСdДeЕfФ', 2, 8)
    aАbБcСdДeЕfФ
    >>> slice_all('АБСДЕФ', 2, 4)
    АБСДЕФ
    >>> slice_all('АБСДЕФ', -4, -2)
    АБСДЕФ
    >>> slice_all(None, 2, 4)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> slice_all('abcdef', SSIZE_T_MAX, SSIZE_T_MIN)
    abcdef
    """
    print(s[:])


def slice_start_none(unicode s, Py_ssize_t i, Py_ssize_t j):
    """
    >>> slice_start_none('abcdef', 2, 3)
    cdef
    >>> slice_start_none('abcdef', 0, 5)
    abcdef
    >>> slice_start_none('abcdef', -6, -1)
    abcdef
    >>> slice_start_none('abcdef', -6, -7)
    abcdef
    >>> slice_start_none('abcdef', -7, -7)
    abcdef
    >>> slice_start_none('aАbБcСdДeЕfФ', 2, 8)
    bБcСdДeЕfФ
    >>> slice_start_none('АБСДЕФ', 2, 4)
    СДЕФ
    >>> slice_start_none('АБСДЕФ', -4, -2)
    СДЕФ
    >>> slice_start_none(None, 2, 4)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> slice_start_none('abcdef', SSIZE_T_MAX, SSIZE_T_MIN)
    <BLANKLINE>
    """
    print(s[i:None])


def slice_none_end(unicode s, Py_ssize_t i, Py_ssize_t j):
    """
    >>> slice_none_end('abcdef', 2, 3)
    ab
    >>> slice_none_end('abcdef', 0, 5)
    <BLANKLINE>
    >>> slice_none_end('abcdef', -6, -1)
    <BLANKLINE>
    >>> slice_none_end('abcdef', -6, -7)
    <BLANKLINE>
    >>> slice_none_end('abcdef', -7, -7)
    <BLANKLINE>
    >>> slice_none_end('aАbБcСdДeЕfФ', 2, 8)
    aА
    >>> slice_none_end('АБСДЕФ', 2, 4)
    АБ
    >>> slice_none_end('АБСДЕФ', -4, -2)
    АБ
    >>> slice_none_end(None, 2, 4)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> slice_none_end('abcdef', SSIZE_T_MAX, SSIZE_T_MIN)
    abcdef
    """
    print(s[None:i])


def slice_none_none(unicode s, Py_ssize_t i, Py_ssize_t j):
    """
    >>> slice_none_none('abcdef', 2, 3)
    abcdef
    >>> slice_none_none('abcdef', 0, 5)
    abcdef
    >>> slice_none_none('abcdef', -6, -1)
    abcdef
    >>> slice_none_none('abcdef', -6, -7)
    abcdef
    >>> slice_none_none('abcdef', -7, -7)
    abcdef
    >>> slice_none_none('aАbБcСdДeЕfФ', 2, 8)
    aАbБcСdДeЕfФ
    >>> slice_none_none('АБСДЕФ', 2, 4)
    АБСДЕФ
    >>> slice_none_none('АБСДЕФ', -4, -2)
    АБСДЕФ
    >>> slice_none_none(None, 2, 4)
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not subscriptable
    >>> slice_none_none('abcdef', SSIZE_T_MAX, SSIZE_T_MIN)
    abcdef
    """
    print(s[None:None])
