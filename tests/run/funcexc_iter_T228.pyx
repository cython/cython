# ticket: t228

__doc__ = u"""
>>> def py_iterator():
...    if True: return
...    yield None

>>> list(py_iterator())
[]
>>> list(cy_iterator())
[]

>>> try:
...     raise ValueError
... except:
...     print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
...     a = list(py_iterator())
...     print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
True
True

>>> print(sys.exc_info()[0] is None or sys.exc_info()[0])
True

>>> try:
...     raise ValueError
... except:
...     print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
...     a = list(py_iterator())
...     print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
...     a = list(cy_iterator())
...     print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
True
True
True

>>> print(sys.exc_info()[0] is None or sys.exc_info()[0])
True

>>> double_raise(py_iterator)
True
True
True

>>> print(sys.exc_info()[0] is None or sys.exc_info()[0])
True
"""

import sys

cdef class cy_iterator(object):
    def __iter__(self):
        return self
    def __next__(self):
        raise StopIteration

def double_raise(py_iterator):
    try:
        raise ValueError
    except:
        print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
        a = list(py_iterator())
        print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])
        a = list(cy_iterator())
        print(sys.exc_info()[0] is ValueError or sys.exc_info()[0])


###### Tests to do with the optimization of StopIteration to "return NULL" #######
# we're mainly checking that
#  1. Calling __next__ manually doesn't crash (the wrapper function adds the exception)
#  2. if you raise a value then that value gets raised
#  3. putting the exception in various places try...finally / try...except blocks works

def call_next_directly():
    """
    >>> call_next_directly()
    Traceback (most recent call last):
    ...
    StopIteration
    """
    cy_iterator().__next__()

cdef class cy_iter_many_options:
    cdef what
    def __init__(self, what):
        self.what = what

    def __iter__(self):
        return self

    def __next__(self):
        if self.what == "StopIteration in finally no return":
            try:
                raise StopIteration
            finally:
                print "Finally..."
        elif self.what == "StopIteration in finally return":
            try:
                raise StopIteration
            finally:
                self.what = None
                return "in finally"  # but will stop iterating next time
        elif self.what == "StopIteration from finally":
            try:
                raise ValueError
            finally:
                raise StopIteration
        elif self.what == "catch StopIteration":
            try:
                raise StopIteration
            except StopIteration:
                self.what = None
                return "in except"  # but will stop next time
        elif self.what == "don't catch StopIteration":
            try:
                raise StopIteration
            except ValueError:
                return 0
        elif self.what == "StopIteration from except":
            try:
                raise ValueError
            except ValueError:
                raise StopIteration
        elif self.what == "StopIteration with value":
            raise StopIteration("I'm a value!")
        elif self.what is None:
            raise StopIteration
        else:
            raise ValueError("self.what didn't match anything")

def test_cy_iter_many_options(option):
    """
    >>> test_cy_iter_many_options("StopIteration in finally no return")
    Finally...
    []
    >>> test_cy_iter_many_options("StopIteration in finally return")
    ['in finally']
    >>> test_cy_iter_many_options("StopIteration from finally")
    []
    >>> test_cy_iter_many_options("catch StopIteration")
    ['in except']
    >>> test_cy_iter_many_options("don't catch StopIteration")
    []
    >>> try:
    ...     cy_iter_many_options("StopIteration with value").__next__()
    ... except StopIteration as e:
    ...     print(e.args)
    ("I'm a value!",)
    """
    return list(cy_iter_many_options(option))

