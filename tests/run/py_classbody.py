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


class ForLoopInPyClass(object):
    """
    >>> ForLoopInPyClass.i    # doctest: +ELLIPSIS
    Traceback (most recent call last):
    AttributeError: ...ForLoopInPyClass... has no attribute ...i...
    >>> ForLoopInPyClass.k
    0
    >>> ForLoopInPyClass.m
    1
    """
    for i in range(0):
        pass

    for k in range(1):
        pass

    for m in range(2):
        pass


def del_in_class(x):
    """
    >>> del_in_class(True)
    no error
    >>> del_in_class(False)
    NameError
    """
    try:
        class Test(object):
            if x:
                attr = 1
            del attr
    except NameError:
        print("NameError")
    else:
        print("no error")
