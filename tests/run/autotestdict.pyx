# Directive defaults to True

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
MyCdefClass.method (line 75) ; >>> add_log("cdef class method")
MyClass.method (line 65) ; >>> add_log("class method")
doc_without_test (line 47) ; Some docs
mycpdeffunc (line 53) ; >>> add_log("cpdef")
myfunc (line 44) ; >>> add_log("def")

"""

log = []


cdef cdeffunc():
    """
    Please don't include me!

    >>> True
    False
    """

def all_tests_run():
    log.sort()
    assert log == [u'cdef class method', u'class method', u'cpdef', u'def'], log

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

    >>> True
    True
    """
    
    def method(self):
        """>>> add_log("class method")"""

cdef class MyCdefClass:
    """
    Needs no hack
    
    >>> True
    True
    """
    def method(self):
        """>>> add_log("cdef class method")"""

