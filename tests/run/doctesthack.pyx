#cython: doctesthack=True

"""
Tests doctesthack compiler directive.

The doctests are actually run as part of this test;
which makes the test flow a bit untraditional. Both
module test and individual tests are run; finally,
all_tests_run() is executed which does final validation.

>>> items = __test__.items()
>>> items.sort()
>>> for key, value in items:
...     print key, ';', value
mycpdeffunc (line 40) ; >>> add_log("cpdef")
myfunc (line 34) ; >>> add_log("def")

"""

log = []

#__test__ = {'a':'445', 'b':'3'}

def all_tests_run():
    log.sort()
    assert log == [u'cpdef', u'def'], log

def add_log(s):
    log.append(unicode(s))
    if len(log) == len(__test__):
        # Final per-function doctest executed
        all_tests_run()

def myfunc():
    """>>> add_log("def")"""

def nodocstring():
    pass

cpdef mycpdeffunc():
    """>>> add_log("cpdef")"""


class MyClass:
    """
    Needs no hack

    >>> True
    True
    """
    
    def method(self):
        """
        >>> True
        False
        """

## cdef class MyCdefClass:
##     """
##     >>> add_log("cdef class")
##     """
##     def method(self):
##         """
##         >>> add_log("cdef class method")
##         """

