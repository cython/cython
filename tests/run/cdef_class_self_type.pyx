# mode: run

# cython: binding=True, annotation_typing=True

# The feature this is testing only really works on Python 3, so many
# of the tests are hidden behind a version guard in the module __doc__.
# This is unavoidable and due to the different way Python treats
# bound/unbound methods between versions 2 and 3

cimport cython

ctypedef fused FooOrInt:
    Foo
    int

cdef class Foo:
    cdef update(self):
        # a function that'll only be accessible if we know the type
        pass

    def meth1(self, try_to_run_update=True):
        """
        >>> f = Foo()
        >>> f.meth1()
        'Foo'
        >>> Foo.meth1(f)
        'Foo'

        See module __doc__ for more
        """
        if try_to_run_update:
            self.update()  # no error
        return cython.typeof(self)

    def meth2(Foo self, try_to_run_update=True):
        """
        # specifying the type as Foo should do nothing different
        >>> f = Foo()
        >>> f.meth2()
        'Foo'
        >>> Foo.meth2(f)
        'Foo'

        See module __doc__ for more
        """
        if try_to_run_update:
            self.update()  # no error
        return cython.typeof(self)

    def meth_o(object self):
        """
        >>> Foo().meth_o()
        Couldn't find self.update
        ('Python object', 'Foo')

        See module __doc__ for more...
        """
        try:
            self.update()
        except AttributeError:
            print("Couldn't find self.update")
        else:
            print("Called self.update()")
        return cython.typeof(self), type(self).__name__

    def meth_i(int i):
        """
        (passed Foo not int)
        >>> Foo().meth_i() # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        TypeError:

        See module doc for more

        (passed dict not int)
        >>> Foo.meth_i({}) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        TypeError:
        """
        return i+1

    def meth_fused(FooOrInt x):
        """
        >>> Foo.meth_fused(1)
        'int'
        >>> Foo().meth_fused()
        'Foo'
        """
        return cython.typeof(x)

    @cython.locals(i=int)
    def meth_locals(i):
        """
        See module doc for more
        >>> Foo().meth_locals() # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        TypeError:
        """
        return cython.typeof(i)

    def meth_anno(i: cython.int):
        """
        See module __doc__ for more
        >>> Foo().meth_anno() # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        TypeError:
        """
        return cython.typeof(i)

import sys
if sys.version_info[0] > 2:
    # The vast majority of the tests here will only work on Python 3
    __doc__ = """
    >>> Foo.meth1(1, try_to_run_update=False)  # not really safe, but current behaviour is not to detect it
    'Foo'

    >>> Foo.meth2(1, try_to_run_update=False)  # not really safe, but current behaviour is not to detect it
    'Foo'

    >>> Foo.meth_i(1)
    2

    >>> Foo.meth_o({})
    Called self.update()
    ('Python object', 'dict')

    >>> Foo.meth_locals(1)
    'int'

    >>> Foo.meth_anno(1)
    'int'
    """
