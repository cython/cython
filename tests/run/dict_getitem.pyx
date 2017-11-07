# mode: run
# tag: dict, getitem

cimport cython

def test(dict d, index):
    """
    >>> d = { 1: 10 }
    >>> test(d, 1)
    10

    >>> test(d, 2)
    Traceback (most recent call last):
    KeyError: 2

    >>> test(d, (1,2))
    Traceback (most recent call last):
    KeyError: (1, 2)

    >>> import sys
    >>> try: d[(1,)]
    ... except KeyError:
    ...     args = sys.exc_info()[1].args
    ...     if sys.version_info >= (2,5): print(args)
    ...     else: print((args,))   # fake it for older CPython versions
    ((1,),)

    >>> import sys
    >>> try: test(d, (1,))
    ... except KeyError:
    ...     args = sys.exc_info()[1].args
    ...     if sys.version_info >= (2,5): print(args)
    ...     else: print((args,))   # fake it for older CPython versions
    ((1,),)

    >>> class Unhashable:
    ...    def __hash__(self):
    ...        raise ValueError
    >>> test(d, Unhashable())
    Traceback (most recent call last):
    ValueError

    >>> test(None, 1) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...object...
    """
    return d[index]


def getitem_str(dict d, obj, str index):
    """
    >>> d = {'abc': 1, 'xyz': 2, None: 3}
    >>> getitem_str(d, d, 'abc')
    (1, 1)
    >>> getitem_str(d, d, 'xyz')
    (2, 2)
    >>> getitem_str(d, d, None)
    (3, 3)

    >>> class GetItem(object):
    ...     def __getitem__(self, name): return d[name]
    >>> getitem_str(d, GetItem(), 'abc')
    (1, 1)
    >>> getitem_str(d, GetItem(), 'xyz')
    (2, 2)
    >>> getitem_str(d, GetItem(), None)
    (3, 3)
    >>> getitem_str(d, GetItem(), 'no')
    Traceback (most recent call last):
    KeyError: 'no'

    >>> class GetItemFail(object):
    ...     def __getitem__(self, name): raise ValueError("failed")
    >>> getitem_str(d, GetItemFail(), 'abc')
    Traceback (most recent call last):
    ValueError: failed
    >>> getitem_str(d, GetItemFail(), None)
    Traceback (most recent call last):
    ValueError: failed
    """
    return d[index], obj[index]


def getitem_unicode(dict d, obj, unicode index):
    """
    >>> d = {'abc': 1, 'xyz': 2, None: 3}
    >>> getitem_unicode(d, d, u'abc')
    (1, 1)
    >>> getitem_unicode(d, d, u'xyz')
    (2, 2)
    >>> getitem_unicode(d, d, None)
    (3, 3)

    >>> class GetItem(object):
    ...     def __getitem__(self, name): return d[name]
    >>> getitem_unicode(d, GetItem(), u'abc')
    (1, 1)
    >>> getitem_unicode(d, GetItem(), u'xyz')
    (2, 2)
    >>> getitem_unicode(d, GetItem(), None)
    (3, 3)
    >>> try: getitem_unicode(d, GetItem(), u'no')
    ... except KeyError as exc: assert exc.args[0] == u'no', str(exc)
    ... else: assert False, "KeyError not raised"

    >>> class GetItemFail(object):
    ...     def __getitem__(self, name): raise ValueError("failed")
    >>> getitem_unicode(d, GetItemFail(), u'abc')
    Traceback (most recent call last):
    ValueError: failed
    """
    return d[index], obj[index]


def getitem_tuple(dict d, index):
    """
    >>> d = {1: 1, (1,): 2}
    >>> getitem_tuple(d, 1)
    (1, 2)
    """
    return d[index], d[index,]


def getitem_in_condition(dict d, key, expected_result):
    """
    >>> d = dict(a=1, b=2)
    >>> getitem_in_condition(d, 'a', 1)
    True
    """
    return d[key] is expected_result or d[key] == expected_result


@cython.test_fail_if_path_exists('//NoneCheckNode')
def getitem_not_none(dict d not None, key):
    """
    >>> d = { 1: 10 }
    >>> test(d, 1)
    10

    >>> test(d, 2)
    Traceback (most recent call last):
    KeyError: 2

    >>> test(d, (1,2))
    Traceback (most recent call last):
    KeyError: (1, 2)
    """
    return d[key]
