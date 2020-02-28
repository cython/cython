# mode: run

# cython: binding=True, annotation_typing=True

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
        >>> Foo.meth1(1, try_to_run_update=False)  # not really safe, but current behaviour is not to detect it
        'Foo'
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
        >>> Foo.meth2(1, try_to_run_update=False)  # not really safe, but current behaviour is not to detect it
        'Foo'
        """
        if try_to_run_update:
            self.update()  # no error
        return cython.typeof(self)

    def meth_o(object self):
        """
        >>> Foo().meth_o()
        Couldn't find self.update
        ('Python object', 'Foo')
        >>> Foo.meth_o({})
        Called self.update()
        ('Python object', 'dict')
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
        >>> Foo().meth_i() # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        TypeError:
        >>> Foo.meth_i(1)
        2
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
        >>> Foo.meth_locals(1)
        'int'
        >>> Foo().meth_locals() # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        TypeError:
        """
        return cython.typeof(i)

    def meth_anno(i: cython.int):
        """
        >>> Foo.meth_anno(1)
        'int'
        >>> Foo().meth_anno() # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        TypeError:
        """
        return cython.typeof(i)
