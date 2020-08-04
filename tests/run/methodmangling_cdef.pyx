# mode: run

def call_cdt_private_cdef(CDefTest o):
    return o._CDefTest__private_cdef()

cdef __c_func():
    return "cdef function"

cdef __c_var = "Shouldn't see this"

cdef class CDefTest:
    """
    >>> cd = CDefTest()
    >>> '_CDefTest__private' in dir(cd)
    True
    >>> cd._CDefTest__private()
    8
    >>> call_cdt_private_cdef(cd)
    8
    >>> '__private' in dir(cd)
    False
    >>> '_CDefTest__x' in dir(cd)
    True

    >>> '__x' in dir(cd)
    False
    >>> cd._CDefTest__y
    2
    """
    __x = 1
    cdef public int __y

    def __init__(self):
        self.__y = 2

    def __private(self): return 8

    cdef __private_cdef(self): return 8

    def get(self):
        """
        >>> CDefTest().get()
        (1, 1, 8)
        """
        return self._CDefTest__x, self.__x, self.__private()

    def get_inner(self):
        """
        >>> CDefTest().get_inner()
        (1, 1, 8)
        """
        def get(o):
            return o._CDefTest__x, o.__x, o.__private()
        return get(self)

    def get_c_func(self):
        """
        Should still be able to access C function with __names
        >>> CDefTest().get_c_func()
        'cdef function'
        """
        return __c_func()

    def get_c_func2(self):
        """
        Should find mangled name before C __name
        >>> CDefTest().get_c_func2()
        'lambda'
        """
        _CDefTest__c_func = lambda: "lambda"
        return __c_func()

    def get_c_var(self):
        """
        >>> CDefTest().get_c_var()
        'c var'
        """
        global __c_var
        __c_var = "c var"
        return __c_var

def call_inpdx_private_cdef(InPxd o):
    return o._InPxd__private_cdef()

cdef class InPxd:
    """
    >>> InPxd()._InPxd__y
    2
    >>> call_inpdx_private_cdef(InPxd())
    8
    """
    def __init__(self):
        self.__y = 2

    cdef int __private_cdef(self): return 8
