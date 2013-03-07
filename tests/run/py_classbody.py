# mode: run
# tag: pyclass, global


pyvar = 2

class TestPyAttr(object):
    """
    >>> TestPyAttr.pyvar    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    AttributeError: ...TestPyAttr...has no attribute 'pyvar'
    >>> TestPyAttr.pyval1
    3
    >>> TestPyAttr.pyval2
    2
    """
    pyvar = 3
    pyval1 = pyvar
    del pyvar
    pyval2 = pyvar


import cython
cdefvar = cython.declare(int, 10)

class TestCdefAttr(object):
    """
    >>> TestCdefAttr.cdefvar   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    AttributeError: ...TestCdefAttr...has no attribute 'cdefvar'
    >>> TestCdefAttr.cdefval1
    11

    >>> #TestCdefAttr.cdefval2
    """
    cdefvar = 11
    cdefval1 = cdefvar
    del cdefvar
    # cdefval2 = cdefvar       # FIXME: doesn't currently work ...
