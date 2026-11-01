# mode: run

# cython: language_level=3

# Also used by the language_level=2 tests in "strmethods_ll2.pyx"

cimport cython

fake_none = object()

@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def str_startswith(str s, sub, start=None, stop=None):
    """
    >>> str_startswith('a', 'a')
    True
    >>> str_startswith('ab', 'a')
    True
    >>> str_startswith('a', 'b')
    False
    >>> str_startswith('ab', 'b')
    False
    >>> str_startswith('a', ('a', 'b'))
    True
    >>> str_startswith('a', 'a', 1)
    False
    >>> str_startswith('a', 'a', 0, 0)
    False
    >>> str_startswith('a', 'a', fake_none)
    True
    >>> str_startswith('a', 'b', fake_none)
    False
    >>> str_startswith('a', 'a', fake_none, fake_none)
    True
    >>> str_startswith('a', 'a', fake_none, 0)
    False
    >>> str_startswith('a', 'a', 0, fake_none)
    True
    >>> str_startswith('a', 'a', 1, fake_none)
    False
    """

    if start is None:
      return s.startswith(sub)
    elif start is fake_none and stop is fake_none:
      return s.startswith(sub, None, None)
    elif start is fake_none:
      if stop is None:
        return s.startswith(sub, None)
      else:
        return s.startswith(sub, None, stop)
    elif stop is fake_none:
      return s.startswith(sub, start, None)
    elif stop is None:
      return s.startswith(sub, start)
    else:
      return s.startswith(sub, start, stop)


@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def str_endswith(str s, sub, start=None, stop=None):
    """
    >>> str_endswith('a', 'a')
    True
    >>> str_endswith('ba', 'a')
    True
    >>> str_endswith('a', 'b')
    False
    >>> str_endswith('ba', 'b')
    False
    >>> str_endswith('a', ('a', 'b'))
    True
    >>> str_endswith('a', 'a', 1)
    False
    >>> str_endswith('a', 'a', 0, 0)
    False
    """

    if start is None:
      return s.endswith(sub)
    elif stop is None:
      return s.endswith(sub, start)
    else:
      return s.endswith(sub, start, stop)


def str_find(str s, sub, start=None, stop=None):
    """
    >>> str_find('a', 'a')
    0
    >>> str_find('ab', 'a')
    0
    >>> str_find('a', 'b')
    -1
    >>> str_find('ab', 'b')
    1
    >>> str_find('a', 'a', 1)
    -1
    >>> str_find('a', 'a', 0, 0)
    -1
    >>> str_find('a', 'a', fake_none)
    0
    >>> str_find('a', 'b', fake_none)
    -1
    >>> str_find('a', 'a', fake_none, fake_none)
    0
    >>> str_find('a', 'a', fake_none, 0)
    -1
    >>> str_find('a', 'a', 0, fake_none)
    0
    >>> str_find('a', 'a', 1, fake_none)
    -1
    """

    if start is None:
      return s.find(sub)
    elif start is fake_none and stop is fake_none:
      return s.find(sub, None, None)
    elif start is fake_none:
      if stop is None:
        return s.find(sub, None)
      else:
        return s.find(sub, None, stop)
    elif stop is fake_none:
      return s.find(sub, start, None)
    elif stop is None:
      return s.find(sub, start)
    else:
      return s.find(sub, start, stop)


def object_as_name(object):
    """
    >>> object_as_name('abx')
    True
    >>> object_as_name('abc')
    False
    """
    return object.endswith("x")


def str_as_name(str):
    """
    >>> str_as_name('abx')
    True
    >>> str_as_name('abc')
    False
    """
    return str.endswith("x")


#@cython.test_fail_if_path_exists(
#    "//SimpleCallNode",
#    "//SimpleCallNode//NoneCheckNode",
#    "//SimpleCallNode//AttributeNode[@is_py_attr = false]")
def str_join(str s, args):
    """
    >>> print(str_join('a', list('bbb')))
    babab
    """
    result = s.join(args)
    assert cython.typeof(result) == "str object", cython.typeof(result)
    return result


#@cython.test_fail_if_path_exists(
#    "//SimpleCallNode",
#    "//SimpleCallNode//NoneCheckNode",
#    "//SimpleCallNode//AttributeNode[@is_py_attr = false]")
def literal_join(args):
    """
    >>> print(literal_join(list('abcdefg')))
    a|b|c|d|e|f|g
    """
    result = '|'.join(args)
    assert cython.typeof(result) == "str object", cython.typeof(result)
    return result


# unicode.__mod__(format, values)

format1 = 'abc%sdef'
format2 = 'abc%sdef%sghi'

def mod_format(str s, values):
    """
    >>> mod_format(format1, 'sa') == 'abcsadef'  or  mod_format(format1, 'sa')
    True
    >>> mod_format(format2, ('XYZ', 'ABC')) == 'abcXYZdefABCghi'  or  mod_format(format2, ('XYZ', 'ABC'))
    True
    >>> mod_format(None, 'sa')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...NoneType...
    >>> class RMod(object):
    ...     def __rmod__(self, other):
    ...         return 123
    >>> mod_format(None, RMod())
    123
    """
    assert cython.typeof(s % values) == "Python object", cython.typeof(s % values)
    return s % values


def mod_format_literal(values):
    """
    >>> mod_format_literal('sa') == 'abcsadef'  or  mod_format(format1, 'sa')
    True
    >>> mod_format_literal(('sa',)) == 'abcsadef'  or  mod_format(format1, ('sa',))
    True
    >>> mod_format_literal(['sa']) == "abc['sa']def"  or  mod_format(format1, ['sa'])
    True
    """
    assert cython.typeof('abc%sdef' % values) == "str object", cython.typeof('abc%sdef' % values)
    return 'abc%sdef' % values


def mod_format_tuple(*values):
    """
    >>> mod_format_tuple('sa') == 'abcsadef'  or  mod_format(format1, 'sa')
    True
    >>> mod_format_tuple()  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: not enough arguments for format string...
    """
    assert cython.typeof('abc%sdef' % values) == "str object", cython.typeof('abc%sdef' % values)
    return 'abc%sdef' % values
