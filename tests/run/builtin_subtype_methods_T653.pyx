#cython: language_level=2
# mode: run
# ticket: 653

cimport cython

cdef class MyList(list):
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

cdef class MyDict(dict):
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
