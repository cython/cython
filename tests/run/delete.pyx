
class A(object):
    """
    >>> a = A()
    >>> a.f()
    [2, 1]
    >>> a.g()
    (False, True)
    """
    def f(self):
        self.refs = [3,2,1]
        del self.refs[0]
        return self.refs

    def g(self):
        self.a = 3
        del self.a
        return (hasattr(self, u"a"), hasattr(self, u"g"))

def del_item(L, o):
    """
    >>> del_item({1: 'a', 2: 'b'}, 1)
    {2: 'b'}
    >>> del_item(list(range(10)), 2)
    [0, 1, 3, 4, 5, 6, 7, 8, 9]
    """
    del L[o]
    return L

def del_dict(dict D, o):
    """
    >>> del_dict({1: 'a', 2: 'b'}, 1)
    {2: 'b'}
    """
    del D[o]
    return D

def del_list(list L, o):
    """
    >>> del_list(list(range(5)), 3)
    [0, 1, 2, 4]
    """
    del L[o]
    return L

def del_int(L, int i):
    """
    >>> del_int(list(range(5)), 3)
    [0, 1, 2, 4]
    >>> del_int({-1: 'neg', 1: 'pos'}, -1)
    {1: 'pos'}
    """
    del L[i]
    return L

def del_list_int(L, int i):
    """
    >>> del_list_int(list(range(5)), 3)
    [0, 1, 2, 4]
    """
    del L[i]
    return L

def del_temp_slice(a):
    """
    >>> class A(object):
    ...     attr = [1,2,3]
    >>> a = A()
    >>> a.attr
    [1, 2, 3]
    >>> del_temp_slice(a)
    []
    >>> a.attr
    []
    >>> del_temp_slice(a)
    []
    >>> a.attr
    []
    """
    while a.attr:
        del a.attr[:]
    return a.attr
