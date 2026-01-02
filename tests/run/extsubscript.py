# mode: run
# tag: subscript, getitem, setitem, delitem

# GENERATED TEST CODE
# Run me as a Python script to regenerate my test code.
# If things go wrong, delete all lines between the START/END markers and rerun.

import cython


###### START: generated test code ######
@cython.cclass
class ExtMapDel():
    """
    >>> obj = ExtMapDel()
    >>> del obj[5]  # ExtMapDel
    __delitem__(ExtMapDel, i=5)
    >>> import cython

    >>> class PyMapDel():
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel, i={i})")

    >>> obj = PyMapDel()
    >>> del obj[5]  # PyMapDel
    __delitem__(PyMapDel, i=5)

    >>> class PyMapDel_subclassing_ExtMapDel(ExtMapDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel
    __delitem__(PyMapDel_subclassing_ExtMapDel, i=5)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel, i={i})")


@cython.cclass
class ExtSeqDel():
    """
    >>> obj = ExtSeqDel()
    >>> del obj[5]  # ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqDel():
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel()
    >>> del obj[5]  # PySeqDel
    __delitem__(PySeqDel, i: cython.Py_ssize_t=5)

    >>> class PySeqDel_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel
    __delitem__(PySeqDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet():
    """
    >>> obj = ExtMapSet()
    >>> obj[5] = 10  # ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)
    >>> import cython

    >>> class PyMapSet():
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet, i={i}, value={value})")

    >>> obj = PyMapSet()
    >>> obj[5] = 10  # PyMapSet
    __setitem__(PyMapSet, i=5, value=10)

    >>> class PyMapSet_subclassing_ExtMapSet(ExtMapSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet
    __setitem__(PyMapSet_subclassing_ExtMapSet, i=5, value=10)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet, i={i}, value={value})")


@cython.cclass
class ExtSeqSet():
    """
    >>> obj = ExtSeqSet()
    >>> obj[5] = 10  # ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqSet():
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet()
    >>> obj[5] = 10  # PySeqSet
    __setitem__(PySeqSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqSet_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet
    __setitem__(PySeqSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel():
    """
    >>> obj = ExtMapSetDel()
    >>> obj[5] = 10  # ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)
    >>> import cython

    >>> class PyMapSetDel():
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel, i={i})")

    >>> obj = PyMapSetDel()
    >>> obj[5] = 10  # PyMapSetDel
    __setitem__(PyMapSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel
    __delitem__(PyMapSetDel, i=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel, i={i})")


@cython.cclass
class ExtSeqSetDel():
    """
    >>> obj = ExtSeqSetDel()
    >>> obj[5] = 10  # ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSetDel():
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel()
    >>> obj[5] = 10  # PySeqSetDel
    __setitem__(PySeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel
    __delitem__(PySeqSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet():
    """
    >>> obj = ExtMapGet()
    >>> obj[5]  # ExtMapGet
    __getitem__(ExtMapGet, i=5)
    >>> import cython

    >>> class PyMapGet():
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet, i={i})")

    >>> obj = PyMapGet()
    >>> obj[5]  # PyMapGet
    __getitem__(PyMapGet, i=5)

    >>> class PyMapGet_subclassing_ExtMapGet(ExtMapGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet
    __getitem__(PyMapGet_subclassing_ExtMapGet, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet, i={i})")


@cython.cclass
class ExtSeqGet():
    """
    >>> obj = ExtSeqGet()
    >>> obj[5]  # ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGet():
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet()
    >>> obj[5]  # PySeqGet
    __getitem__(PySeqGet, i: cython.Py_ssize_t=5)

    >>> class PySeqGet_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet
    __getitem__(PySeqGet_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel():
    """
    >>> obj = ExtMapGetDel()
    >>> obj[5]  # ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    >>> del obj[5]  # ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)
    >>> import cython

    >>> class PyMapGetDel():
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel, i={i})")

    >>> obj = PyMapGetDel()
    >>> obj[5]  # PyMapGetDel
    __getitem__(PyMapGetDel, i=5)
    >>> del obj[5]  # PyMapGetDel
    __delitem__(PyMapGetDel, i=5)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel, i={i})")


@cython.cclass
class ExtSeqGetDel():
    """
    >>> obj = ExtSeqGetDel()
    >>> obj[5]  # ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetDel():
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel()
    >>> obj[5]  # PySeqGetDel
    __getitem__(PySeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel
    __delitem__(PySeqGetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet():
    """
    >>> obj = ExtMapGetSet()
    >>> obj[5]  # ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    >>> obj[5] = 10  # ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)
    >>> import cython

    >>> class PyMapGetSet():
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet, i={i}, value={value})")

    >>> obj = PyMapGetSet()
    >>> obj[5]  # PyMapGetSet
    __getitem__(PyMapGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetSet
    __setitem__(PyMapGetSet, i=5, value=10)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet, i=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet():
    """
    >>> obj = ExtSeqGetSet()
    >>> obj[5]  # ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqGetSet():
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet()
    >>> obj[5]  # PySeqGetSet
    __getitem__(PySeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet
    __setitem__(PySeqGetSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel():
    """
    >>> obj = ExtMapGetSetDel()
    >>> obj[5]  # ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)
    >>> import cython

    >>> class PyMapGetSetDel():
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel, i={i})")

    >>> obj = PyMapGetSetDel()
    >>> obj[5]  # PyMapGetSetDel
    __getitem__(PyMapGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel
    __setitem__(PyMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel
    __delitem__(PyMapGetSetDel, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel, i={i})")


@cython.cclass
class ExtSeqGetSetDel():
    """
    >>> obj = ExtSeqGetSetDel()
    >>> obj[5]  # ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel():
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel()
    >>> obj[5]  # PySeqGetSetDel
    __getitem__(PySeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel
    __setitem__(PySeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel
    __delitem__(PySeqGetSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtMapDel_subclassing_ExtMapDel()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtMapDel
    __delitem__(ExtMapDel_subclassing_ExtMapDel, i=5)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtMapDel(ExtMapDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel
    __delitem__(PyMapDel_subclassing_ExtMapDel, i=5)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapDel(ExtMapDel_subclassing_ExtMapDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapDel
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapDel, i=5)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtMapDel, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtSeqDel_subclassing_ExtMapDel()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtMapDel
    __delitem__(ExtSeqDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtMapDel(ExtMapDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtMapDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtMapDel
    __delitem__(PySeqDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapDel(ExtSeqDel_subclassing_ExtMapDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapDel
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtMapSet_subclassing_ExtMapDel()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtMapDel
    __setitem__(ExtMapSet_subclassing_ExtMapDel, i=5, value=10)
    >>> del obj[5]  # ExtMapSet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtMapDel(ExtMapDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapDel
    __setitem__(PyMapSet_subclassing_ExtMapDel, i=5, value=10)
    >>> del obj[5]  # PyMapSet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapDel(ExtMapSet_subclassing_ExtMapDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapDel
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapDel, i=5, value=10)
    >>> del obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtMapDel, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtSeqSet_subclassing_ExtMapDel()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtMapDel
    __setitem__(ExtSeqSet_subclassing_ExtMapDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtMapDel(ExtMapDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtMapDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtMapDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtMapDel
    __setitem__(PySeqSet_subclassing_ExtMapDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapDel(ExtSeqSet_subclassing_ExtMapDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapDel
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtMapDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtMapDel()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtMapDel
    __setitem__(ExtMapSetDel_subclassing_ExtMapDel, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtMapDel
    __delitem__(ExtMapSetDel_subclassing_ExtMapDel, i=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtMapDel(ExtMapDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapDel
    __setitem__(PyMapSetDel_subclassing_ExtMapDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapDel
    __delitem__(PyMapSetDel_subclassing_ExtMapDel, i=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapDel(ExtMapSetDel_subclassing_ExtMapDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapDel
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapDel
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapDel, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtMapDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtMapDel, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtMapDel()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtMapDel
    __setitem__(ExtSeqSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtMapDel
    __delitem__(ExtSeqSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtMapDel(ExtMapDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtMapDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtMapDel
    __setitem__(PySeqSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtMapDel
    __delitem__(PySeqSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapDel(ExtSeqSetDel_subclassing_ExtMapDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapDel
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapDel
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtMapGet_subclassing_ExtMapDel()
    >>> obj[5]  # ExtMapGet_subclassing_ExtMapDel
    __getitem__(ExtMapGet_subclassing_ExtMapDel, i=5)
    >>> del obj[5]  # ExtMapGet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtMapDel(ExtMapDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapDel
    __getitem__(PyMapGet_subclassing_ExtMapDel, i=5)
    >>> del obj[5]  # PyMapGet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapDel(ExtMapGet_subclassing_ExtMapDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapDel
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapDel, i=5)
    >>> del obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtMapDel, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtSeqGet_subclassing_ExtMapDel()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtMapDel
    __getitem__(ExtSeqGet_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtMapDel(ExtMapDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtMapDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtMapDel
    __getitem__(PySeqGet_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapDel(ExtSeqGet_subclassing_ExtMapDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapDel
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtMapDel()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtMapDel
    __getitem__(ExtMapGetDel_subclassing_ExtMapDel, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtMapDel
    __delitem__(ExtMapGetDel_subclassing_ExtMapDel, i=5)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtMapDel(ExtMapDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapDel
    __getitem__(PyMapGetDel_subclassing_ExtMapDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapDel
    __delitem__(PyMapGetDel_subclassing_ExtMapDel, i=5)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapDel(ExtMapGetDel_subclassing_ExtMapDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapDel
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapDel
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtMapDel, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtMapDel, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtMapDel()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtMapDel
    __getitem__(ExtSeqGetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtMapDel
    __delitem__(ExtSeqGetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtMapDel(ExtMapDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtMapDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtMapDel
    __getitem__(PySeqGetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtMapDel
    __delitem__(PySeqGetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapDel(ExtSeqGetDel_subclassing_ExtMapDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapDel
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapDel
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtMapDel()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtMapDel
    __getitem__(ExtMapGetSet_subclassing_ExtMapDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtMapDel
    __setitem__(ExtMapGetSet_subclassing_ExtMapDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtMapDel(ExtMapDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapDel
    __getitem__(PyMapGetSet_subclassing_ExtMapDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapDel
    __setitem__(PyMapGetSet_subclassing_ExtMapDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapDel(ExtMapGetSet_subclassing_ExtMapDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapDel
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapDel
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtMapDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtMapDel, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtMapDel()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtMapDel
    __getitem__(ExtSeqGetSet_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtMapDel
    __setitem__(ExtSeqGetSet_subclassing_ExtMapDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtMapDel(ExtMapDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtMapDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtMapDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtMapDel
    __getitem__(PySeqGetSet_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtMapDel
    __setitem__(PySeqGetSet_subclassing_ExtMapDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapDel(ExtSeqGetSet_subclassing_ExtMapDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapDel
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapDel
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapDel
    __delitem__(ExtMapDel, i=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtMapDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtMapDel()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtMapDel
    __getitem__(ExtMapGetSetDel_subclassing_ExtMapDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtMapDel
    __setitem__(ExtMapGetSetDel_subclassing_ExtMapDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtMapDel
    __delitem__(ExtMapGetSetDel_subclassing_ExtMapDel, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtMapDel(ExtMapDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapDel
    __getitem__(PyMapGetSetDel_subclassing_ExtMapDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapDel
    __setitem__(PyMapGetSetDel_subclassing_ExtMapDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapDel
    __delitem__(PyMapGetSetDel_subclassing_ExtMapDel, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapDel(ExtMapGetSetDel_subclassing_ExtMapDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapDel
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapDel
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapDel
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtMapDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtMapDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtMapDel, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtMapDel(ExtMapDel):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtMapDel()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapDel
    __getitem__(ExtSeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtMapDel
    __setitem__(ExtSeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapDel
    __delitem__(ExtSeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtMapDel(ExtMapDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtMapDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtMapDel
    __getitem__(PySeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtMapDel
    __setitem__(PySeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtMapDel
    __delitem__(PySeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapDel(ExtSeqGetSetDel_subclassing_ExtMapDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapDel
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapDel
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapDel
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtMapDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtMapDel_subclassing_ExtSeqDel()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtSeqDel
    __delitem__(ExtMapDel_subclassing_ExtSeqDel, i=5)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtSeqDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtSeqDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtSeqDel
    __delitem__(PyMapDel_subclassing_ExtSeqDel, i=5)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqDel(ExtMapDel_subclassing_ExtSeqDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqDel
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqDel, i=5)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtSeqDel, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtSeqDel_subclassing_ExtSeqDel()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel
    __delitem__(PySeqDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqDel(ExtSeqDel_subclassing_ExtSeqDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqDel
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtMapSet_subclassing_ExtSeqDel()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtSeqDel
    __setitem__(ExtMapSet_subclassing_ExtSeqDel, i=5, value=10)
    >>> del obj[5]  # ExtMapSet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtSeqDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtSeqDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtSeqDel
    __setitem__(PyMapSet_subclassing_ExtSeqDel, i=5, value=10)
    >>> del obj[5]  # PyMapSet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqDel(ExtMapSet_subclassing_ExtSeqDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqDel
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqDel, i=5, value=10)
    >>> del obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtSeqDel, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtSeqSet_subclassing_ExtSeqDel()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtSeqDel
    __setitem__(ExtSeqSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqDel
    __setitem__(PySeqSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqDel(ExtSeqSet_subclassing_ExtSeqDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqDel
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtSeqDel()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtSeqDel
    __setitem__(ExtMapSetDel_subclassing_ExtSeqDel, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtSeqDel
    __delitem__(ExtMapSetDel_subclassing_ExtSeqDel, i=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtSeqDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtSeqDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtSeqDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtSeqDel
    __setitem__(PyMapSetDel_subclassing_ExtSeqDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtSeqDel
    __delitem__(PyMapSetDel_subclassing_ExtSeqDel, i=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqDel(ExtMapSetDel_subclassing_ExtSeqDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqDel
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqDel
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqDel, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtSeqDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtSeqDel, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtSeqDel()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtSeqDel
    __setitem__(ExtSeqSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtSeqDel
    __delitem__(ExtSeqSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqDel
    __setitem__(PySeqSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqDel
    __delitem__(PySeqSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqDel(ExtSeqSetDel_subclassing_ExtSeqDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqDel
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqDel
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtMapGet_subclassing_ExtSeqDel()
    >>> obj[5]  # ExtMapGet_subclassing_ExtSeqDel
    __getitem__(ExtMapGet_subclassing_ExtSeqDel, i=5)
    >>> del obj[5]  # ExtMapGet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtSeqDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtSeqDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtSeqDel
    __getitem__(PyMapGet_subclassing_ExtSeqDel, i=5)
    >>> del obj[5]  # PyMapGet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqDel(ExtMapGet_subclassing_ExtSeqDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqDel
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqDel, i=5)
    >>> del obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtSeqDel, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtSeqGet_subclassing_ExtSeqDel()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtSeqDel
    __getitem__(ExtSeqGet_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqDel
    __getitem__(PySeqGet_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqDel(ExtSeqGet_subclassing_ExtSeqDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqDel
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtSeqDel()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtSeqDel
    __getitem__(ExtMapGetDel_subclassing_ExtSeqDel, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtSeqDel
    __delitem__(ExtMapGetDel_subclassing_ExtSeqDel, i=5)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtSeqDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtSeqDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtSeqDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtSeqDel
    __getitem__(PyMapGetDel_subclassing_ExtSeqDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtSeqDel
    __delitem__(PyMapGetDel_subclassing_ExtSeqDel, i=5)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqDel(ExtMapGetDel_subclassing_ExtSeqDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqDel
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqDel
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtSeqDel, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtSeqDel, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtSeqDel()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtSeqDel
    __getitem__(ExtSeqGetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtSeqDel
    __delitem__(ExtSeqGetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqDel
    __getitem__(PySeqGetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqDel
    __delitem__(PySeqGetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqDel(ExtSeqGetDel_subclassing_ExtSeqDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqDel
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqDel
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtSeqDel()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtSeqDel
    __getitem__(ExtMapGetSet_subclassing_ExtSeqDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtSeqDel
    __setitem__(ExtMapGetSet_subclassing_ExtSeqDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtSeqDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtSeqDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtSeqDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtSeqDel
    __getitem__(PyMapGetSet_subclassing_ExtSeqDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtSeqDel
    __setitem__(PyMapGetSet_subclassing_ExtSeqDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqDel(ExtMapGetSet_subclassing_ExtSeqDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqDel
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqDel
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtSeqDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtSeqDel, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtSeqDel()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtSeqDel
    __getitem__(ExtSeqGetSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtSeqDel
    __setitem__(ExtSeqGetSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqDel
    __getitem__(PySeqGetSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqDel
    __setitem__(PySeqGetSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqDel(ExtSeqGetSet_subclassing_ExtSeqDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqDel
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqDel
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqDel
    __delitem__(ExtSeqDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtSeqDel()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqDel
    __getitem__(ExtMapGetSetDel_subclassing_ExtSeqDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtSeqDel
    __setitem__(ExtMapGetSetDel_subclassing_ExtSeqDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqDel
    __delitem__(ExtMapGetSetDel_subclassing_ExtSeqDel, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtSeqDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtSeqDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtSeqDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtSeqDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtSeqDel
    __getitem__(PyMapGetSetDel_subclassing_ExtSeqDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtSeqDel
    __setitem__(PyMapGetSetDel_subclassing_ExtSeqDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtSeqDel
    __delitem__(PyMapGetSetDel_subclassing_ExtSeqDel, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqDel(ExtMapGetSetDel_subclassing_ExtSeqDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqDel
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqDel
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqDel
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtSeqDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtSeqDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtSeqDel, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtSeqDel(ExtSeqDel):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtSeqDel()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqDel
    __getitem__(ExtSeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtSeqDel
    __setitem__(ExtSeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqDel
    __delitem__(ExtSeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtSeqDel(ExtSeqDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqDel
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqDel
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqDel
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqDel(ExtSeqGetSetDel_subclassing_ExtSeqDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqDel
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqDel
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqDel
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtSeqDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtMapDel_subclassing_ExtMapSet()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtMapSet
    __delitem__(ExtMapDel_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # ExtMapDel_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtMapSet(ExtMapSet):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapSet, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapSet()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapSet
    __delitem__(PyMapDel_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapSet(ExtMapDel_subclassing_ExtMapSet):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapSet, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapSet()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapSet
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtMapSet, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtSeqDel_subclassing_ExtMapSet()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtMapSet
    __delitem__(ExtSeqDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqDel_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtMapSet(ExtMapSet):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtMapSet()
    >>> del obj[5]  # PySeqDel_subclassing_ExtMapSet
    __delitem__(PySeqDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapSet(ExtSeqDel_subclassing_ExtMapSet):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapSet()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapSet
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtMapSet_subclassing_ExtMapSet()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtMapSet
    __setitem__(ExtMapSet_subclassing_ExtMapSet, i=5, value=10)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtMapSet(ExtMapSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet
    __setitem__(PyMapSet_subclassing_ExtMapSet, i=5, value=10)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapSet(ExtMapSet_subclassing_ExtMapSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapSet, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapSet()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapSet
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapSet, i=5, value=10)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtMapSet, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtSeqSet_subclassing_ExtMapSet()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtMapSet
    __setitem__(ExtSeqSet_subclassing_ExtMapSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtMapSet(ExtMapSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtMapSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtMapSet()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtMapSet
    __setitem__(PySeqSet_subclassing_ExtMapSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapSet(ExtSeqSet_subclassing_ExtMapSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapSet()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapSet
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtMapSet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtMapSet()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtMapSet
    __setitem__(ExtMapSetDel_subclassing_ExtMapSet, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtMapSet
    __delitem__(ExtMapSetDel_subclassing_ExtMapSet, i=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtMapSet(ExtMapSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSet, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSet()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSet
    __setitem__(PyMapSetDel_subclassing_ExtMapSet, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSet
    __delitem__(PyMapSetDel_subclassing_ExtMapSet, i=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSet(ExtMapSetDel_subclassing_ExtMapSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSet, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSet()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSet
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSet, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSet
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSet, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtMapSet, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtMapSet, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtMapSet()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtMapSet
    __setitem__(ExtSeqSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtMapSet
    __delitem__(ExtSeqSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtMapSet(ExtMapSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtMapSet()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtMapSet
    __setitem__(PySeqSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtMapSet
    __delitem__(PySeqSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSet(ExtSeqSetDel_subclassing_ExtMapSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSet()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSet
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSet
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtMapGet_subclassing_ExtMapSet()
    >>> obj[5]  # ExtMapGet_subclassing_ExtMapSet
    __getitem__(ExtMapGet_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # ExtMapGet_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtMapSet(ExtMapSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapSet, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapSet()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapSet
    __getitem__(PyMapGet_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapSet(ExtMapGet_subclassing_ExtMapSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapSet, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapSet()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapSet
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtMapSet, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtSeqGet_subclassing_ExtMapSet()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtMapSet
    __getitem__(ExtSeqGet_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGet_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtMapSet(ExtMapSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtMapSet()
    >>> obj[5]  # PySeqGet_subclassing_ExtMapSet
    __getitem__(PySeqGet_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapSet(ExtSeqGet_subclassing_ExtMapSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapSet()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapSet
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtMapSet()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtMapSet
    __getitem__(ExtMapGetDel_subclassing_ExtMapSet, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtMapSet
    __delitem__(ExtMapGetDel_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # ExtMapGetDel_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtMapSet(ExtMapSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapSet, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapSet, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapSet()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapSet
    __getitem__(PyMapGetDel_subclassing_ExtMapSet, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapSet
    __delitem__(PyMapGetDel_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSet(ExtMapGetDel_subclassing_ExtMapSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSet, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSet, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSet()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSet
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSet, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSet
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtMapSet, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtMapSet, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtMapSet()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtMapSet
    __getitem__(ExtSeqGetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtMapSet
    __delitem__(ExtSeqGetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetDel_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtMapSet(ExtMapSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtMapSet()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtMapSet
    __getitem__(PySeqGetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtMapSet
    __delitem__(PySeqGetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSet(ExtSeqGetDel_subclassing_ExtMapSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSet()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSet
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSet
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSet
    __setitem__(ExtMapSet, i=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtMapSet()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtMapSet
    __getitem__(ExtMapGetSet_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtMapSet
    __setitem__(ExtMapGetSet_subclassing_ExtMapSet, i=5, value=10)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtMapSet(ExtMapSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapSet, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapSet()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapSet
    __getitem__(PyMapGetSet_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapSet
    __setitem__(PyMapGetSet_subclassing_ExtMapSet, i=5, value=10)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSet(ExtMapGetSet_subclassing_ExtMapSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSet, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSet()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSet
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSet
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSet, i=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtMapSet, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtMapSet, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtMapSet()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtMapSet
    __getitem__(ExtSeqGetSet_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtMapSet
    __setitem__(ExtSeqGetSet_subclassing_ExtMapSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtMapSet(ExtMapSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtMapSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtMapSet()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtMapSet
    __getitem__(PySeqGetSet_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtMapSet
    __setitem__(PySeqGetSet_subclassing_ExtMapSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSet(ExtSeqGetSet_subclassing_ExtMapSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSet()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSet
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSet
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtMapSet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtMapSet()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtMapSet
    __getitem__(ExtMapGetSetDel_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtMapSet
    __setitem__(ExtMapGetSetDel_subclassing_ExtMapSet, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtMapSet
    __delitem__(ExtMapGetSetDel_subclassing_ExtMapSet, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtMapSet(ExtMapSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapSet, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapSet()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapSet
    __getitem__(PyMapGetSetDel_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapSet
    __setitem__(PyMapGetSetDel_subclassing_ExtMapSet, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapSet
    __delitem__(PyMapGetSetDel_subclassing_ExtMapSet, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSet(ExtMapGetSetDel_subclassing_ExtMapSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSet, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSet()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSet
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSet, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSet
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSet, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSet
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSet, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtMapSet, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtMapSet, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtMapSet, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtMapSet(ExtMapSet):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtMapSet()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapSet
    __getitem__(ExtSeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtMapSet
    __setitem__(ExtSeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapSet
    __delitem__(ExtSeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtMapSet(ExtMapSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtMapSet()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtMapSet
    __getitem__(PySeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtMapSet
    __setitem__(PySeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtMapSet
    __delitem__(PySeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSet(ExtSeqGetSetDel_subclassing_ExtMapSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSet()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSet
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSet
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSet
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtMapSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtMapDel_subclassing_ExtSeqSet()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtSeqSet
    __delitem__(ExtMapDel_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # ExtMapDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtSeqSet, i={i})")

    >>> obj = PyMapDel_subclassing_ExtSeqSet()
    >>> del obj[5]  # PyMapDel_subclassing_ExtSeqSet
    __delitem__(PyMapDel_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqSet(ExtMapDel_subclassing_ExtSeqSet):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqSet, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqSet()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqSet
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtSeqSet, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtSeqDel_subclassing_ExtSeqSet()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtSeqSet
    __delitem__(ExtSeqDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqSet()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqSet
    __delitem__(PySeqDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqSet(ExtSeqDel_subclassing_ExtSeqSet):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqSet()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqSet
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtMapSet_subclassing_ExtSeqSet()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtSeqSet
    __setitem__(ExtMapSet_subclassing_ExtSeqSet, i=5, value=10)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtSeqSet, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtSeqSet()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtSeqSet
    __setitem__(PyMapSet_subclassing_ExtSeqSet, i=5, value=10)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqSet(ExtMapSet_subclassing_ExtSeqSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqSet, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqSet()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqSet
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqSet, i=5, value=10)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtSeqSet, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtSeqSet_subclassing_ExtSeqSet()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet
    __setitem__(PySeqSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqSet(ExtSeqSet_subclassing_ExtSeqSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqSet()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqSet
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtSeqSet()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtSeqSet
    __setitem__(ExtMapSetDel_subclassing_ExtSeqSet, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtSeqSet
    __delitem__(ExtMapSetDel_subclassing_ExtSeqSet, i=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtSeqSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtSeqSet, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtSeqSet()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtSeqSet
    __setitem__(PyMapSetDel_subclassing_ExtSeqSet, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtSeqSet
    __delitem__(PyMapSetDel_subclassing_ExtSeqSet, i=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSet(ExtMapSetDel_subclassing_ExtSeqSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSet, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSet()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSet
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSet, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSet
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSet, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtSeqSet, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtSeqSet, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtSeqSet()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtSeqSet
    __delitem__(ExtSeqSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSet()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSet
    __setitem__(PySeqSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSet
    __delitem__(PySeqSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSet(ExtSeqSetDel_subclassing_ExtSeqSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSet()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSet
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSet
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtMapGet_subclassing_ExtSeqSet()
    >>> obj[5]  # ExtMapGet_subclassing_ExtSeqSet
    __getitem__(ExtMapGet_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # ExtMapGet_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtSeqSet, i={i})")

    >>> obj = PyMapGet_subclassing_ExtSeqSet()
    >>> obj[5]  # PyMapGet_subclassing_ExtSeqSet
    __getitem__(PyMapGet_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqSet(ExtMapGet_subclassing_ExtSeqSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqSet, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqSet()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqSet
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtSeqSet, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtSeqGet_subclassing_ExtSeqSet()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtSeqSet
    __getitem__(ExtSeqGet_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGet_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqSet()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqSet
    __getitem__(PySeqGet_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqSet(ExtSeqGet_subclassing_ExtSeqSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqSet()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqSet
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtSeqSet()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtSeqSet
    __getitem__(ExtMapGetDel_subclassing_ExtSeqSet, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtSeqSet
    __delitem__(ExtMapGetDel_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # ExtMapGetDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtSeqSet, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtSeqSet, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtSeqSet()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtSeqSet
    __getitem__(PyMapGetDel_subclassing_ExtSeqSet, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtSeqSet
    __delitem__(PyMapGetDel_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSet(ExtMapGetDel_subclassing_ExtSeqSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSet, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSet, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSet()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSet
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSet, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSet
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtSeqSet, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtSeqSet, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtSeqSet()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtSeqSet
    __getitem__(ExtSeqGetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtSeqSet
    __delitem__(ExtSeqGetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqSet()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqSet
    __getitem__(PySeqGetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqSet
    __delitem__(PySeqGetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSet(ExtSeqGetDel_subclassing_ExtSeqSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSet()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSet
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSet
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtSeqSet()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtSeqSet
    __getitem__(ExtMapGetSet_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtSeqSet
    __setitem__(ExtMapGetSet_subclassing_ExtSeqSet, i=5, value=10)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtSeqSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtSeqSet, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtSeqSet()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtSeqSet
    __getitem__(PyMapGetSet_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtSeqSet
    __setitem__(PyMapGetSet_subclassing_ExtSeqSet, i=5, value=10)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSet(ExtMapGetSet_subclassing_ExtSeqSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSet, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSet()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSet
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSet
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSet, i=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtSeqSet, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtSeqSet, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtSeqSet()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtSeqSet
    __getitem__(ExtSeqGetSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtSeqSet
    __setitem__(ExtSeqGetSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqSet()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqSet
    __getitem__(PySeqGetSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqSet
    __setitem__(PySeqGetSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSet(ExtSeqGetSet_subclassing_ExtSeqSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSet()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSet
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSet
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtSeqSet()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqSet
    __getitem__(ExtMapGetSetDel_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtSeqSet
    __setitem__(ExtMapGetSetDel_subclassing_ExtSeqSet, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqSet
    __delitem__(ExtMapGetSetDel_subclassing_ExtSeqSet, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtSeqSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtSeqSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtSeqSet, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtSeqSet()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtSeqSet
    __getitem__(PyMapGetSetDel_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtSeqSet
    __setitem__(PyMapGetSetDel_subclassing_ExtSeqSet, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtSeqSet
    __delitem__(PyMapGetSetDel_subclassing_ExtSeqSet, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSet(ExtMapGetSetDel_subclassing_ExtSeqSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSet, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSet()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSet
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSet, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSet
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSet, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSet
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSet, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtSeqSet, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtSeqSet, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtSeqSet, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtSeqSet(ExtSeqSet):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtSeqSet()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqSet
    __getitem__(ExtSeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtSeqSet
    __setitem__(ExtSeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqSet
    __delitem__(ExtSeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtSeqSet(ExtSeqSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqSet()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqSet
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqSet
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqSet
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSet(ExtSeqGetSetDel_subclassing_ExtSeqSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSet()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSet
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSet
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSet
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtSeqSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtMapDel_subclassing_ExtMapSetDel()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtMapSetDel
    __delitem__(ExtMapDel_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # ExtMapDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapSetDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapSetDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapSetDel
    __delitem__(PyMapDel_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapSetDel(ExtMapDel_subclassing_ExtMapSetDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapSetDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapSetDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapSetDel
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtMapSetDel, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtSeqDel_subclassing_ExtMapSetDel()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtMapSetDel
    __delitem__(ExtSeqDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtMapSetDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtMapSetDel
    __delitem__(PySeqDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapSetDel(ExtSeqDel_subclassing_ExtMapSetDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapSetDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapSetDel
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtMapSet_subclassing_ExtMapSetDel()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtMapSetDel
    __setitem__(ExtMapSet_subclassing_ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapSet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSetDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSetDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSetDel
    __setitem__(PyMapSet_subclassing_ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapSetDel(ExtMapSet_subclassing_ExtMapSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapSetDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapSetDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapSetDel
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtMapSetDel, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtSeqSet_subclassing_ExtMapSetDel()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtMapSetDel
    __setitem__(ExtSeqSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtMapSetDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtMapSetDel
    __setitem__(PySeqSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapSetDel(ExtSeqSet_subclassing_ExtMapSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapSetDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapSetDel
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtMapSetDel()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel_subclassing_ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel_subclassing_ExtMapSetDel, i=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel, i=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSetDel(ExtMapSetDel_subclassing_ExtMapSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSetDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSetDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSetDel
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSetDel
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapSetDel, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtMapSetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtMapSetDel, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtMapSetDel()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtMapSetDel
    __setitem__(ExtSeqSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtMapSetDel
    __delitem__(ExtSeqSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtMapSetDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtMapSetDel
    __setitem__(PySeqSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtMapSetDel
    __delitem__(PySeqSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSetDel(ExtSeqSetDel_subclassing_ExtMapSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSetDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSetDel
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSetDel
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtMapGet_subclassing_ExtMapSetDel()
    >>> obj[5]  # ExtMapGet_subclassing_ExtMapSetDel
    __getitem__(ExtMapGet_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGet_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapSetDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapSetDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapSetDel
    __getitem__(PyMapGet_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapSetDel(ExtMapGet_subclassing_ExtMapSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapSetDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapSetDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapSetDel
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtMapSetDel, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtSeqGet_subclassing_ExtMapSetDel()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtMapSetDel
    __getitem__(ExtSeqGet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGet_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # ExtSeqGet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtMapSetDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtMapSetDel
    __getitem__(PySeqGet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # PySeqGet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapSetDel(ExtSeqGet_subclassing_ExtMapSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapSetDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapSetDel
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtMapSetDel()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtMapSetDel
    __getitem__(ExtMapGetDel_subclassing_ExtMapSetDel, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtMapSetDel
    __delitem__(ExtMapGetDel_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapSetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapSetDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapSetDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapSetDel
    __getitem__(PyMapGetDel_subclassing_ExtMapSetDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapSetDel
    __delitem__(PyMapGetDel_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSetDel(ExtMapGetDel_subclassing_ExtMapSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSetDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSetDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSetDel
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSetDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSetDel
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtMapSetDel, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtMapSetDel, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtMapSetDel()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtMapSetDel
    __getitem__(ExtSeqGetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtMapSetDel
    __delitem__(ExtSeqGetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtMapSetDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtMapSetDel
    __getitem__(PySeqGetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtMapSetDel
    __delitem__(PySeqGetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSetDel(ExtSeqGetDel_subclassing_ExtMapSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSetDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSetDel
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSetDel
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapSetDel, i=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtMapSetDel()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtMapSetDel
    __getitem__(ExtMapGetSet_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtMapSetDel
    __setitem__(ExtMapGetSet_subclassing_ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapSetDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapSetDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapSetDel
    __getitem__(PyMapGetSet_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapSetDel
    __setitem__(PyMapGetSet_subclassing_ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSetDel(ExtMapGetSet_subclassing_ExtMapSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSetDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSetDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSetDel
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSetDel
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtMapSetDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtMapSetDel, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtMapSetDel()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtMapSetDel
    __getitem__(ExtSeqGetSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtMapSetDel
    __setitem__(ExtSeqGetSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtMapSetDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtMapSetDel
    __getitem__(PySeqGetSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtMapSetDel
    __setitem__(PySeqGetSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSetDel(ExtSeqGetSet_subclassing_ExtMapSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSetDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSetDel
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSetDel
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapSetDel
    __delitem__(ExtMapSetDel, i=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtMapSetDel()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtMapSetDel
    __getitem__(ExtMapGetSetDel_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtMapSetDel
    __setitem__(ExtMapGetSetDel_subclassing_ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtMapSetDel
    __delitem__(ExtMapGetSetDel_subclassing_ExtMapSetDel, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapSetDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapSetDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapSetDel
    __getitem__(PyMapGetSetDel_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapSetDel
    __setitem__(PyMapGetSetDel_subclassing_ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapSetDel
    __delitem__(PyMapGetSetDel_subclassing_ExtMapSetDel, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSetDel(ExtMapGetSetDel_subclassing_ExtMapSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSetDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSetDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSetDel
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSetDel
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSetDel
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapSetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtMapSetDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtMapSetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtMapSetDel, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtMapSetDel()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapSetDel
    __getitem__(ExtSeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtMapSetDel
    __setitem__(ExtSeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapSetDel
    __delitem__(ExtSeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtMapSetDel(ExtMapSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtMapSetDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtMapSetDel
    __getitem__(PySeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtMapSetDel
    __setitem__(PySeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtMapSetDel
    __delitem__(PySeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSetDel(ExtSeqGetSetDel_subclassing_ExtMapSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSetDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSetDel
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSetDel
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSetDel
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtMapSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtMapDel_subclassing_ExtSeqSetDel()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtSeqSetDel
    __delitem__(ExtMapDel_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # ExtMapDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtSeqSetDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtSeqSetDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtSeqSetDel
    __delitem__(PyMapDel_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqSetDel(ExtMapDel_subclassing_ExtSeqSetDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqSetDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqSetDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqSetDel
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtSeqSetDel, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtSeqDel_subclassing_ExtSeqSetDel()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqSetDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqSetDel
    __delitem__(PySeqDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqSetDel(ExtSeqDel_subclassing_ExtSeqSetDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqSetDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqSetDel
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtMapSet_subclassing_ExtSeqSetDel()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtSeqSetDel
    __setitem__(ExtMapSet_subclassing_ExtSeqSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapSet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtSeqSetDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtSeqSetDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtSeqSetDel
    __setitem__(PyMapSet_subclassing_ExtSeqSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqSetDel(ExtMapSet_subclassing_ExtSeqSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqSetDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqSetDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqSetDel
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtSeqSetDel, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtSeqSet_subclassing_ExtSeqSetDel()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSetDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSetDel
    __setitem__(PySeqSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqSetDel(ExtSeqSet_subclassing_ExtSeqSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqSetDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqSetDel
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtSeqSetDel()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtSeqSetDel
    __setitem__(ExtMapSetDel_subclassing_ExtSeqSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtSeqSetDel
    __delitem__(ExtMapSetDel_subclassing_ExtSeqSetDel, i=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtSeqSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtSeqSetDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtSeqSetDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtSeqSetDel
    __setitem__(PyMapSetDel_subclassing_ExtSeqSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtSeqSetDel
    __delitem__(PyMapSetDel_subclassing_ExtSeqSetDel, i=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSetDel(ExtMapSetDel_subclassing_ExtSeqSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSetDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSetDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSetDel
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSetDel
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqSetDel, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtSeqSetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtSeqSetDel, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtSeqSetDel()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel_subclassing_ExtSeqSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSetDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSetDel
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSetDel
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtMapGet_subclassing_ExtSeqSetDel()
    >>> obj[5]  # ExtMapGet_subclassing_ExtSeqSetDel
    __getitem__(ExtMapGet_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGet_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtMapGet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtSeqSetDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtSeqSetDel
    __getitem__(PyMapGet_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PyMapGet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqSetDel(ExtMapGet_subclassing_ExtSeqSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqSetDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqSetDel
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtSeqSetDel, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtSeqGet_subclassing_ExtSeqSetDel()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtSeqSetDel
    __getitem__(ExtSeqGet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGet_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqSetDel
    __getitem__(PySeqGet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqSetDel(ExtSeqGet_subclassing_ExtSeqSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqSetDel
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtSeqSetDel()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtSeqSetDel
    __getitem__(ExtMapGetDel_subclassing_ExtSeqSetDel, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtSeqSetDel
    __delitem__(ExtMapGetDel_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtSeqSetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtSeqSetDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtSeqSetDel
    __getitem__(PyMapGetDel_subclassing_ExtSeqSetDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtSeqSetDel
    __delitem__(PyMapGetDel_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSetDel(ExtMapGetDel_subclassing_ExtSeqSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSetDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSetDel
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSetDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSetDel
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtSeqSetDel, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtSeqSetDel, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtSeqSetDel()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtSeqSetDel
    __getitem__(ExtSeqGetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqGetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqSetDel
    __getitem__(PySeqGetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqSetDel
    __delitem__(PySeqGetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSetDel(ExtSeqGetDel_subclassing_ExtSeqSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSetDel
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSetDel
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtSeqSetDel()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtSeqSetDel
    __getitem__(ExtMapGetSet_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtSeqSetDel
    __setitem__(ExtMapGetSet_subclassing_ExtSeqSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtSeqSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtSeqSetDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtSeqSetDel
    __getitem__(PyMapGetSet_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtSeqSetDel
    __setitem__(PyMapGetSet_subclassing_ExtSeqSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSetDel(ExtMapGetSet_subclassing_ExtSeqSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSetDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSetDel
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSetDel
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtSeqSetDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtSeqSetDel, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtSeqSetDel()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtSeqSetDel
    __getitem__(ExtSeqGetSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqGetSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqSetDel
    __getitem__(PySeqGetSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqSetDel
    __setitem__(PySeqGetSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSetDel(ExtSeqGetSet_subclassing_ExtSeqSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSetDel
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSetDel
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqSetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtSeqSetDel()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqSetDel
    __getitem__(ExtMapGetSetDel_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtSeqSetDel
    __setitem__(ExtMapGetSetDel_subclassing_ExtSeqSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqSetDel
    __delitem__(ExtMapGetSetDel_subclassing_ExtSeqSetDel, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtSeqSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtSeqSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtSeqSetDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtSeqSetDel
    __getitem__(PyMapGetSetDel_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtSeqSetDel
    __setitem__(PyMapGetSetDel_subclassing_ExtSeqSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtSeqSetDel
    __delitem__(PyMapGetSetDel_subclassing_ExtSeqSetDel, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSetDel(ExtMapGetSetDel_subclassing_ExtSeqSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSetDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSetDel
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSetDel
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSetDel
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqSetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtSeqSetDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtSeqSetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtSeqSetDel, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtSeqSetDel()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqSetDel
    __getitem__(ExtSeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtSeqSetDel
    __setitem__(ExtSeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqSetDel
    __delitem__(ExtSeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtSeqSetDel(ExtSeqSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqSetDel
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqSetDel
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqSetDel
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSetDel(ExtSeqGetSetDel_subclassing_ExtSeqSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSetDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSetDel
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSetDel
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSetDel
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtSeqSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtMapDel_subclassing_ExtMapGet()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtMapGet
    __delitem__(ExtMapDel_subclassing_ExtMapGet, i=5)
    >>> obj[5]  # ExtMapDel_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtMapGet(ExtMapGet):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapGet, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapGet()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapGet
    __delitem__(PyMapDel_subclassing_ExtMapGet, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGet(ExtMapDel_subclassing_ExtMapGet):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGet, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGet()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGet
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGet, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtMapGet, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtSeqDel_subclassing_ExtMapGet()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtMapGet
    __delitem__(ExtSeqDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqDel_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtMapGet(ExtMapGet):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtMapGet()
    >>> del obj[5]  # PySeqDel_subclassing_ExtMapGet
    __delitem__(PySeqDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGet(ExtSeqDel_subclassing_ExtMapGet):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGet()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGet
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtMapSet_subclassing_ExtMapGet()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtMapGet
    __setitem__(ExtMapSet_subclassing_ExtMapGet, i=5, value=10)
    >>> obj[5]  # ExtMapSet_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtMapGet(ExtMapGet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapGet, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapGet()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapGet
    __setitem__(PyMapSet_subclassing_ExtMapGet, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGet(ExtMapSet_subclassing_ExtMapGet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGet, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGet()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGet
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGet, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtMapGet, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtSeqSet_subclassing_ExtMapGet()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtMapGet
    __setitem__(ExtSeqSet_subclassing_ExtMapGet, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # ExtSeqSet_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtMapGet(ExtMapGet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtMapGet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtMapGet()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtMapGet
    __setitem__(PySeqSet_subclassing_ExtMapGet, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGet(ExtSeqSet_subclassing_ExtMapGet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGet()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGet
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGet, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtMapGet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtMapGet()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtMapGet
    __setitem__(ExtMapSetDel_subclassing_ExtMapGet, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtMapGet
    __delitem__(ExtMapSetDel_subclassing_ExtMapGet, i=5)
    >>> obj[5]  # ExtMapSetDel_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtMapGet(ExtMapGet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapGet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapGet, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapGet()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapGet
    __setitem__(PyMapSetDel_subclassing_ExtMapGet, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapGet
    __delitem__(PyMapSetDel_subclassing_ExtMapGet, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGet(ExtMapSetDel_subclassing_ExtMapGet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGet, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGet()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGet
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGet, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGet
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGet, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtMapGet, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtMapGet, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtMapGet()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtMapGet
    __setitem__(ExtSeqSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtMapGet
    __delitem__(ExtSeqSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqSetDel_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtMapGet(ExtMapGet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtMapGet()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtMapGet
    __setitem__(PySeqSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtMapGet
    __delitem__(PySeqSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGet(ExtSeqSetDel_subclassing_ExtMapGet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGet()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGet
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGet
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGet
    __getitem__(ExtMapGet, i=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtMapGet_subclassing_ExtMapGet()
    >>> obj[5]  # ExtMapGet_subclassing_ExtMapGet
    __getitem__(ExtMapGet_subclassing_ExtMapGet, i=5)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtMapGet(ExtMapGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet
    __getitem__(PyMapGet_subclassing_ExtMapGet, i=5)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGet(ExtMapGet_subclassing_ExtMapGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGet, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGet()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGet
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGet, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtMapGet, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtSeqGet_subclassing_ExtMapGet()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtMapGet
    __getitem__(ExtSeqGet_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtMapGet(ExtMapGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtMapGet()
    >>> obj[5]  # PySeqGet_subclassing_ExtMapGet
    __getitem__(PySeqGet_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGet(ExtSeqGet_subclassing_ExtMapGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGet()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGet
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtMapGet()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtMapGet
    __getitem__(ExtMapGetDel_subclassing_ExtMapGet, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtMapGet
    __delitem__(ExtMapGetDel_subclassing_ExtMapGet, i=5)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtMapGet(ExtMapGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGet, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGet, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGet()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGet
    __getitem__(PyMapGetDel_subclassing_ExtMapGet, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGet
    __delitem__(PyMapGetDel_subclassing_ExtMapGet, i=5)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGet(ExtMapGetDel_subclassing_ExtMapGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGet, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGet, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGet()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGet
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGet, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGet
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGet, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtMapGet, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtMapGet, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtMapGet()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtMapGet
    __getitem__(ExtSeqGetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtMapGet
    __delitem__(ExtSeqGetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtMapGet(ExtMapGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtMapGet()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtMapGet
    __getitem__(PySeqGetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtMapGet
    __delitem__(PySeqGetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGet(ExtSeqGetDel_subclassing_ExtMapGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGet()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGet
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGet
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtMapGet()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtMapGet
    __getitem__(ExtMapGetSet_subclassing_ExtMapGet, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtMapGet
    __setitem__(ExtMapGetSet_subclassing_ExtMapGet, i=5, value=10)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtMapGet(ExtMapGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGet, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGet()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGet
    __getitem__(PyMapGetSet_subclassing_ExtMapGet, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGet
    __setitem__(PyMapGetSet_subclassing_ExtMapGet, i=5, value=10)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGet(ExtMapGetSet_subclassing_ExtMapGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGet, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGet()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGet
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGet, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGet
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGet, i=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtMapGet, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtMapGet, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtMapGet()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtMapGet
    __getitem__(ExtSeqGetSet_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtMapGet
    __setitem__(ExtSeqGetSet_subclassing_ExtMapGet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtMapGet(ExtMapGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtMapGet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtMapGet()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtMapGet
    __getitem__(PySeqGetSet_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtMapGet
    __setitem__(PySeqGetSet_subclassing_ExtMapGet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGet(ExtSeqGetSet_subclassing_ExtMapGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGet()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGet
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGet
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtMapGet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtMapGet()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtMapGet
    __getitem__(ExtMapGetSetDel_subclassing_ExtMapGet, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtMapGet
    __setitem__(ExtMapGetSetDel_subclassing_ExtMapGet, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtMapGet
    __delitem__(ExtMapGetSetDel_subclassing_ExtMapGet, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtMapGet(ExtMapGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGet, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGet()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGet
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGet, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGet
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGet, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGet
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGet, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGet(ExtMapGetSetDel_subclassing_ExtMapGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGet, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGet()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGet
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGet, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGet
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGet, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGet
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGet, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtMapGet, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtMapGet, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtMapGet, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtMapGet(ExtMapGet):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtMapGet()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapGet
    __getitem__(ExtSeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtMapGet
    __setitem__(ExtSeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapGet
    __delitem__(ExtSeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtMapGet(ExtMapGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtMapGet()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtMapGet
    __getitem__(PySeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtMapGet
    __setitem__(PySeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtMapGet
    __delitem__(PySeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGet(ExtSeqGetSetDel_subclassing_ExtMapGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGet()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGet
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGet
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGet
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtMapGet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtMapDel_subclassing_ExtSeqGet()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtSeqGet
    __delitem__(ExtMapDel_subclassing_ExtSeqGet, i=5)
    >>> obj[5]  # ExtMapDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtSeqGet, i={i})")

    >>> obj = PyMapDel_subclassing_ExtSeqGet()
    >>> del obj[5]  # PyMapDel_subclassing_ExtSeqGet
    __delitem__(PyMapDel_subclassing_ExtSeqGet, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGet(ExtMapDel_subclassing_ExtSeqGet):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGet, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGet()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGet
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGet, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtSeqGet, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtSeqDel_subclassing_ExtSeqGet()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtSeqGet
    __delitem__(ExtSeqDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqGet()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqGet
    __delitem__(PySeqDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGet(ExtSeqDel_subclassing_ExtSeqGet):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGet()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGet
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtMapSet_subclassing_ExtSeqGet()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtSeqGet
    __setitem__(ExtMapSet_subclassing_ExtSeqGet, i=5, value=10)
    >>> obj[5]  # ExtMapSet_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtSeqGet, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtSeqGet()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtSeqGet
    __setitem__(PyMapSet_subclassing_ExtSeqGet, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGet(ExtMapSet_subclassing_ExtSeqGet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGet, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGet()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGet
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGet, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtSeqGet, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtSeqSet_subclassing_ExtSeqGet()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtSeqGet
    __setitem__(ExtSeqSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # ExtSeqSet_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqGet()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqGet
    __setitem__(PySeqSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGet(ExtSeqSet_subclassing_ExtSeqGet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGet()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGet
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtSeqGet()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtSeqGet
    __setitem__(ExtMapSetDel_subclassing_ExtSeqGet, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtSeqGet
    __delitem__(ExtMapSetDel_subclassing_ExtSeqGet, i=5)
    >>> obj[5]  # ExtMapSetDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtSeqGet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtSeqGet, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtSeqGet()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtSeqGet
    __setitem__(PyMapSetDel_subclassing_ExtSeqGet, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtSeqGet
    __delitem__(PyMapSetDel_subclassing_ExtSeqGet, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGet(ExtMapSetDel_subclassing_ExtSeqGet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGet, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGet()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGet
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGet, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGet
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGet, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtSeqGet, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtSeqGet, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtSeqGet()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtSeqGet
    __setitem__(ExtSeqSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtSeqGet
    __delitem__(ExtSeqSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqSetDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqGet()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqGet
    __setitem__(PySeqSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqGet
    __delitem__(PySeqSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGet(ExtSeqSetDel_subclassing_ExtSeqGet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGet()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGet
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGet
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtMapGet_subclassing_ExtSeqGet()
    >>> obj[5]  # ExtMapGet_subclassing_ExtSeqGet
    __getitem__(ExtMapGet_subclassing_ExtSeqGet, i=5)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtSeqGet, i={i})")

    >>> obj = PyMapGet_subclassing_ExtSeqGet()
    >>> obj[5]  # PyMapGet_subclassing_ExtSeqGet
    __getitem__(PyMapGet_subclassing_ExtSeqGet, i=5)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGet(ExtMapGet_subclassing_ExtSeqGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGet, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGet()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGet
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGet, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtSeqGet, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtSeqGet_subclassing_ExtSeqGet()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtSeqGet
    __getitem__(ExtSeqGet_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet
    __getitem__(PySeqGet_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGet(ExtSeqGet_subclassing_ExtSeqGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGet()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGet
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtSeqGet()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtSeqGet
    __getitem__(ExtMapGetDel_subclassing_ExtSeqGet, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtSeqGet
    __delitem__(ExtMapGetDel_subclassing_ExtSeqGet, i=5)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtSeqGet, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtSeqGet, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtSeqGet()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtSeqGet
    __getitem__(PyMapGetDel_subclassing_ExtSeqGet, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtSeqGet
    __delitem__(PyMapGetDel_subclassing_ExtSeqGet, i=5)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGet(ExtMapGetDel_subclassing_ExtSeqGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGet, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGet, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGet()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGet
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGet, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGet
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGet, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtSeqGet, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtSeqGet, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtSeqGet()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtSeqGet
    __delitem__(ExtSeqGetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGet()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGet
    __getitem__(PySeqGetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGet
    __delitem__(PySeqGetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGet(ExtSeqGetDel_subclassing_ExtSeqGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGet()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGet
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGet
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtSeqGet()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtSeqGet
    __getitem__(ExtMapGetSet_subclassing_ExtSeqGet, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtSeqGet
    __setitem__(ExtMapGetSet_subclassing_ExtSeqGet, i=5, value=10)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtSeqGet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtSeqGet, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtSeqGet()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtSeqGet
    __getitem__(PyMapGetSet_subclassing_ExtSeqGet, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtSeqGet
    __setitem__(PyMapGetSet_subclassing_ExtSeqGet, i=5, value=10)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGet(ExtMapGetSet_subclassing_ExtSeqGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGet, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGet()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGet
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGet, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGet
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGet, i=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtSeqGet, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtSeqGet, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtSeqGet()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtSeqGet
    __getitem__(ExtSeqGetSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtSeqGet
    __setitem__(ExtSeqGetSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGet()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGet
    __getitem__(PySeqGetSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGet
    __setitem__(PySeqGetSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGet(ExtSeqGetSet_subclassing_ExtSeqGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGet()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGet
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGet
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtSeqGet()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqGet
    __getitem__(ExtMapGetSetDel_subclassing_ExtSeqGet, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtSeqGet
    __setitem__(ExtMapGetSetDel_subclassing_ExtSeqGet, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqGet
    __delitem__(ExtMapGetSetDel_subclassing_ExtSeqGet, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtSeqGet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtSeqGet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtSeqGet, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtSeqGet()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtSeqGet
    __getitem__(PyMapGetSetDel_subclassing_ExtSeqGet, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtSeqGet
    __setitem__(PyMapGetSetDel_subclassing_ExtSeqGet, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtSeqGet
    __delitem__(PyMapGetSetDel_subclassing_ExtSeqGet, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGet(ExtMapGetSetDel_subclassing_ExtSeqGet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGet, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGet()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGet
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGet, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGet
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGet, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGet
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGet, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtSeqGet, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtSeqGet, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtSeqGet, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtSeqGet(ExtSeqGet):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtSeqGet()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqGet
    __getitem__(ExtSeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtSeqGet
    __setitem__(ExtSeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqGet
    __delitem__(ExtSeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtSeqGet(ExtSeqGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGet()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGet
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGet
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGet
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGet(ExtSeqGetSetDel_subclassing_ExtSeqGet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGet()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGet
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGet
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGet
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtSeqGet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtMapDel_subclassing_ExtMapGetDel()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtMapGetDel
    __delitem__(ExtMapDel_subclassing_ExtMapGetDel, i=5)
    >>> obj[5]  # ExtMapDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapGetDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapGetDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapGetDel
    __delitem__(PyMapDel_subclassing_ExtMapGetDel, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetDel(ExtMapDel_subclassing_ExtMapGetDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetDel
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetDel, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtMapGetDel, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtSeqDel_subclassing_ExtMapGetDel()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtMapGetDel
    __delitem__(ExtSeqDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtMapGetDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtMapGetDel
    __delitem__(PySeqDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetDel(ExtSeqDel_subclassing_ExtMapGetDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetDel
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtMapSet_subclassing_ExtMapGetDel()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtMapGetDel
    __setitem__(ExtMapSet_subclassing_ExtMapGetDel, i=5, value=10)
    >>> obj[5]  # ExtMapSet_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    >>> del obj[5]  # ExtMapSet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapGetDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapGetDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapGetDel
    __setitem__(PyMapSet_subclassing_ExtMapGetDel, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    >>> del obj[5]  # PyMapSet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetDel(ExtMapSet_subclassing_ExtMapGetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetDel
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetDel, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    >>> del obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtMapGetDel, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtSeqSet_subclassing_ExtMapGetDel()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtMapGetDel
    __setitem__(ExtSeqSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # ExtSeqSet_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    >>> del obj[5]  # ExtSeqSet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtMapGetDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtMapGetDel
    __setitem__(PySeqSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    >>> del obj[5]  # PySeqSet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetDel(ExtSeqSet_subclassing_ExtMapGetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetDel
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    >>> del obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtMapGetDel()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtMapGetDel
    __setitem__(ExtMapSetDel_subclassing_ExtMapGetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtMapGetDel
    __delitem__(ExtMapSetDel_subclassing_ExtMapGetDel, i=5)
    >>> obj[5]  # ExtMapSetDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapGetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapGetDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapGetDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapGetDel
    __setitem__(PyMapSetDel_subclassing_ExtMapGetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapGetDel
    __delitem__(PyMapSetDel_subclassing_ExtMapGetDel, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetDel(ExtMapSetDel_subclassing_ExtMapGetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetDel
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetDel
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetDel, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtMapGetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtMapGetDel, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtMapGetDel()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtMapGetDel
    __setitem__(ExtSeqSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtMapGetDel
    __delitem__(ExtSeqSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqSetDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtMapGetDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtMapGetDel
    __setitem__(PySeqSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtMapGetDel
    __delitem__(PySeqSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetDel(ExtSeqSetDel_subclassing_ExtMapGetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetDel
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetDel
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel, i=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtMapGet_subclassing_ExtMapGetDel()
    >>> obj[5]  # ExtMapGet_subclassing_ExtMapGetDel
    __getitem__(ExtMapGet_subclassing_ExtMapGetDel, i=5)
    >>> del obj[5]  # ExtMapGet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGetDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGetDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGetDel
    __getitem__(PyMapGet_subclassing_ExtMapGetDel, i=5)
    >>> del obj[5]  # PyMapGet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetDel(ExtMapGet_subclassing_ExtMapGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetDel
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetDel, i=5)
    >>> del obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtMapGetDel, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtSeqGet_subclassing_ExtMapGetDel()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtMapGetDel
    __getitem__(ExtSeqGet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtMapGetDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtMapGetDel
    __getitem__(PySeqGet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetDel(ExtSeqGet_subclassing_ExtMapGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetDel
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtMapGetDel()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetDel_subclassing_ExtMapGetDel, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel_subclassing_ExtMapGetDel, i=5)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel, i=5)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetDel(ExtMapGetDel_subclassing_ExtMapGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetDel
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetDel
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtMapGetDel, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtMapGetDel, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtMapGetDel()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtMapGetDel
    __getitem__(ExtSeqGetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtMapGetDel
    __delitem__(ExtSeqGetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtMapGetDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtMapGetDel
    __getitem__(PySeqGetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtMapGetDel
    __delitem__(PySeqGetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetDel(ExtSeqGetDel_subclassing_ExtMapGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetDel
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetDel
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtMapGetDel()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetSet_subclassing_ExtMapGetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtMapGetDel
    __setitem__(ExtMapGetSet_subclassing_ExtMapGetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetDel
    __getitem__(PyMapGetSet_subclassing_ExtMapGetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetDel
    __setitem__(PyMapGetSet_subclassing_ExtMapGetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetDel(ExtMapGetSet_subclassing_ExtMapGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetDel
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetDel
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtMapGetDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtMapGetDel, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtMapGetDel()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtMapGetDel
    __getitem__(ExtSeqGetSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtMapGetDel
    __setitem__(ExtSeqGetSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtMapGetDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtMapGetDel
    __getitem__(PySeqGetSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtMapGetDel
    __setitem__(PySeqGetSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetDel(ExtSeqGetSet_subclassing_ExtMapGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetDel
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetDel
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetDel, i=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtMapGetDel()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtMapGetDel
    __getitem__(ExtMapGetSetDel_subclassing_ExtMapGetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtMapGetDel
    __setitem__(ExtMapGetSetDel_subclassing_ExtMapGetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtMapGetDel
    __delitem__(ExtMapGetSetDel_subclassing_ExtMapGetDel, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetDel
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetDel
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetDel
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetDel, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetDel(ExtMapGetSetDel_subclassing_ExtMapGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetDel
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetDel
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetDel
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtMapGetDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtMapGetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtMapGetDel, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtMapGetDel()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapGetDel
    __getitem__(ExtSeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtMapGetDel
    __setitem__(ExtSeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapGetDel
    __delitem__(ExtSeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtMapGetDel(ExtMapGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtMapGetDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtMapGetDel
    __getitem__(PySeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtMapGetDel
    __setitem__(PySeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtMapGetDel
    __delitem__(PySeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetDel(ExtSeqGetSetDel_subclassing_ExtMapGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetDel
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetDel
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetDel
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtMapGetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtMapDel_subclassing_ExtSeqGetDel()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtSeqGetDel
    __delitem__(ExtMapDel_subclassing_ExtSeqGetDel, i=5)
    >>> obj[5]  # ExtMapDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtSeqGetDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtSeqGetDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtSeqGetDel
    __delitem__(PyMapDel_subclassing_ExtSeqGetDel, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetDel(ExtMapDel_subclassing_ExtSeqGetDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetDel
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetDel, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtSeqGetDel, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtSeqDel_subclassing_ExtSeqGetDel()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqGetDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqGetDel
    __delitem__(PySeqDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetDel(ExtSeqDel_subclassing_ExtSeqGetDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetDel
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtMapSet_subclassing_ExtSeqGetDel()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtSeqGetDel
    __setitem__(ExtMapSet_subclassing_ExtSeqGetDel, i=5, value=10)
    >>> obj[5]  # ExtMapSet_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtMapSet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtSeqGetDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtSeqGetDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtSeqGetDel
    __setitem__(PyMapSet_subclassing_ExtSeqGetDel, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PyMapSet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetDel(ExtMapSet_subclassing_ExtSeqGetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetDel
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetDel, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtSeqGetDel, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtSeqSet_subclassing_ExtSeqGetDel()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtSeqGetDel
    __setitem__(ExtSeqSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # ExtSeqSet_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqSet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqGetDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqGetDel
    __setitem__(PySeqSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqSet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetDel(ExtSeqSet_subclassing_ExtSeqGetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetDel
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtSeqGetDel()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtSeqGetDel
    __setitem__(ExtMapSetDel_subclassing_ExtSeqGetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtSeqGetDel
    __delitem__(ExtMapSetDel_subclassing_ExtSeqGetDel, i=5)
    >>> obj[5]  # ExtMapSetDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtSeqGetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtSeqGetDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtSeqGetDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtSeqGetDel
    __setitem__(PyMapSetDel_subclassing_ExtSeqGetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtSeqGetDel
    __delitem__(PyMapSetDel_subclassing_ExtSeqGetDel, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetDel(ExtMapSetDel_subclassing_ExtSeqGetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetDel
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetDel
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetDel, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtSeqGetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtSeqGetDel, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtSeqGetDel()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtSeqGetDel
    __setitem__(ExtSeqSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqSetDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqGetDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqGetDel
    __setitem__(PySeqSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqGetDel
    __delitem__(PySeqSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetDel(ExtSeqSetDel_subclassing_ExtSeqGetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetDel
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetDel
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtMapGet_subclassing_ExtSeqGetDel()
    >>> obj[5]  # ExtMapGet_subclassing_ExtSeqGetDel
    __getitem__(ExtMapGet_subclassing_ExtSeqGetDel, i=5)
    >>> del obj[5]  # ExtMapGet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtSeqGetDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtSeqGetDel
    __getitem__(PyMapGet_subclassing_ExtSeqGetDel, i=5)
    >>> del obj[5]  # PyMapGet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetDel(ExtMapGet_subclassing_ExtSeqGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetDel
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetDel, i=5)
    >>> del obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtSeqGetDel, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtSeqGet_subclassing_ExtSeqGetDel()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGetDel
    __getitem__(PySeqGet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetDel(ExtSeqGet_subclassing_ExtSeqGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetDel
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtSeqGetDel()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtSeqGetDel
    __getitem__(ExtMapGetDel_subclassing_ExtSeqGetDel, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtSeqGetDel
    __delitem__(ExtMapGetDel_subclassing_ExtSeqGetDel, i=5)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtSeqGetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtSeqGetDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtSeqGetDel
    __getitem__(PyMapGetDel_subclassing_ExtSeqGetDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtSeqGetDel
    __delitem__(PyMapGetDel_subclassing_ExtSeqGetDel, i=5)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetDel(ExtMapGetDel_subclassing_ExtSeqGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetDel
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetDel
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtSeqGetDel, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtSeqGetDel, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtSeqGetDel()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel_subclassing_ExtSeqGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetDel
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetDel
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtSeqGetDel()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtSeqGetDel
    __getitem__(ExtMapGetSet_subclassing_ExtSeqGetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtSeqGetDel
    __setitem__(ExtMapGetSet_subclassing_ExtSeqGetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtSeqGetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtSeqGetDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtSeqGetDel
    __getitem__(PyMapGetSet_subclassing_ExtSeqGetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtSeqGetDel
    __setitem__(PyMapGetSet_subclassing_ExtSeqGetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetDel(ExtMapGetSet_subclassing_ExtSeqGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetDel
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetDel
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtSeqGetDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtSeqGetDel, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtSeqGetDel()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtSeqGetDel
    __setitem__(ExtSeqGetSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetDel
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetDel
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetDel(ExtSeqGetSet_subclassing_ExtSeqGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetDel
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetDel
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtSeqGetDel()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqGetDel
    __getitem__(ExtMapGetSetDel_subclassing_ExtSeqGetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtSeqGetDel
    __setitem__(ExtMapGetSetDel_subclassing_ExtSeqGetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqGetDel
    __delitem__(ExtMapGetSetDel_subclassing_ExtSeqGetDel, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtSeqGetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtSeqGetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtSeqGetDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtSeqGetDel
    __getitem__(PyMapGetSetDel_subclassing_ExtSeqGetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtSeqGetDel
    __setitem__(PyMapGetSetDel_subclassing_ExtSeqGetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtSeqGetDel
    __delitem__(PyMapGetSetDel_subclassing_ExtSeqGetDel, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetDel(ExtMapGetSetDel_subclassing_ExtSeqGetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetDel
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetDel
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetDel
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtSeqGetDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtSeqGetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtSeqGetDel, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtSeqGetDel()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqGetDel
    __getitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtSeqGetDel
    __setitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqGetDel
    __delitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetDel(ExtSeqGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetDel
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetDel
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetDel
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetDel(ExtSeqGetSetDel_subclassing_ExtSeqGetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetDel
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetDel
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetDel
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtMapDel_subclassing_ExtMapGetSet()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtMapGetSet
    __delitem__(ExtMapDel_subclassing_ExtMapGetSet, i=5)
    >>> obj[5]  # ExtMapDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    >>> obj[5] = 10  # ExtMapDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapGetSet, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapGetSet()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapGetSet
    __delitem__(PyMapDel_subclassing_ExtMapGetSet, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSet(ExtMapDel_subclassing_ExtMapGetSet):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSet, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSet()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSet
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSet, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtMapGetSet, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtSeqDel_subclassing_ExtMapGetSet()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtMapGetSet
    __delitem__(ExtSeqDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    >>> obj[5] = 10  # ExtSeqDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtMapGetSet()
    >>> del obj[5]  # PySeqDel_subclassing_ExtMapGetSet
    __delitem__(PySeqDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSet(ExtSeqDel_subclassing_ExtMapGetSet):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSet()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSet
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtMapSet_subclassing_ExtMapGetSet()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtMapGetSet
    __setitem__(ExtMapSet_subclassing_ExtMapGetSet, i=5, value=10)
    >>> obj[5]  # ExtMapSet_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapGetSet, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapGetSet()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapGetSet
    __setitem__(PyMapSet_subclassing_ExtMapGetSet, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetSet(ExtMapSet_subclassing_ExtMapGetSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetSet, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetSet()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetSet
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetSet, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtMapGetSet, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtSeqSet_subclassing_ExtMapGetSet()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtMapGetSet
    __setitem__(ExtSeqSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # ExtSeqSet_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtMapGetSet()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtMapGetSet
    __setitem__(PySeqSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetSet(ExtSeqSet_subclassing_ExtMapGetSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetSet()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetSet
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtMapGetSet()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapSetDel_subclassing_ExtMapGetSet, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtMapGetSet
    __delitem__(ExtMapSetDel_subclassing_ExtMapGetSet, i=5)
    >>> obj[5]  # ExtMapSetDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapGetSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapGetSet, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapGetSet()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapGetSet
    __setitem__(PyMapSetDel_subclassing_ExtMapGetSet, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapGetSet
    __delitem__(PyMapSetDel_subclassing_ExtMapGetSet, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSet(ExtMapSetDel_subclassing_ExtMapGetSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSet, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSet()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSet
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSet, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSet
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSet, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtMapGetSet, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtMapGetSet, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtMapGetSet()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtMapGetSet
    __setitem__(ExtSeqSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtMapGetSet
    __delitem__(ExtSeqSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqSetDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtMapGetSet()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtMapGetSet
    __setitem__(PySeqSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtMapGetSet
    __delitem__(PySeqSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSet(ExtSeqSetDel_subclassing_ExtMapGetSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSet()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSet
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSet
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet, i=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtMapGet_subclassing_ExtMapGetSet()
    >>> obj[5]  # ExtMapGet_subclassing_ExtMapGetSet
    __getitem__(ExtMapGet_subclassing_ExtMapGetSet, i=5)
    >>> obj[5] = 10  # ExtMapGet_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGetSet, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGetSet()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGetSet
    __getitem__(PyMapGet_subclassing_ExtMapGetSet, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetSet(ExtMapGet_subclassing_ExtMapGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetSet, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetSet()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetSet
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetSet, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtMapGetSet, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtSeqGet_subclassing_ExtMapGetSet()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtMapGetSet
    __getitem__(ExtSeqGet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGet_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtMapGetSet()
    >>> obj[5]  # PySeqGet_subclassing_ExtMapGetSet
    __getitem__(PySeqGet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetSet(ExtSeqGet_subclassing_ExtMapGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetSet()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetSet
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtMapGetSet()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetDel_subclassing_ExtMapGetSet, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtMapGetSet
    __delitem__(ExtMapGetDel_subclassing_ExtMapGetSet, i=5)
    >>> obj[5] = 10  # ExtMapGetDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetSet, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetSet, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetSet()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetSet
    __getitem__(PyMapGetDel_subclassing_ExtMapGetSet, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetSet
    __delitem__(PyMapGetDel_subclassing_ExtMapGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSet(ExtMapGetDel_subclassing_ExtMapGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSet, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSet, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSet()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSet
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSet, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSet
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtMapGetSet, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtMapGetSet, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtMapGetSet()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtMapGetSet
    __getitem__(ExtSeqGetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtMapGetSet
    __delitem__(ExtSeqGetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtMapGetSet()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtMapGetSet
    __getitem__(PySeqGetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtMapGetSet
    __delitem__(PySeqGetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSet(ExtSeqGetDel_subclassing_ExtMapGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSet()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSet
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSet
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet, i=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtMapGetSet()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSet_subclassing_ExtMapGetSet, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSet_subclassing_ExtMapGetSet, i=5, value=10)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet, i=5, value=10)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSet(ExtMapGetSet_subclassing_ExtMapGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSet, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSet()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSet
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSet
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSet, i=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtMapGetSet, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtMapGetSet, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtMapGetSet()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtMapGetSet
    __getitem__(ExtSeqGetSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtMapGetSet
    __setitem__(ExtSeqGetSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtMapGetSet()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtMapGetSet
    __getitem__(PySeqGetSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtMapGetSet
    __setitem__(PySeqGetSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSet(ExtSeqGetSet_subclassing_ExtMapGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSet()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSet
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSet
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtMapGetSet()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtMapGetSet
    __getitem__(ExtMapGetSetDel_subclassing_ExtMapGetSet, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtMapGetSet
    __setitem__(ExtMapGetSetDel_subclassing_ExtMapGetSet, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtMapGetSet
    __delitem__(ExtMapGetSetDel_subclassing_ExtMapGetSet, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSet, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSet()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSet
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSet
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSet, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSet
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSet, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSet(ExtMapGetSetDel_subclassing_ExtMapGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSet, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSet()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSet
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSet
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSet, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSet
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSet, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtMapGetSet, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtMapGetSet, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtMapGetSet, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtMapGetSet()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapGetSet
    __getitem__(ExtSeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtMapGetSet
    __setitem__(ExtSeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapGetSet
    __delitem__(ExtSeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtMapGetSet(ExtMapGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtMapGetSet()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtMapGetSet
    __getitem__(PySeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtMapGetSet
    __setitem__(PySeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtMapGetSet
    __delitem__(PySeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSet(ExtSeqGetSetDel_subclassing_ExtMapGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSet()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSet
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSet
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSet
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtMapGetSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtMapDel_subclassing_ExtSeqGetSet()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtSeqGetSet
    __delitem__(ExtMapDel_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5]  # ExtMapDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtMapDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtSeqGetSet, i={i})")

    >>> obj = PyMapDel_subclassing_ExtSeqGetSet()
    >>> del obj[5]  # PyMapDel_subclassing_ExtSeqGetSet
    __delitem__(PyMapDel_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSet(ExtMapDel_subclassing_ExtSeqGetSet):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSet, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSet()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSet
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtSeqGetSet, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtSeqDel_subclassing_ExtSeqGetSet()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtSeqGetSet
    __delitem__(ExtSeqDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqGetSet()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqGetSet
    __delitem__(PySeqDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSet(ExtSeqDel_subclassing_ExtSeqGetSet):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSet()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSet
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtMapSet_subclassing_ExtSeqGetSet()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtSeqGetSet
    __setitem__(ExtMapSet_subclassing_ExtSeqGetSet, i=5, value=10)
    >>> obj[5]  # ExtMapSet_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtSeqGetSet, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtSeqGetSet()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtSeqGetSet
    __setitem__(PyMapSet_subclassing_ExtSeqGetSet, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetSet(ExtMapSet_subclassing_ExtSeqGetSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetSet, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetSet()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetSet
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetSet, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtSeqGetSet, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtSeqSet_subclassing_ExtSeqGetSet()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # ExtSeqSet_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqGetSet()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqGetSet
    __setitem__(PySeqSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetSet(ExtSeqSet_subclassing_ExtSeqGetSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetSet()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetSet
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtSeqGetSet()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtSeqGetSet
    __setitem__(ExtMapSetDel_subclassing_ExtSeqGetSet, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtSeqGetSet
    __delitem__(ExtMapSetDel_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5]  # ExtMapSetDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtSeqGetSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtSeqGetSet, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtSeqGetSet()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtSeqGetSet
    __setitem__(PyMapSetDel_subclassing_ExtSeqGetSet, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtSeqGetSet
    __delitem__(PyMapSetDel_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSet(ExtMapSetDel_subclassing_ExtSeqGetSet):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSet, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSet()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSet
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSet, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSet
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtSeqGetSet, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtSeqGetSet, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtSeqGetSet()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtSeqGetSet
    __delitem__(ExtSeqSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqSetDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqGetSet()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqGetSet
    __setitem__(PySeqSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqGetSet
    __delitem__(PySeqSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSet(ExtSeqSetDel_subclassing_ExtSeqGetSet):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSet()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSet
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSet
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtMapGet_subclassing_ExtSeqGetSet()
    >>> obj[5]  # ExtMapGet_subclassing_ExtSeqGetSet
    __getitem__(ExtMapGet_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5] = 10  # ExtMapGet_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtSeqGetSet, i={i})")

    >>> obj = PyMapGet_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PyMapGet_subclassing_ExtSeqGetSet
    __getitem__(PyMapGet_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetSet(ExtMapGet_subclassing_ExtSeqGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetSet, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetSet
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtSeqGetSet, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtSeqGet_subclassing_ExtSeqGetSet()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGet_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGetSet
    __getitem__(PySeqGet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetSet(ExtSeqGet_subclassing_ExtSeqGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetSet
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtSeqGetSet()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtSeqGetSet
    __getitem__(ExtMapGetDel_subclassing_ExtSeqGetSet, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtSeqGetSet
    __delitem__(ExtMapGetDel_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5] = 10  # ExtMapGetDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtSeqGetSet, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtSeqGetSet, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtSeqGetSet
    __getitem__(PyMapGetDel_subclassing_ExtSeqGetSet, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtSeqGetSet
    __delitem__(PyMapGetDel_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSet(ExtMapGetDel_subclassing_ExtSeqGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSet, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSet, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSet
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSet, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSet
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtSeqGetSet, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtSeqGetSet, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtSeqGetSet()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtSeqGetSet
    __delitem__(ExtSeqGetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetSet
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetSet
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSet(ExtSeqGetDel_subclassing_ExtSeqGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSet
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSet
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtSeqGetSet()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtSeqGetSet
    __getitem__(ExtMapGetSet_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtSeqGetSet
    __setitem__(ExtMapGetSet_subclassing_ExtSeqGetSet, i=5, value=10)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtSeqGetSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtSeqGetSet, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtSeqGetSet
    __getitem__(PyMapGetSet_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtSeqGetSet
    __setitem__(PyMapGetSet_subclassing_ExtSeqGetSet, i=5, value=10)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSet(ExtMapGetSet_subclassing_ExtSeqGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSet, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSet
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSet
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSet, i=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtSeqGetSet, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtSeqGetSet, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtSeqGetSet()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSet(ExtSeqGetSet_subclassing_ExtSeqGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSet
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSet
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtSeqGetSet()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqGetSet
    __getitem__(ExtMapGetSetDel_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtSeqGetSet
    __setitem__(ExtMapGetSetDel_subclassing_ExtSeqGetSet, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqGetSet
    __delitem__(ExtMapGetSetDel_subclassing_ExtSeqGetSet, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtSeqGetSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtSeqGetSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtSeqGetSet, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtSeqGetSet
    __getitem__(PyMapGetSetDel_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtSeqGetSet
    __setitem__(PyMapGetSetDel_subclassing_ExtSeqGetSet, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtSeqGetSet
    __delitem__(PyMapGetSetDel_subclassing_ExtSeqGetSet, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSet(ExtMapGetSetDel_subclassing_ExtSeqGetSet):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSet, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSet, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSet, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSet
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSet, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSet
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSet, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSet
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSet, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtSeqGetSet, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtSeqGetSet, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtSeqGetSet, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtSeqGetSet()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqGetSet
    __getitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtSeqGetSet
    __setitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqGetSet
    __delitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSet(ExtSeqGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSet
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSet
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSet
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSet(ExtSeqGetSetDel_subclassing_ExtSeqGetSet):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSet()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSet
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSet
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSet
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetSet, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtMapDel_subclassing_ExtMapGetSetDel()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapDel_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5]  # ExtMapDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # ExtMapDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapGetSetDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapGetSetDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapGetSetDel
    __delitem__(PyMapDel_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSetDel(ExtMapDel_subclassing_ExtMapGetSetDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSetDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSetDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSetDel
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtMapGetSetDel, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtSeqDel_subclassing_ExtMapGetSetDel()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtMapGetSetDel
    __delitem__(ExtSeqDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # ExtSeqDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtMapGetSetDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtMapGetSetDel
    __delitem__(PySeqDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSetDel(ExtSeqDel_subclassing_ExtMapGetSetDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSetDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSetDel
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtMapSet_subclassing_ExtMapGetSetDel()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapSet_subclassing_ExtMapGetSetDel, i=5, value=10)
    >>> obj[5]  # ExtMapSet_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> del obj[5]  # ExtMapSet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapGetSetDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapGetSetDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapGetSetDel
    __setitem__(PyMapSet_subclassing_ExtMapGetSetDel, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> del obj[5]  # PyMapSet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetSetDel(ExtMapSet_subclassing_ExtMapGetSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetSetDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetSetDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetSetDel
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetSetDel, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> del obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtMapGetSetDel, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtSeqSet_subclassing_ExtMapGetSetDel()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtMapGetSetDel
    __setitem__(ExtSeqSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # ExtSeqSet_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> del obj[5]  # ExtSeqSet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtMapGetSetDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtMapGetSetDel
    __setitem__(PySeqSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> del obj[5]  # PySeqSet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetSetDel(ExtSeqSet_subclassing_ExtMapGetSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetSetDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetSetDel
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> del obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapSetDel_subclassing_ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapSetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5]  # ExtMapSetDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapGetSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapGetSetDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapGetSetDel
    __setitem__(PyMapSetDel_subclassing_ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapGetSetDel
    __delitem__(PyMapSetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSetDel(ExtMapSetDel_subclassing_ExtMapGetSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSetDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSetDel
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSetDel
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtMapGetSetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtMapGetSetDel, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtSeqSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtMapGetSetDel
    __delitem__(ExtSeqSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqSetDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtMapGetSetDel
    __setitem__(PySeqSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtMapGetSetDel
    __delitem__(PySeqSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSetDel(ExtSeqSetDel_subclassing_ExtMapGetSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSetDel
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSetDel
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel, i=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtMapGet_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # ExtMapGet_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGet_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGet_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGetSetDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGetSetDel
    __getitem__(PyMapGet_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetSetDel(ExtMapGet_subclassing_ExtMapGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetSetDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetSetDel
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtMapGetSetDel, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtSeqGet_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtMapGetSetDel
    __getitem__(ExtSeqGet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGet_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # ExtSeqGet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtMapGetSetDel
    __getitem__(PySeqGet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # PySeqGet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetSetDel(ExtSeqGet_subclassing_ExtMapGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetSetDel
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetSetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetSetDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetSetDel
    __getitem__(PyMapGetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetSetDel
    __delitem__(PyMapGetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSetDel(ExtMapGetDel_subclassing_ExtMapGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSetDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSetDel
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSetDel
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtMapGetSetDel, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtMapGetSetDel, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtSeqGetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtMapGetSetDel
    __delitem__(ExtSeqGetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtMapGetSetDel
    __getitem__(PySeqGetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtMapGetSetDel
    __delitem__(PySeqGetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSetDel(ExtSeqGetDel_subclassing_ExtMapGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSetDel
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSetDel
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel, i=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSet_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSet_subclassing_ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSetDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSetDel
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSetDel
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSetDel(ExtMapGetSet_subclassing_ExtMapGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSetDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSetDel
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSetDel
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtMapGetSetDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtMapGetSetDel, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtMapGetSetDel
    __getitem__(ExtSeqGetSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtMapGetSetDel
    __setitem__(ExtSeqGetSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtMapGetSetDel
    __getitem__(PySeqGetSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtMapGetSetDel
    __setitem__(PySeqGetSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSetDel(ExtSeqGetSet_subclassing_ExtMapGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSetDel
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSetDel
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel, i=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtMapGetSetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtMapGetSetDel_subclassing_ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtMapGetSetDel
    __delitem__(ExtMapGetSetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel_subclassing_ExtMapGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSetDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSetDel
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSetDel
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSetDel
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtMapGetSetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtMapGetSetDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtMapGetSetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtMapGetSetDel, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapGetSetDel
    __getitem__(ExtSeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtMapGetSetDel
    __setitem__(ExtSeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtMapGetSetDel
    __delitem__(ExtSeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtMapGetSetDel(ExtMapGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtMapGetSetDel
    __getitem__(PySeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtMapGetSetDel
    __setitem__(PySeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtMapGetSetDel
    __delitem__(PySeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSetDel(ExtSeqGetSetDel_subclassing_ExtMapGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSetDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSetDel
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSetDel
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSetDel
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtMapGetSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtMapDel_subclassing_ExtSeqGetSetDel()
    >>> del obj[5]  # ExtMapDel_subclassing_ExtSeqGetSetDel
    __delitem__(ExtMapDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5]  # ExtMapDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtMapDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PyMapDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtSeqGetSetDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtSeqGetSetDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtSeqGetSetDel
    __delitem__(PyMapDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)

    >>> class PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSetDel(ExtMapDel_subclassing_ExtSeqGetSetDel):
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSetDel, i={i})")

    >>> obj = PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSetDel()
    >>> del obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSetDel
    __delitem__(PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5]  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PyMapDel_subclassing_ExtMapDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    """
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapDel_subclassing_ExtSeqGetSetDel, i={i})")


@cython.cclass
class ExtSeqDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtSeqDel_subclassing_ExtSeqGetSetDel()
    >>> del obj[5]  # ExtSeqDel_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqGetSetDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqGetSetDel
    __delitem__(PySeqDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSetDel(ExtSeqDel_subclassing_ExtSeqGetSetDel):
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSetDel()
    >>> del obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSetDel
    __delitem__(PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqDel_subclassing_ExtSeqDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    """
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapSet_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtMapSet_subclassing_ExtSeqGetSetDel()
    >>> obj[5] = 10  # ExtMapSet_subclassing_ExtSeqGetSetDel
    __setitem__(ExtMapSet_subclassing_ExtSeqGetSetDel, i=5, value=10)
    >>> obj[5]  # ExtMapSet_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtMapSet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapSet_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtSeqGetSetDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtSeqGetSetDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtSeqGetSetDel
    __setitem__(PyMapSet_subclassing_ExtSeqGetSetDel, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PyMapSet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)

    >>> class PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetSetDel(ExtMapSet_subclassing_ExtSeqGetSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetSetDel, i={i}, value={value})")

    >>> obj = PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetSetDel()
    >>> obj[5] = 10  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetSetDel
    __setitem__(PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetSetDel, i=5, value=10)
    >>> obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PyMapSet_subclassing_ExtMapSet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSet_subclassing_ExtSeqGetSetDel, i={i}, value={value})")


@cython.cclass
class ExtSeqSet_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtSeqSet_subclassing_ExtSeqGetSetDel()
    >>> obj[5] = 10  # ExtSeqSet_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # ExtSeqSet_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqSet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSet_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqGetSetDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqGetSetDel
    __setitem__(PySeqSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqSet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetSetDel(ExtSeqSet_subclassing_ExtSeqGetSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetSetDel()
    >>> obj[5] = 10  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetSetDel
    __setitem__(PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqSet_subclassing_ExtSeqSet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapSetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtMapSetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5] = 10  # ExtMapSetDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtMapSetDel_subclassing_ExtSeqGetSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapSetDel_subclassing_ExtSeqGetSetDel
    __delitem__(ExtMapSetDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5]  # ExtMapSetDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapSetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtSeqGetSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtSeqGetSetDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtSeqGetSetDel
    __setitem__(PyMapSetDel_subclassing_ExtSeqGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtSeqGetSetDel
    __delitem__(PyMapSetDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)

    >>> class PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSetDel(ExtMapSetDel_subclassing_ExtSeqGetSetDel):
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSetDel, i={i})")

    >>> obj = PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5] = 10  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSetDel
    __setitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSetDel
    __delitem__(PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5]  # PyMapSetDel_subclassing_ExtMapSetDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapSetDel_subclassing_ExtSeqGetSetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapSetDel_subclassing_ExtSeqGetSetDel, i={i})")


@cython.cclass
class ExtSeqSetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtSeqSetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5] = 10  # ExtSeqSetDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqSetDel_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # ExtSeqSetDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqSetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqGetSetDel
    __setitem__(PySeqSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqGetSetDel
    __delitem__(PySeqSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSetDel(ExtSeqSetDel_subclassing_ExtSeqGetSetDel):
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5] = 10  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSetDel
    __setitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSetDel
    __delitem__(PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5]  # PySeqSetDel_subclassing_ExtSeqSetDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    """
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGet_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtMapGet_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # ExtMapGet_subclassing_ExtSeqGetSetDel
    __getitem__(ExtMapGet_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGet_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtMapGet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapGet_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtSeqGetSetDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtSeqGetSetDel
    __getitem__(PyMapGet_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PyMapGet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)

    >>> class PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetSetDel(ExtMapGet_subclassing_ExtSeqGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetSetDel, i={i})")

    >>> obj = PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetSetDel
    __getitem__(PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PyMapGet_subclassing_ExtMapGet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGet_subclassing_ExtSeqGetSetDel, i={i})")


@cython.cclass
class ExtSeqGet_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtSeqGet_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # ExtSeqGet_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGet_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGet_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGetSetDel
    __getitem__(PySeqGet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetSetDel(ExtSeqGet_subclassing_ExtSeqGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetSetDel
    __getitem__(PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGet_subclassing_ExtSeqGet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtMapGetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # ExtMapGetDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtMapGetDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> del obj[5]  # ExtMapGetDel_subclassing_ExtSeqGetSetDel
    __delitem__(ExtMapGetDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PyMapGetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtSeqGetSetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtSeqGetSetDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtSeqGetSetDel
    __getitem__(PyMapGetDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtSeqGetSetDel
    __delitem__(PyMapGetDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)

    >>> class PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSetDel(ExtMapGetDel_subclassing_ExtSeqGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSetDel, i={i})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSetDel, i={i})")

    >>> obj = PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSetDel
    __getitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> del obj[5]  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSetDel
    __delitem__(PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetDel_subclassing_ExtMapGetDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetDel_subclassing_ExtSeqGetSetDel, i={i})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetDel_subclassing_ExtSeqGetSetDel, i={i})")


@cython.cclass
class ExtSeqGetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtSeqGetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # ExtSeqGetDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # ExtSeqGetDel_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> import cython

    >>> class PySeqGetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetSetDel
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetSetDel
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)

    >>> class PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetDel_subclassing_ExtSeqGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSetDel
    __getitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> del obj[5]  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSetDel
    __delitem__(PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetDel_subclassing_ExtSeqGetDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")


@cython.cclass
class ExtMapGetSet_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtMapGetSet_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # ExtMapGetSet_subclassing_ExtSeqGetSetDel
    __getitem__(ExtMapGetSet_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSet_subclassing_ExtSeqGetSetDel
    __setitem__(ExtMapGetSet_subclassing_ExtSeqGetSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PyMapGetSet_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtSeqGetSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtSeqGetSetDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtSeqGetSetDel
    __getitem__(PyMapGetSet_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtSeqGetSetDel
    __setitem__(PyMapGetSet_subclassing_ExtSeqGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)

    >>> class PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSetDel(ExtMapGetSet_subclassing_ExtSeqGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSetDel, i={i}, value={value})")

    >>> obj = PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSetDel
    __getitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSetDel
    __setitem__(PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSet_subclassing_ExtMapGetSet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSet_subclassing_ExtSeqGetSetDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSet_subclassing_ExtSeqGetSetDel, i={i}, value={value})")


@cython.cclass
class ExtSeqGetSet_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtSeqGetSet_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # ExtSeqGetSet_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSet_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSet_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSetDel
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSetDel
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSetDel(ExtSeqGetSet_subclassing_ExtSeqGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")

    >>> obj = PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSetDel
    __getitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSetDel
    __setitem__(PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSet_subclassing_ExtSeqGetSet_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSet_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")


@cython.cclass
class ExtMapGetSetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtMapGetSetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtMapGetSetDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5] = 10  # ExtMapGetSetDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtMapGetSetDel_subclassing_ExtSeqGetSetDel, i=5, value=10)
    >>> del obj[5]  # ExtMapGetSetDel_subclassing_ExtSeqGetSetDel
    __delitem__(ExtMapGetSetDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> import cython

    >>> class PyMapGetSetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtSeqGetSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtSeqGetSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtSeqGetSetDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtSeqGetSetDel
    __getitem__(PyMapGetSetDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtSeqGetSetDel
    __setitem__(PyMapGetSetDel_subclassing_ExtSeqGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtSeqGetSetDel
    __delitem__(PyMapGetSetDel_subclassing_ExtSeqGetSetDel, i=5)

    >>> class PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSetDel(ExtMapGetSetDel_subclassing_ExtSeqGetSetDel):
    ...     def __getitem__(self, i):
    ...         print(f"__getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSetDel, i={i})")
    ...     def __setitem__(self, i, value):
    ...         print(f"__setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSetDel, i={i}, value={value})")
    ...     def __delitem__(self, i):
    ...         print(f"__delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSetDel, i={i})")

    >>> obj = PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSetDel
    __getitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSetDel, i=5)
    >>> obj[5] = 10  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSetDel
    __setitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSetDel, i=5, value=10)
    >>> del obj[5]  # PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSetDel
    __delitem__(PyMapGetSetDel_subclassing_ExtMapGetSetDel_subclassing_ExtSeqGetSetDel, i=5)
    """
    def __getitem__(self, i):
        print(f"__getitem__(ExtMapGetSetDel_subclassing_ExtSeqGetSetDel, i={i})")
    def __setitem__(self, i, value):
        print(f"__setitem__(ExtMapGetSetDel_subclassing_ExtSeqGetSetDel, i={i}, value={value})")
    def __delitem__(self, i):
        print(f"__delitem__(ExtMapGetSetDel_subclassing_ExtSeqGetSetDel, i={i})")


@cython.cclass
class ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    """
    >>> obj = ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel
    __getitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel
    __setitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel
    __delitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> import cython

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)

    >>> class PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel(ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel):
    ...     def __getitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")
    ...     def __setitem__(self, i: cython.Py_ssize_t, value):
    ...         print(f"__setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    ...     def __delitem__(self, i: cython.Py_ssize_t):
    ...         print(f"__delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")

    >>> obj = PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel()
    >>> obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel
    __getitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    >>> obj[5] = 10  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel
    __setitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5, value=10)
    >>> del obj[5]  # PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel
    __delitem__(PySeqGetSetDel_subclassing_ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t=5)
    """
    def __getitem__(self, i: cython.Py_ssize_t):
        print(f"__getitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")
    def __setitem__(self, i: cython.Py_ssize_t, value):
        print(f"__setitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i}, value={value})")
    def __delitem__(self, i: cython.Py_ssize_t):
        print(f"__delitem__(ExtSeqGetSetDel_subclassing_ExtSeqGetSetDel, i: cython.Py_ssize_t={i})")


###### END: generated test code ######


#################################################
##  This is the test code generator script:
#################################################

def _gen_test_code():
    code = []
    add = code.append

    from string import Template as _Template
    def Template(s: str):
        return _Template(s.rstrip() + '\n')

    method_templates = {
        'Get': Template("""\
    def __getitem__(self, $index):
        print(f"__getitem__($type, $index={i})")
        """),
        'Set': Template("""\
    def __setitem__(self, $index, value):
        print(f"__setitem__($type, $index={i}, value={value})")
        """),
        'Del': Template("""\
    def __delitem__(self, $index):
        print(f"__delitem__($type, $index={i})")
        """),
    }

    doctest_templates = {
        'Get': Template("""\
    >>> obj[5]  # $doctest_type
    __getitem__($type, $index=5)
        """),
        'Set': Template("""\
    >>> obj[5] = 10  # $doctest_type
    __setitem__($type, $index=5, value=10)
        """),
        'Del': Template("""\
    >>> del obj[5]  # $doctest_type
    __delitem__($type, $index=5)
        """),
    }

    index_arg_code = [
        ('Map', "i"),
        ('Seq', "i: cython.Py_ssize_t"),
    ]

    def test_name(ext_or_py, method_names, index_name, base_name):
        return f'{ext_or_py}{index_name}{''.join(method_names)}{"_subclassing_"+base_name if base_name else ""}'

    def generate_classes(method_names, base_class_methods, base_index_name, base_index):
        base_name = f'Ext{base_index_name}{''.join(base_class_methods)}' if base_class_methods else ''
        base_class_methods = [name for name in base_class_methods if name not in method_names]

        for index_name, index in index_arg_code:
            ext_name = test_name('Ext', method_names, index_name, base_name)
            add("@cython.cclass\n")
            add(f"class {ext_name}({base_name}):\n")
            add(f'    """\n')

            # Extension type tests.
            add(f'    >>> obj = {ext_name}()\n')
            for name in method_names:
                add(doctest_templates[name].substitute(type=ext_name, doctest_type=ext_name, index=index))
            for name in base_class_methods:
                add(doctest_templates[name].substitute(type=base_name, doctest_type=ext_name, index=base_index))

            # Python type and subtype tests (as doctests to reduce compilation size).
            add(f"    >>> import cython\n")
            for pyclass_base_name in (base_name, ext_name):
                class_name = test_name('Py', method_names, index_name, pyclass_base_name)
                add("\n")
                add(f"    >>> class {class_name}({pyclass_base_name}):\n")
                for name in method_names:
                    for line in method_templates[name].substitute(type=class_name, index=index).splitlines(keepends=True):
                        add(f"    ... {line}")

                add("\n")
                add(f'    >>> obj = {class_name}()\n')
                for name in method_names:
                    add(doctest_templates[name].substitute(type=class_name, doctest_type=class_name, index=index))
                for name in base_class_methods:
                    add(doctest_templates[name].substitute(type=base_name, doctest_type=class_name, index=base_index))

            add('    """\n')

            # Extension method implementations.
            for name in method_names:
                add(method_templates[name].substitute(type=ext_name, index=index))
            add("\n\n")

    # Generate simple (base) classes.

    from itertools import product
    all_implementations = [
        tuple(name for name in method_names if name is not None)
        for method_names in product(*[[None, name] for name in method_templates])
    ]
    assert all_implementations[0] == (), all_implementations[0]
    del all_implementations[0]

    for method_names in all_implementations:
        generate_classes(method_names, (), None, None)

    # Generate subtypes with partial and complete method overrides.

    for base_class_methods in all_implementations:
        for base_index_name, base_index in index_arg_code:
            for method_names in all_implementations:
                generate_classes(method_names, base_class_methods, base_index_name, base_index)

    return code


def _regen_test_file(file_path):
    with open(file_path) as f:
        lines = iter(f)
        start_lines = []
        end_lines = []
        for line in lines:
            start_lines.append(line)
            if line.startswith('###### ') and 'START' in line:
                break
        for line in lines:
            if line.startswith('###### ') and 'END' in line:
                end_lines.append(line)
                break
        end_lines.extend(lines)

    code = _gen_test_code()

    from itertools import chain
    with open(file_path, 'w') as f:
        f.writelines(chain(start_lines, code, end_lines))


if __name__ == '__main__':
    _regen_test_file(__file__)
