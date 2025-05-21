# -*- coding: utf-8 -*-

cimport cython


text = u'ab jd  sdflk as sa  sadas asdas fsdf '
sep = u'  '
format1 = u'abc%sdef'
format2 = u'abc%sdef%sghi'
unicode_sa = u'sa'

multiline_text = u'''\
ab jd
sdflk as sa
sadas asdas fsdf '''

def print_all(l):
    for s in l:
        print(s)


# unicode.split(s, [sep, [maxsplit]])

@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def split(unicode s):
    """
    >>> def test_split():
    ...     py = text.split()
    ...     cy = split(text)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> print_all( test_split() )
    ab
    jd
    sdflk
    as
    sa
    sadas
    asdas
    fsdf
    """
    return s.split()

@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def split_sep(unicode s, sep):
    """
    >>> def test_split_sep(sep):
    ...     py = text.split(sep)
    ...     cy = split_sep(text, sep)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> print_all( test_split_sep(sep) )
    ab jd
    sdflk as sa
    sadas asdas fsdf\x20
    >>> print_all( test_split_sep(None) )
    ab
    jd
    sdflk
    as
    sa
    sadas
    asdas
    fsdf
    """
    return s.split(sep)

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceFromPyTypeNode",
    "//PythonCapiCallNode")
def split_sep_max(unicode s, sep, max):
    """
    >>> def test_split_sep_max(sep, max):
    ...     py = text.split(sep, max)
    ...     cy = split_sep_max(text, sep, max)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> print_all( test_split_sep_max(sep, 1) )
    ab jd
    sdflk as sa  sadas asdas fsdf\x20
    >>> print_all( test_split_sep_max(None, 2) )
    ab
    jd
    sdflk as sa  sadas asdas fsdf\x20
    >>> print_all( text.split(None, 2) )
    ab
    jd
    sdflk as sa  sadas asdas fsdf\x20
    >>> print_all( split_sep_max(text, None, 2) )
    ab
    jd
    sdflk as sa  sadas asdas fsdf\x20
    """
    return s.split(sep, max)

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode", "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def split_sep_max_int(unicode s, sep):
    """
    >>> def test_split_sep_max_int(sep):
    ...     py = text.split(sep, 1)
    ...     cy = split_sep_max_int(text, sep)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> print_all( test_split_sep_max_int(sep) )
    ab jd
    sdflk as sa  sadas asdas fsdf\x20
    >>> print_all( test_split_sep_max_int(None) )
    ab
    jd  sdflk as sa  sadas asdas fsdf\x20
    """
    return s.split(sep, 1)


# unicode.splitlines(s, [keepends])

@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def splitlines(unicode s):
    """
    >>> def test_splitlines(s):
    ...     py = s.splitlines()
    ...     cy = splitlines(s)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> len(test_splitlines(multiline_text))
    3
    >>> print_all( test_splitlines(multiline_text) )
    ab jd
    sdflk as sa
    sadas asdas fsdf\x20
    """
    return s.splitlines()

@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def splitlines_keep(unicode s, keep):
    """
    >>> def test_splitlines_keep(s, keep):
    ...     py = s.splitlines(keep)
    ...     cy = splitlines_keep(s, keep)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> len(test_splitlines_keep(multiline_text, True))
    3
    >>> print_all( test_splitlines_keep(multiline_text, True) )
    ab jd
    <BLANKLINE>
    sdflk as sa
    <BLANKLINE>
    sadas asdas fsdf\x20
    """
    return s.splitlines(keep)

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode", "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def splitlines_keep_bint(unicode s):
    """
    >>> def test_splitlines_keep_bint(s):
    ...     py = s.splitlines(True) + ['--'] + s.splitlines(False)
    ...     cy = splitlines_keep_bint(s)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> len(test_splitlines_keep_bint(multiline_text))
    7
    >>> print_all( test_splitlines_keep_bint(multiline_text) )
    ab jd
    <BLANKLINE>
    sdflk as sa
    <BLANKLINE>
    sadas asdas fsdf\x20
    --
    ab jd
    sdflk as sa
    sadas asdas fsdf\x20
    """
    return s.splitlines(True) + ['--'] + s.splitlines(False)


