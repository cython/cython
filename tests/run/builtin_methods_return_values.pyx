# mode: run
# tag: list, set, builtins
# ticket: t688

_set = set

class TestObj(object):
    pass

def _setattr(obj):
    """
    >>> t = TestObj()
    >>> _setattr(t) is None
    True
    >>> t.test is None
    True
    """
    setattr(obj, 'test', None)
    return setattr(obj, 'test', None)

def _delattr(obj):
    """
    >>> t = TestObj()
    >>> t.test1 = t.test2 = True
    >>> _delattr(t) is None
    True
    >>> hasattr(t, 'test1')
    False
    >>> hasattr(t, 'test2')
    False
    """
    delattr(obj, 'test1')
    return delattr(obj, 'test2')

def list_sort(list l):
    """
    >>> list_sort([1,2,3]) is None
    True
    """
    l.sort()
    return l.sort()

def list_reverse(list l):
    """
    >>> list_reverse([1,2,3]) is None
    True
    """
    l.reverse()
    return l.reverse()

def list_insert(list l):
    """
    >>> list_insert([1,2,3]) is None
    True
    """
    l.insert(1, 2)
    return l.insert(1, 2)

def list_append(list l):
    """
    >>> list_append([1,2,3]) is None
    True
    """
    l.append(1)
    return l.append(2)

def set_clear(set s):
    """
    >>> set_clear(_set([1,2,3])) is None
    True
    >>> set_clear(None)
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'clear'
    """
    s.clear()
    return s.clear()

def set_discard(set s):
    """
    >>> set_discard(_set([1,2,3])) is None
    True
    """
    s.discard(1)
    return s.discard(2)

def set_add(set s):
    """
    >>> set_add(_set([1,2,3])) is None
    True
    """
    s.add(1)
    return s.add(2)

def dict_clear(dict d):
    """
    >>> dict_clear({1:2,3:4}) is None
    True
    >>> dict_clear(None)
    Traceback (most recent call last):
    AttributeError: 'NoneType' object has no attribute 'clear'
    """
    d.clear()
    return d.clear()
