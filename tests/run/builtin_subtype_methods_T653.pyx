#cython: language_level=2
# mode: run
# ticket: t653

cimport cython

# The "contains" tests relate to GH-4785 - replacing the method
# call with PySequence_Contains was causing infinite recursion
# for some classes

cdef class MyList(list):
    """
    >>> l = MyList()
    >>> l.__contains__(1)
    MyList.__contains__
    False
    >>> l.append(1)
    >>> l.__contains__(1)
    MyList.__contains__
    True
    """
    def test_append(self, x):
        """
        >>> l = MyList()
        >>> type(l) is MyList
        True
        >>> list(l)
        []
        >>> l.test_append(5)
        >>> list(l)
        [5]
        """
        self.append(x)

    def __contains__(self, value):
        print "MyList.__contains__"
        return list.__contains__(self, value)  # probably optimized

cdef class MyDict(dict):
    # tests for __contains__ are in the global __doc__ to version-check a PyPy bug

    @cython.test_assert_path_exists("//ComprehensionNode//AttributeNode",
                                    "//ComprehensionNode//AttributeNode[@attribute='items']")
    @cython.test_fail_if_path_exists("//ComprehensionNode//CMethodSelfCloneNode")
    def test_items(self):
        """
        >>> MyDict(a=1, b=2).test_items()
        [('a', 1), ('b', 2)]
        """
        l = [ (key, value) for key, value in self.items() ]
        l.sort()
        return l

    def test_values(self):
        """
        >>> MyDict(a=1, b=2).test_values()
        [1, 2]
        """
        l = [ v for v in self.values() ]
        l.sort()
        return l

    def __contains__(self, key):
        print "MyDict.__contains__"
        return dict.__contains__(self, key)

import sys
pypy_version = getattr(sys, 'pypy_version_info', None)
if not (pypy_version and pypy_version < (7, 3, 10)):
    __doc__ = """
    >>> MyDict(a=1).__contains__("a")
    MyDict.__contains__
    True
    """

@cython.final
cdef class MyDictFinal(dict):
    @cython.test_assert_path_exists("//ComprehensionNode//CMethodSelfCloneNode")
    def test_items(self):
        """
        >>> MyDictFinal(a=1, b=2).test_items()
        [('a', 1), ('b', 2)]
        """
        l = [ (key, value) for key, value in self.items() ]
        l.sort()
        return l

    def test_values(self):
        """
        >>> MyDictFinal(a=1, b=2).test_values()
        [1, 2]
        """
        l = [ v for v in self.values() ]
        l.sort()
        return l

cdef class MyDict2(MyDict):
    @cython.test_assert_path_exists("//ComprehensionNode//AttributeNode",
                                    "//ComprehensionNode//AttributeNode[@attribute='items']")
    @cython.test_fail_if_path_exists("//ComprehensionNode//CMethodSelfCloneNode")
    def test_items(self):
        """
        >>> MyDict2(a=1, b=2).test_items()
        [('a', 1), ('b', 2)]
        """
        l = [ (key, value) for key, value in self.items() ]
        l.sort()
        return l

    def test_values(self):
        """
        >>> MyDict2(a=1, b=2).test_values()
        [1, 2]
        """
        l = [ v for v in self.values() ]
        l.sort()
        return l

@cython.final
cdef class MyDict2Final(MyDict):
    @cython.test_assert_path_exists("//ComprehensionNode//CMethodSelfCloneNode")
    def test_items(self):
        """
        >>> MyDict2Final(a=1, b=2).test_items()
        [('a', 1), ('b', 2)]
        """
        l = [ (key, value) for key, value in self.items() ]
        l.sort()
        return l

    def test_values(self):
        """
        >>> MyDict2Final(a=1, b=2).test_values()
        [1, 2]
        """
        l = [ v for v in self.values() ]
        l.sort()
        return l

@cython.final
cdef class MyDictOverride(dict):
    def items(self):
        return [(1,2), (3,4)]

    @cython.test_assert_path_exists("//ComprehensionNode//AttributeNode",
                                    "//ComprehensionNode//AttributeNode[@attribute='items']")
    @cython.test_fail_if_path_exists("//ComprehensionNode//CMethodSelfCloneNode")
    def test_items(self):
        """
        >>> MyDictOverride(a=1, b=2).test_items()
        [(1, 2), (3, 4)]
        """
        l = [ (key, value) for key, value in self.items() ]
        l.sort()
        return l

    def test_values(self):
        """
        >>> MyDictOverride(a=1, b=2).test_values()
        [1, 2]
        """
        l = [ v for v in self.values() ]
        l.sort()
        return l

@cython.final
cdef class MyDictOverride2(MyDict):
    def items(self):
        return [(1,2), (3,4)]

    @cython.test_assert_path_exists("//ComprehensionNode//AttributeNode",
                                    "//ComprehensionNode//AttributeNode[@attribute='items']")
    @cython.test_fail_if_path_exists("//ComprehensionNode//CMethodSelfCloneNode")
    def test_items(self):
        """
        >>> MyDictOverride2(a=1, b=2).test_items()
        [(1, 2), (3, 4)]
        """
        l = [ (key, value) for key, value in self.items() ]
        l.sort()
        return l

    def test_values(self):
        """
        >>> MyDictOverride2(a=1, b=2).test_values()
        [1, 2]
        """
        l = [ v for v in self.values() ]
        l.sort()
        return l

class MyBytes(bytes):
    """
    >>> mb = MyBytes(b"abc")
    >>> mb.__contains__(b"a")
    MyBytes.__contains__
    True
    >>> mb.__contains__(b"z")
    MyBytes.__contains__
    False
    """
    def __contains__(self, value):
        print "MyBytes.__contains__"
        return bytes.__contains__(self, value)
