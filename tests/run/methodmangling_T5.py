# mode: run
# ticket: 5

class CyTest(object):
    """
    >>> cy = CyTest()
    >>> '_CyTest__private' in dir(cy)
    True
    >>> cy._CyTest__private()
    8
    >>> '__private' in dir(cy)
    False
    >>> '_CyTest__x' in dir(cy)
    True

    >>> '__x' in dir(cy)
    False
    """
    __x = 1
    def __private(self): return 8

    def get(self):
        """
        >>> CyTest().get()
        (1, 1, 8)
        """
        return self._CyTest__x, self.__x, self.__private()

    def get_inner(self):
        """
        >>> CyTest().get_inner()
        (1, 1, 8)
        """
        def get(o):
            return o._CyTest__x, o.__x, o.__private()
        return get(self)

class CyTestSub(CyTest):
    """
    >>> cy = CyTestSub()
    >>> '_CyTestSub__private' in dir(cy)
    True
    >>> cy._CyTestSub__private()
    9
    >>> '_CyTest__private' in dir(cy)
    True
    >>> cy._CyTest__private()
    8
    >>> '__private' in dir(cy)
    False

    >>> '_CyTestSub__x' in dir(cy)
    False
    >>> '_CyTestSub__y' in dir(cy)
    True
    >>> '_CyTest__x' in dir(cy)
    True
    >>> '__x' in dir(cy)
    False
    """
    __y = 2
    def __private(self): return 9

    def get(self):
        """
        >>> CyTestSub().get()
        (1, 2, 2, 9)
        """
        return self._CyTest__x, self._CyTestSub__y, self.__y, self.__private()

    def get_inner(self):
        """
        >>> CyTestSub().get_inner()
        (1, 2, 2, 9)
        """
        def get(o):
            return o._CyTest__x, o._CyTestSub__y, o.__y, o.__private()
        return get(self)

class _UnderscoreTest(object):
    """
    >>> ut = _UnderscoreTest()
    >>> '__x' in dir(ut)
    False
    >>> '_UnderscoreTest__x' in dir(ut)
    True
    >>> ut._UnderscoreTest__x
    1
    >>> ut.get()
    1
    """
    __x = 1

    def get(self):
        return self.__x
