# -*- coding: utf-8 -*-

cimport cython

import sys

PY_VERSION = sys.version_info

text = u'ab jd  sdflk as sa  sadas asdas fsdf '
sep = u'  '

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
    >>> print_all( text.split() )
    ab
    jd
    sdflk
    as
    sa
    sadas
    asdas
    fsdf
    >>> print_all( split(text) )
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
    >>> print_all( text.split(sep) )
    ab jd
    sdflk as sa
    sadas asdas fsdf 
    >>> print_all( split_sep(text, sep) )
    ab jd
    sdflk as sa
    sadas asdas fsdf 
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
    >>> print_all( text.split(sep, 1) )
    ab jd
    sdflk as sa  sadas asdas fsdf 
    >>> print_all( split_sep_max(text, sep, 1) )
    ab jd
    sdflk as sa  sadas asdas fsdf 
    """
    return s.split(sep, max)

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode", "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def split_sep_max_int(unicode s, sep):
    """
    >>> print_all( text.split(sep, 1) )
    ab jd
    sdflk as sa  sadas asdas fsdf 
    >>> print_all( split_sep_max_int(text, sep) )
    ab jd
    sdflk as sa  sadas asdas fsdf 
    """
    return s.split(sep, 1)


# unicode.splitlines(s, [keepends])

@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def splitlines(unicode s):
    """
    >>> len(multiline_text.splitlines())
    3
    >>> print_all( multiline_text.splitlines() )
    ab jd
    sdflk as sa
    sadas asdas fsdf 
    >>> len(splitlines(multiline_text))
    3
    >>> print_all( splitlines(multiline_text) )
    ab jd
    sdflk as sa
    sadas asdas fsdf 
    """
    return s.splitlines()

@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def splitlines_keep(unicode s, keep):
    """
    >>> len(multiline_text.splitlines(True))
    3
    >>> print_all( multiline_text.splitlines(True) )
    ab jd
    <BLANKLINE>
    sdflk as sa
    <BLANKLINE>
    sadas asdas fsdf 
    >>> len(splitlines_keep(multiline_text, True))
    3
    >>> print_all( splitlines_keep(multiline_text, True) )
    ab jd
    <BLANKLINE>
    sdflk as sa
    <BLANKLINE>
    sadas asdas fsdf 
    """
    return s.splitlines(keep)

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode", "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def splitlines_keep_bint(unicode s):
    """
    >>> len(multiline_text.splitlines(True))
    3
    >>> print_all( multiline_text.splitlines(True) )
    ab jd
    <BLANKLINE>
    sdflk as sa
    <BLANKLINE>
    sadas asdas fsdf 
    >>> print_all( multiline_text.splitlines(False) )
    ab jd
    sdflk as sa
    sadas asdas fsdf 
    >>> len(splitlines_keep_bint(multiline_text))
    7
    >>> print_all( splitlines_keep_bint(multiline_text) )
    ab jd
    <BLANKLINE>
    sdflk as sa
    <BLANKLINE>
    sadas asdas fsdf 
    --
    ab jd
    sdflk as sa
    sadas asdas fsdf 
    """
    return s.splitlines(True) + ['--'] + s.splitlines(False)


# unicode.join(s, iterable)

pipe_sep = u'|'

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode", "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode",
    "//SimpleCallNode//AttributeNode[@is_py_attr = true]")
@cython.test_assert_path_exists(
    "//SimpleCallNode",
    "//SimpleCallNode//NoneCheckNode",
    "//SimpleCallNode//AttributeNode[@is_py_attr = false]")
def join(unicode sep, l):
    """
    >>> l = text.split()
    >>> len(l)
    8
    >>> print( pipe_sep.join(l) )
    ab|jd|sdflk|as|sa|sadas|asdas|fsdf
    >>> print( join(pipe_sep, l) )
    ab|jd|sdflk|as|sa|sadas|asdas|fsdf
    """
    return sep.join(l)

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode", "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode", "//NoneCheckNode",
    "//SimpleCallNode//AttributeNode[@is_py_attr = true]")
@cython.test_assert_path_exists(
    "//SimpleCallNode",
    "//SimpleCallNode//AttributeNode[@is_py_attr = false]")
def join_sep(l):
    """
    >>> l = text.split()
    >>> len(l)
    8
    >>> print( '|'.join(l) )
    ab|jd|sdflk|as|sa|sadas|asdas|fsdf
    >>> print( join_sep(l) )
    ab|jd|sdflk|as|sa|sadas|asdas|fsdf
    """
    return u'|'.join(l)

@cython.test_assert_path_exists(
    "//SimpleCallNode",
    "//SimpleCallNode//NameNode")
def join_unbound(unicode sep, l):
    """
    >>> l = text.split()
    >>> len(l)
    8
    >>> print( pipe_sep.join(l) )
    ab|jd|sdflk|as|sa|sadas|asdas|fsdf
    >>> print( join_unbound(pipe_sep, l) )
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
    >>> text.startswith('ab ')
    True
    >>> startswith(text, 'ab ')
    'MATCH'
    >>> text.startswith('ab X')
    False
    >>> startswith(text, 'ab X')
    'NO MATCH'

    >>> PY_VERSION < (2,5) or text.startswith(('ab', 'ab '))
    True
    >>> startswith(text, ('ab', 'ab '))
    'MATCH'
    >>> PY_VERSION < (2,5) or not text.startswith((' ab', 'ab X'))
    True
    >>> startswith(text, (' ab', 'ab X'))
    'NO MATCH'
    """
    if s.startswith(sub):
        return 'MATCH'
    else:
        return 'NO MATCH'

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceFromPyTypeNode",
    "//PythonCapiCallNode")
def startswith_start_end(unicode s, sub, start, end):
    """
    >>> text.startswith('b ', 1, 5)
    True
    >>> startswith_start_end(text, 'b ', 1, 5)
    'MATCH'
    >>> text.startswith('ab ', -1000, 5000)
    True
    >>> startswith_start_end(text, 'ab ', -1000, 5000)
    'MATCH'
    >>> text.startswith('b X', 1, 5)
    False
    >>> startswith_start_end(text, 'b X', 1, 5)
    'NO MATCH'
    """
    if s.startswith(sub, start, end):
        return 'MATCH'
    else:
        return 'NO MATCH'


# unicode.endswith(s, prefix, [start, [end]])

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
    "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//PythonCapiCallNode")
def endswith(unicode s, sub):
    """
    >>> text.endswith('fsdf ')
    True
    >>> endswith(text, 'fsdf ')
    'MATCH'
    >>> text.endswith('fsdf X')
    False
    >>> endswith(text, 'fsdf X')
    'NO MATCH'

    >>> PY_VERSION < (2,5) or text.endswith(('fsdf', 'fsdf '))
    True
    >>> endswith(text, ('fsdf', 'fsdf '))
    'MATCH'
    >>> PY_VERSION < (2,5) or not text.endswith(('fsdf', 'fsdf X'))
    True
    >>> endswith(text, ('fsdf', 'fsdf X'))
    'NO MATCH'
    """
    if s.endswith(sub):
        return 'MATCH'
    else:
        return 'NO MATCH'

@cython.test_fail_if_path_exists(
    "//CoerceToPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceFromPyTypeNode",
    "//PythonCapiCallNode")
def endswith_start_end(unicode s, sub, start, end):
    """
    >>> text.endswith('fsdf', 10, len(text)-1)
    True
    >>> endswith_start_end(text, 'fsdf', 10, len(text)-1)
    'MATCH'
    >>> text.endswith('fsdf ', 10, len(text)-1)
    False
    >>> endswith_start_end(text, 'fsdf ', 10, len(text)-1)
    'NO MATCH'

    >>> text.endswith('fsdf ', -1000, 5000)
    True
    >>> endswith_start_end(text, 'fsdf ', -1000, 5000)
    'MATCH'

    >>> PY_VERSION < (2,5) or text.endswith(('fsd', 'fsdf'), 10, len(text)-1)
    True
    >>> endswith_start_end(text, ('fsd', 'fsdf'), 10, len(text)-1)
    'MATCH'
    >>> PY_VERSION < (2,5) or not text.endswith(('fsdf ', 'fsdf X'), 10, len(text)-1)
    True
    >>> endswith_start_end(text, ('fsdf ', 'fsdf X'), 10, len(text)-1)
    'NO MATCH'
    """
    if s.endswith(sub, start, end):
        return 'MATCH'
    else:
        return 'NO MATCH'


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


# unicode.find(s, sub, [start, [end]])

@cython.test_fail_if_path_exists(
    "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceToPyTypeNode",
    "//PythonCapiCallNode")
def find(unicode s, substring):
    """
    >>> text.find('sa')
    16
    >>> find(text, 'sa')
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
    >>> text.find('sa', 17, 25)
    20
    >>> find_start_end(text, 'sa', 17, 25)
    20
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
    >>> text.rfind('sa')
    20
    >>> rfind(text, 'sa')
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
    >>> text.rfind('sa', 14, 19)
    16
    >>> rfind_start_end(text, 'sa', 14, 19)
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
    >>> text.count('sa')
    2
    >>> count(text, 'sa')
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
    >>> text.count('sa', 14, 21)
    1
    >>> text.count('sa', 14, 22)
    2
    >>> count_start_end(text, 'sa', 14, 21)
    1
    >>> count_start_end(text, 'sa', 14, 22)
    2
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
    >>> print( text.replace('sa', 'SA') )
    ab jd  sdflk as SA  SAdas asdas fsdf 
    >>> print( replace(text, 'sa', 'SA') )
    ab jd  sdflk as SA  SAdas asdas fsdf 
    """
    return s.replace(substring, repl)

@cython.test_fail_if_path_exists(
    "//CastNode", "//TypecastNode")
@cython.test_assert_path_exists(
    "//CoerceFromPyTypeNode",
    "//PythonCapiCallNode")
def replace_maxcount(unicode s, substring, repl, maxcount):
    """
    >>> print( text.replace('sa', 'SA', 1) )
    ab jd  sdflk as SA  sadas asdas fsdf 
    >>> print( replace_maxcount(text, 'sa', 'SA', 1) )
    ab jd  sdflk as SA  sadas asdas fsdf 
    """
    return s.replace(substring, repl, maxcount)