# unicode.join(s, iterable)

pipe_sep = u'|'

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode", "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode",
    "//SimpleCallNode//AttributeNode[@is_py_attr = true]")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
)
def join(unicode sep, l):
    """
    >>> def test_join(sep, l):
    ...     py = sep.join(l)
    ...     cy = join(sep, l)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> l = text.split()
    >>> len(l)
    8
    >>> print( test_join(pipe_sep, l) )
    ab|jd|sdflk|as|sa|sadas|asdas|fsdf
    """
    return sep.join(l)


@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode", "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode", "//NoneCheckNode",
    "//SimpleCallNode//AttributeNode[@is_py_attr = true]")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
)
def join_sep(l):
    """
    >>> def test_join_sep(l):
    ...     py = '|'.join(l)
    ...     cy = join_sep(l)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> l = text.split()
    >>> len(l)
    8
    >>> print( test_join_sep(l) )
    ab|jd|sdflk|as|sa|sadas|asdas|fsdf
    """
    result = u'|'.join(l)
    assert cython.typeof(result) == "str object", cython.typeof(result)
    return result


@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode", "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode", "//NoneCheckNode",
    "//SimpleCallNode//AttributeNode[@is_py_attr = true]"
)
@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    "//InlinedGeneratorExpressionNode"
)
def join_sep_genexpr(l):
    """
    >>> def test_join_sep_genexpr(l):
    ...     py = '|'.join(s + ' ' for s in l)
    ...     cy = join_sep_genexpr(l)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> l = text.split()
    >>> len(l)
    8
    >>> print( '<<%s>>' % test_join_sep_genexpr(l) )
    <<ab |jd |sdflk |as |sa |sadas |asdas |fsdf >>
    """
    result = u'|'.join(s + u' ' for s in l)
    assert cython.typeof(result) == "str object", cython.typeof(result)
    return result


@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode", "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode",
)
@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
    "//InlinedGeneratorExpressionNode"
)
def join_sep_genexpr_dictiter(dict d):
    """
    >>> def test_join_sep_genexpr_dictiter(d):
    ...     py = '|'.join( sorted(' '.join('%s:%s' % (k, v) for k, v in d.items()).split()) )
    ...     cy = '|'.join( sorted(join_sep_genexpr_dictiter(d).split()) )
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> l = text.split()
    >>> d = dict(zip(range(len(l)), l))
    >>> print( test_join_sep_genexpr_dictiter(d) )
    0:ab|1:jd|2:sdflk|3:as|4:sa|5:sadas|6:asdas|7:fsdf
    """
    result = u' '.join('%s:%s' % (k, v) for k, v in d.iteritems())
    assert cython.typeof(result) == "str object", cython.typeof(result)
    return result


@cython.test_assert_path_exists(
    "//PythonCapiCallNode",
)
def join_unbound(unicode sep, l):
    """
    >>> def test_join_unbound(sep, l):
    ...     py = sep.join(l)
    ...     cy = join_unbound(sep, l)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> l = text.split()
    >>> len(l)
    8
    >>> print( test_join_unbound(pipe_sep, l) )
    ab|jd|sdflk|as|sa|sadas|asdas|fsdf
    """
    join = unicode.join
    return join(sep, l)


# unicode.startswith(s, prefix, [start, [end]])

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def startswith(unicode s, sub):
    """
    >>> def test_startswith(s, sub):
    ...     py = s.startswith(sub)
    ...     cy = startswith(s, sub)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> test_startswith(text, 'ab ')
    True
    >>> test_startswith(text, 'ab X')
    False

    >>> test_startswith(text, ('ab', 'ab '))
    True
    >>> not test_startswith(text, (' ab', 'ab X'))
    True
    """
    if s.startswith(sub):
        return True
    else:
        return False

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceFromPyTypeNode",
    "//PythonCapiCallNode")
