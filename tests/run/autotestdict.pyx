# cython: autotestdict=True
# Directive defaults to True, but not when testing in Py3.4
"""
Tests autotestdict compiler directive.

Both module test and individual tests are run; finally,
all_tests_run() is executed which does final validation.

>>> items = list(__test__.items())
>>> items.sort()
>>> for key, value in items:
...     print('%s ; %s' % (key, value))
MyCdefClass.cpdef_method (line 77) ; >>> add_log("cpdef class method")
MyCdefClass.method (line 74) ; >>> add_log("cdef class method")
MyClass.method (line 63) ; >>> add_log("class method")
mycpdeffunc (line 50) ; >>> add_log("cpdef")
myfunc (line 40) ; >>> add_log("def")
"""

import sys
log = []

cdef cdeffunc():
    """
    >>> True
    False
    """
cdeffunc() # make sure it's being used

def all_tests_run():
    assert sorted(log) == sorted([u'cdef class', u'class'] + (
        2 * [u'cdef class method', u'class method', u'cpdef', u'cpdef class method', u'def'])), sorted(log)

def add_log(s):
    log.append(unicode(s))
    if len(log) == len(__test__) + 7:
        # Final per-function doctest executed
        all_tests_run()

def myfunc():
    """>>> add_log("def")"""
    x = lambda a:1 # no docstring here ...

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
        """>>> add_log("cdef class cmethod")"""

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

        >>> sys.version_info < (3, 4)
        False
        """

    def __contains__(self, value):
        """
        Should not be included, as it can't be looked up with getattr in Py 3.1

        >>> sys.version_info < (3, 4)
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
