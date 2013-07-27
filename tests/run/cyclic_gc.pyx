# mode: run
# tag: cyclicgc


cimport cython

@cython.test_fail_if_path_exists('//CClassDefNode[@scope.has_cyclic_pyobject_attrs = True]')
@cython.test_assert_path_exists('//CClassDefNode',
                                '//CClassDefNode[@scope]',
                                '//CClassDefNode[@scope.has_cyclic_pyobject_attrs = False]')
cdef class ExtTypeNoGC:
    """
    >>> obj = ExtTypeNoGC()
    >>> obj = ExtTypeNoGC()
    >>> obj = ExtTypeNoGC()
    >>> obj = ExtTypeNoGC()
    >>> obj = ExtTypeNoGC()
    >>> obj = ExtTypeNoGC()
    """


@cython.test_fail_if_path_exists('//CClassDefNode[@scope.has_cyclic_pyobject_attrs = True]')
@cython.test_assert_path_exists('//CClassDefNode',
                                '//CClassDefNode[@scope]',
                                '//CClassDefNode[@scope.has_cyclic_pyobject_attrs = False]')
cdef class ExtSubTypeNoGC(ExtTypeNoGC):
    """
    >>> obj = ExtSubTypeNoGC()
    >>> obj = ExtSubTypeNoGC()
    >>> obj = ExtSubTypeNoGC()
    >>> obj = ExtSubTypeNoGC()
    >>> obj = ExtSubTypeNoGC()
    >>> obj = ExtSubTypeNoGC()
    """


@cython.test_fail_if_path_exists('//CClassDefNode[@scope.has_cyclic_pyobject_attrs = True]')
@cython.test_assert_path_exists('//CClassDefNode',
                                '//CClassDefNode[@scope]',
                                '//CClassDefNode[@scope.has_cyclic_pyobject_attrs = False]')
cdef class ExtTypePyArgsNoGC:
    """
    >>> obj = ExtTypePyArgsNoGC()
    >>> obj = ExtTypePyArgsNoGC()
    >>> obj = ExtTypePyArgsNoGC()
    >>> obj = ExtTypePyArgsNoGC()
    >>> obj = ExtTypePyArgsNoGC()
    >>> obj = ExtTypePyArgsNoGC()
    """
    cdef bytes b
    cdef str s
    cdef unicode u


@cython.test_fail_if_path_exists('//CClassDefNode[@scope.has_cyclic_pyobject_attrs = True]')
@cython.test_assert_path_exists('//CClassDefNode',
                                '//CClassDefNode[@scope]',
                                '//CClassDefNode[@scope.has_cyclic_pyobject_attrs = False]')
cdef class ExtSubTypePyArgsNoGC(ExtTypePyArgsNoGC):
    """
    >>> obj = ExtSubTypePyArgsNoGC()
    >>> obj = ExtSubTypePyArgsNoGC()
    >>> obj = ExtSubTypePyArgsNoGC()
    >>> obj = ExtSubTypePyArgsNoGC()
    >>> obj = ExtSubTypePyArgsNoGC()
    >>> obj = ExtSubTypePyArgsNoGC()
    """


@cython.test_fail_if_path_exists('//CClassDefNode[@scope.has_cyclic_pyobject_attrs = False]')
@cython.test_assert_path_exists('//CClassDefNode',
                                '//CClassDefNode[@scope]',
                                '//CClassDefNode[@scope.has_cyclic_pyobject_attrs = True]')
cdef class ExtTypePyArgsWithGC:
    """
    >>> obj = ExtTypePyArgsWithGC()
    >>> obj = ExtTypePyArgsWithGC()
    >>> obj = ExtTypePyArgsWithGC()
    >>> obj = ExtTypePyArgsWithGC()
    >>> obj = ExtTypePyArgsWithGC()
    >>> obj = ExtTypePyArgsWithGC()
    """
    cdef bytes b
    cdef str s
    cdef unicode u
    cdef list l


@cython.test_fail_if_path_exists('//CClassDefNode[@scope.has_cyclic_pyobject_attrs = True]')
@cython.test_assert_path_exists('//CClassDefNode',
                                '//CClassDefNode[@scope]',
                                '//CClassDefNode[@scope.has_cyclic_pyobject_attrs = False]')
cdef class ExtSubTypePyArgsWithGC(ExtTypePyArgsWithGC):
    """
    >>> obj = ExtSubTypePyArgsWithGC()
    >>> obj = ExtSubTypePyArgsWithGC()
    >>> obj = ExtSubTypePyArgsWithGC()
    >>> obj = ExtSubTypePyArgsWithGC()
    >>> obj = ExtSubTypePyArgsWithGC()
    >>> obj = ExtSubTypePyArgsWithGC()
    """