def startswith_start_end(unicode s, sub, start, end):
    """
    >>> def test_startswith_start_end(s, sub, start, end):
    ...     py = s.startswith(sub, start, end)
    ...     cy = startswith_start_end(s, sub, start, end)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> test_startswith_start_end(text, 'b ', 1, 5)
    True
    >>> test_startswith_start_end(text, 'ab ', -1000, 5000)
    True
    >>> test_startswith_start_end(text, 'b X', 1, 5)
    False

    >>> test_startswith_start_end(text, 'ab ', None, None)
    True
    >>> test_startswith_start_end(text, 'ab ', 1, None)
    False
    >>> test_startswith_start_end(text, 'b ',  1, None)
    True
    >>> test_startswith_start_end(text, 'ab ', None, 3)
    True
    >>> test_startswith_start_end(text, 'ab ', None, 2)
    False
    """
    if s.startswith(sub, start, end):
        return True
    else:
        return False


# unicode.endswith(s, prefix, [start, [end]])

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def endswith(unicode s, sub):
    """
    >>> def test_endswith(s, sub):
    ...     py = s.endswith(sub)
    ...     cy = endswith(s, sub)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> test_endswith(text, 'fsdf ')
    True
    >>> test_endswith(text, 'fsdf X')
    False

    >>> test_endswith(text, ('fsdf', 'fsdf '))
    True
    >>> test_endswith(text, ('fsdf', 'fsdf X'))
    False
    """
    if s.endswith(sub):
        return True
    else:
        return False

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceFromPyTypeNode",
    "//PythonCapiCallNode")
def endswith_start_end(unicode s, sub, start, end):
    """
    >>> def test_endswith_start_end(s, sub, start, end):
    ...     py = s.endswith(sub, start, end)
    ...     cy = endswith_start_end(s, sub, start, end)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> test_endswith_start_end(text, 'fsdf', 10, len(text)-1)
    True
    >>> test_endswith_start_end(text, 'fsdf ', 10, len(text)-1)
    False

    >>> test_endswith_start_end(text, 'fsdf ', -1000, 5000)
    True

    >>> test_endswith_start_end(text, ('fsd', 'fsdf'), 10, len(text)-1)
    True
    >>> test_endswith_start_end(text, ('fsdf ', 'fsdf X'), 10, len(text)-1)
    False

    >>> test_endswith_start_end(text, 'fsdf ', None, None)
    True
    >>> test_endswith_start_end(text, 'fsdf ', 32, None)
    True
    >>> test_endswith_start_end(text, 'fsdf ', 33, None)
    False
    >>> test_endswith_start_end(text, 'fsdf ', None, 37)
    True
    >>> test_endswith_start_end(text, 'fsdf ', None, 36)
    False
    """
    if s.endswith(sub, start, end):
        return True
    else:
        return False


# unicode.__contains__(s, sub)

@cython.test_fail_if_path_exists(
    "//CoerceFromPyTypeNode", "//AttributeNode")
@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode", "//PrimaryCmpNode")
def in_test(unicode s, substring):
    """
    >>> in_test(text, 'sa')
    True
    >>> in_test(text, 'XYZ')
    False
    >>> in_test(None, 'sa')
    Traceback (most recent call last):
    TypeError: 'NoneType' object is not iterable
    """
    return substring in s


# unicode.__concat__(s, suffix)

