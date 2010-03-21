# -*- coding: utf-8 -*-

cimport cython

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
    "//CoerceFromPyTypeNode")
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
# boolean conversion isn't currently smart enough for this ...
#    "//CoerceToPyTypeNode", "//CoerceFromPyTypeNode",
    "//CastNode", "//TypecastNode")
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
