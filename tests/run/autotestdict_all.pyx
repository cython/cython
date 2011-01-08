# cython: autotestdict.all=True

"""
Tests autotestdict compiler directive.

Both module test and individual tests are run; finally,
all_tests_run() is executed which does final validation.

>>> items = list(__test__.items())
>>> items.sort()
>>> for key, value in items:
...     print('%s ; %s' % (key, value))
MyCdefClass.cdef_method (line 79) ; >>> add_log("cdef class method")
MyCdefClass.cpdef_method (line 76) ; >>> add_log("cpdef class method")
MyCdefClass.method (line 73) ; >>> add_log("cdef class method")
MyClass.method (line 62) ; >>> add_log("class method")
cdeffunc (line 26) ; >>> add_log("cdef")
doc_without_test (line 43) ; Some docs
mycpdeffunc (line 49) ; >>> add_log("cpdef")
myfunc (line 40) ; >>> add_log("def")

"""

log = []

cdef cdeffunc():
    """>>> add_log("cdef")"""
cdeffunc() # make sure it's being used

def all_tests_run():
    log.sort()
    assert log == [u'cdef', u'cdef class', u'cdef class method', u'class', u'class method', u'cpdef', u'cpdef class method', u'def'], log

def add_log(s):
    log.append(unicode(s))
    if len(log) == len(__test__):
        # Final per-function doctest executed
        all_tests_run()

def myfunc():
    """>>> add_log("def")"""

def doc_without_test():
    """Some docs"""

def nodocstring():
    pass

cpdef mycpdeffunc():
    """>>> add_log("cpdef")"""


class MyClass:
    """
    Needs no hack

    >>> add_log("class")
    >>> True
    True
    """

    def method(self):
        """>>> add_log("class method")"""

cdef class MyCdefClass:
    """
    Needs no hack

    >>> add_log("cdef class")
    >>> True
    True
    """
    def method(self):
        """>>> add_log("cdef class method")"""

    cpdef cpdef_method(self):
        """>>> add_log("cpdef class method")"""

    cdef cdef_method(self):
        """>>> add_log("cdef class method")"""

    def __cinit__(self):
        """
        Should not be included, as it can't be looked up with getattr

        >>> True
        False
        """

    def __dealloc__(self):
        """
        Should not be included, as it can't be looked up with getattr

        >>> True
        False
        """

    def __richcmp__(self, other, int op):
        """
        Should not be included, as it can't be looked up with getattr in Py 2

        >>> True
        False
        """

    def __nonzero__(self):
        """
        Should not be included, as it can't be looked up with getattr in Py 3.1

        >>> True
        False
        """

    def __len__(self):
        """
        Should not be included, as it can't be looked up with getattr in Py 3.1

        >>> True
        False
        """

    def __contains__(self, value):
        """
        Should not be included, as it can't be looked up with getattr in Py 3.1

        >>> True
        False
        """

cdef class MyOtherCdefClass:
    """
    Needs no hack

    >>> True
    True
    """

    def __bool__(self):
        """
        Should not be included, as it can't be looked up with getattr in Py 2

        >>> True
        False
        """