def concat_any(unicode s, suffix):
    """
    >>> concat(text, 'sa') == text + 'sa'  or  concat(text, 'sa')
    True
    >>> concat(None, 'sa')   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> concat(text, None)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> class RAdd(object):
    ...     def __radd__(self, other):
    ...         return 123
    >>> concat(None, 'sa')   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    assert cython.typeof(s + suffix) == 'Python object', cython.typeof(s + suffix)
    return s + suffix


def concat(unicode s, str suffix):
    """
    >>> concat(text, 'sa') == text + 'sa'  or  concat(text, 'sa')
    True
    >>> concat(None, 'sa')   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> concat(text, None)   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    >>> class RAdd(object):
    ...     def __radd__(self, other):
    ...         return 123
    >>> concat(None, 'sa')   # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...
    """
    assert cython.typeof(s + object()) == 'Python object', cython.typeof(s + object())
    assert cython.typeof(s + suffix) == "str object", cython.typeof(s + suffix)
    return s + suffix


def concat_literal_str(str suffix):
    """
    >>> concat_literal_str('sa') == 'abcsa'  or  concat_literal_str('sa')
    True
    >>> concat_literal_str(None)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...NoneType...
    """
    assert cython.typeof(u'abc' + object()) == 'Python object', cython.typeof(u'abc' + object())
    assert cython.typeof(u'abc' + suffix) == "str object", cython.typeof(u'abc' + suffix)
    return u'abc' + suffix


def concat_literal_unicode(unicode suffix):
    """
    >>> concat_literal_unicode(unicode_sa) == 'abcsa'  or  concat_literal_unicode(unicode_sa)
    True
    >>> concat_literal_unicode(None)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...NoneType...
    """
    assert cython.typeof(u'abc' + suffix) == "str object", cython.typeof(u'abc' + suffix)
    return u'abc' + suffix


# unicode.__mod__(format, values)

def mod_format(unicode s, values):
    """
    >>> mod_format(format1, 'sa') == 'abcsadef'  or  mod_format(format1, 'sa')
    True
    >>> mod_format(format2, ('XYZ', 'ABC')) == 'abcXYZdefABCghi'  or  mod_format(format2, ('XYZ', 'ABC'))
    True

    Exact TypeError message is different in PyPy
    >>> mod_format(None, 'sa')   # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for %: 'NoneType' and 'str'
    >>> class RMod(object):
    ...     def __rmod__(self, other):
    ...         return 123
    >>> mod_format(None, RMod())
    123
    """
    assert cython.typeof(s % values) == 'Python object', cython.typeof(s % values)
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
    assert cython.typeof(u'abc%sdef' % values) == "str object", cython.typeof(u'abc%sdef' % values)
    return u'abc%sdef' % values


def mod_format_tuple(*values):
    """
    >>> mod_format_tuple('sa') == 'abcsadef'  or  mod_format(format1, 'sa')
    True
    >>> mod_format_tuple()
    Traceback (most recent call last):
    TypeError: not enough arguments for format string
    """
    assert cython.typeof(u'abc%sdef' % values) == "str object", cython.typeof(u'abc%sdef' % values)
    return u'abc%sdef' % values


# unicode.find(s, sub, [start, [end]])

@cython.test_fail_if_path_exists(
    "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def find(unicode s, substring):
    """
    >>> def test_find(s, substring):
    ...     py = s.find(substring)
    ...     cy = find(s, substring)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> test_find(text, 'sa')
    16
    """
    cdef Py_ssize_t pos = s.find(substring)
    return pos

@cython.test_fail_if_path_exists(
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def find_start_end(unicode s, substring, start, end):
    """
    >>> def test_find_start_end(s, substring, start, end):
    ...     py = s.find(substring, start, end)
    ...     cy = find_start_end(s, substring, start, end)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> test_find_start_end(text, 'sa', 17, 25)
    20
    >>> test_find_start_end(text, 'sa', None, None)
    16
    >>> test_find_start_end(text, 'sa', 16, None)
    16
    >>> test_find_start_end(text, 'sa', 17, None)
    20
    >>> test_find_start_end(text, 'sa', None, 16)
    -1
    >>> test_find_start_end(text, 'sa', None, 19)
    16
    """
    cdef Py_ssize_t pos = s.find(substring, start, end)
    return pos


# unicode.rfind(s, sub, [start, [end]])

@cython.test_fail_if_path_exists(
    "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def rfind(unicode s, substring):
    """
    >>> def test_rfind(s, substring):
    ...     py = s.rfind(substring)
    ...     cy = rfind(s, substring)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> test_rfind(text, 'sa')
    20
    """
    cdef Py_ssize_t pos = s.rfind(substring)
    return pos

@cython.test_fail_if_path_exists(
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def rfind_start_end(unicode s, substring, start, end):
    """
    >>> def test_rfind_start_end(s, substring, start, end):
    ...     py = s.rfind(substring, start, end)
    ...     cy = rfind_start_end(s, substring, start, end)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> test_rfind_start_end(text, 'sa', 14, 19)
    16
    >>> test_rfind_start_end(text, 'sa', None, None)
    20
    >>> test_rfind_start_end(text, 'sa', 16, None)
    20
    >>> test_rfind_start_end(text, 'sa', 21, None)
    -1
    >>> test_rfind_start_end(text, 'sa', None, 22)
    20
    >>> test_rfind_start_end(text, 'sa', None, 21)
    16
    """
    cdef Py_ssize_t pos = s.rfind(substring, start, end)
    return pos


# unicode.count(s, sub, [start, [end]])

@cython.test_fail_if_path_exists(
    "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def count(unicode s, substring):
    """
    >>> def test_count(s, substring):
    ...     py = s.count(substring)
    ...     cy = count(s, substring)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> test_count(text, 'sa')
    2
    """
    cdef Py_ssize_t pos = s.count(substring)
    return pos

@cython.test_fail_if_path_exists(
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def count_start_end(unicode s, substring, start, end):
    """
    >>> def test_count_start_end(s, substring, start, end):
    ...     py = s.count(substring, start, end)
    ...     cy = count_start_end(s, substring, start, end)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> test_count_start_end(text, 'sa', 14, 21)
    1
    >>> test_count_start_end(text, 'sa', 14, 22)
    2
    >>> test_count_start_end(text, 'sa', None, None)
    2
    >>> test_count_start_end(text, 'sa', 14, None)
    2
    >>> test_count_start_end(text, 'sa', 17, None)
    1
    >>> test_count_start_end(text, 'sa', None, 23)
    2
    >>> test_count_start_end(text, 'sa', None, 20)
    1
    """
    cdef Py_ssize_t pos = s.count(substring, start, end)
    return pos


# unicode.replace(s, sub, repl, [maxcount])

@cython.test_fail_if_path_exists(
    "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def replace(unicode s, substring, repl):
    """
    >>> def test_replace(s, substring, repl):
    ...     py = s.replace(substring, repl)
    ...     cy = replace(s, substring, repl)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> print( test_replace(text, 'sa', 'SA') )
    ab jd  sdflk as SA  SAdas asdas fsdf\x20
    """
    return s.replace(substring, repl)

@cython.test_fail_if_path_exists(
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceFromPyTypeNode",
    "//PythonCapiCallNode")
def replace_maxcount(unicode s, substring, repl, maxcount):
    """
    >>> def test_replace_maxcount(s, substring, repl, maxcount):
    ...     py = s.replace(substring, repl, maxcount)
    ...     cy = replace_maxcount(s, substring, repl, maxcount)
    ...     assert py == cy, (py, cy)
    ...     return cy
    >>> print( test_replace_maxcount(text, 'sa', 'SA', 1) )
    ab jd  sdflk as SA  sadas asdas fsdf\x20
    """
    return s.replace(substring, repl, maxcount)


# unicode * int

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
)
@cython.test_assert_path_exists(
    "//MulNode[@is_sequence_mul = True]",
)
def multiply(unicode ustring, int mul):
    """
    >>> astr = u"abc"
    >>> ustr = u"abcüöä\\U0001F642"

    >>> print(multiply(astr, -1))
    <BLANKLINE>
    >>> print(multiply(ustr, -1))
    <BLANKLINE>

    >>> print(multiply(astr, 0))
    <BLANKLINE>
    >>> print(multiply(ustr, 0))
    <BLANKLINE>

    >>> print(multiply(astr, 1))
    abc
    >>> print(multiply(ustr, 1))
    abcüöä\U0001F642

    >>> print(multiply(astr, 2))
    abcabc
    >>> print(multiply(ustr, 2))
    abcüöä\U0001F642abcüöä\U0001F642

    >>> print(multiply(astr, 5))
    abcabcabcabcabc
    >>> print(multiply(ustr, 5))
    abcüöä\U0001F642abcüöä\U0001F642abcüöä\U0001F642abcüöä\U0001F642abcüöä\U0001F642
    """
    return ustring * mul


@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
)
@cython.test_assert_path_exists(
    "//MulNode[@is_sequence_mul = True]",
)
def multiply_call(ustring, int mul):
    """
    >>> astr = u"abc"
    >>> ustr = u"abcüöä\\U0001F642"

    >>> print(multiply_call(astr, 2))
    abcabc
    >>> print(multiply_call(ustr, 2))
    abcüöä\U0001F642abcüöä\U0001F642
    """
    return unicode(ustring) * mul


#@cython.test_fail_if_path_exists(
#    "//CoerceToPyTypeNode",
#    "//CastNode", "//TypecastNode")
#@cython.test_assert_path_exists(
#    "//PythonCapiCallNode")
def multiply_inplace(unicode ustring, int mul):
    """
    >>> astr = u"abc"
    >>> ustr = u"abcüöä\\U0001F642"

    >>> print(multiply_inplace(astr, -1))
    <BLANKLINE>
    >>> print(multiply_inplace(ustr, -1))
    <BLANKLINE>

    >>> print(multiply_inplace(astr, 0))
    <BLANKLINE>
    >>> print(multiply_inplace(ustr, 0))
    <BLANKLINE>

    >>> print(multiply_inplace(astr, 1))
    abc
    >>> print(multiply_inplace(ustr, 1))
    abcüöä\U0001F642

    >>> print(multiply_inplace(astr, 2))
    abcabc
    >>> print(multiply_inplace(ustr, 2))
    abcüöä\U0001F642abcüöä\U0001F642

    >>> print(multiply_inplace(astr, 5))
    abcabcabcabcabc
    >>> print(multiply_inplace(ustr, 5))
    abcüöä\U0001F642abcüöä\U0001F642abcüöä\U0001F642abcüöä\U0001F642abcüöä\U0001F642
    """
    ustring *= mul
    return ustring


@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
)
@cython.test_assert_path_exists(
    "//MulNode[@is_sequence_mul = True]",
)
def multiply_reversed(unicode ustring, int mul):
    """
    >>> astr = u"abc"
    >>> ustr = u"abcüöä\\U0001F642"

    >>> print(multiply_reversed(astr, -1))
    <BLANKLINE>
    >>> print(multiply_reversed(ustr, -1))
    <BLANKLINE>

    >>> print(multiply_reversed(astr, 0))
    <BLANKLINE>
    >>> print(multiply_reversed(ustr, 0))
    <BLANKLINE>

    >>> print(multiply_reversed(astr, 1))
    abc
    >>> print(multiply_reversed(ustr, 1))
    abcüöä\U0001F642

    >>> print(multiply_reversed(astr, 2))
    abcabc
    >>> print(multiply_reversed(ustr, 2))
    abcüöä\U0001F642abcüöä\U0001F642

    >>> print(multiply_reversed(astr, 5))
    abcabcabcabcabc
    >>> print(multiply_reversed(ustr, 5))
    abcüöä\U0001F642abcüöä\U0001F642abcüöä\U0001F642abcüöä\U0001F642abcüöä\U0001F642
    """
    return mul * ustring


@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
)
def unicode__mul__(unicode ustring, int mul):
    """
    >>> astr = u"abc"
    >>> ustr = u"abcüöä\\U0001F642"

    >>> print(unicode__mul__(astr, -1))
    <BLANKLINE>
    >>> print(unicode__mul__(ustr, -1))
    <BLANKLINE>

    >>> print(unicode__mul__(astr, 0))
    <BLANKLINE>
    >>> print(unicode__mul__(ustr, 0))
    <BLANKLINE>

    >>> print(unicode__mul__(astr, 1))
    abc
    >>> print(unicode__mul__(ustr, 1))
    abcüöä\U0001F642

    >>> print(unicode__mul__(astr, 2))
    abcabc
    >>> print(unicode__mul__(ustr, 2))
    abcüöä\U0001F642abcüöä\U0001F642

    >>> print(unicode__mul__(astr, 5))
    abcabcabcabcabc
    >>> print(unicode__mul__(ustr, 5))
    abcüöä\U0001F642abcüöä\U0001F642abcüöä\U0001F642abcüöä\U0001F642abcüöä\U0001F642
    """
    return ustring.__mul__(mul)
