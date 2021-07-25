# cython: language_level=3
# mode: run
# ticket: t653


class DictPySubtype(dict):
    def keys(self):
        """
        >>> d = DictPySubtype(one=42, two=17, three=0)
        >>> for v in sorted(d.keys()):
        ...     print(v)
        three
        two
        """
        for key in dict.keys(self):
            if key != 'one':
                yield key

    def values(self):
        """
        >>> d = DictPySubtype(one=42, two=17, three=0)
        >>> for v in sorted(d.values()):
        ...     print(v)
        17
        42
        """
        for value in dict.values(self):
            if value:
                yield value

    def items(self):
        """
        >>> d = DictPySubtype(one=42, two=17, three=0)
        >>> for v in sorted(d.items()):
        ...     print(v)
        one
        two
        """
        for key, value in dict.items(self):
            if value:
                yield key


class ListPySubtype(list):
    """
    >>> lst = ListPySubtype([1,2,3])
    >>> lst.append(4)
    >>> lst
    [1, 2, 3, 5]
    """
    def append(self, value):
        list.append(self, value+1)
