__doc__ = u"""
  >>> test_str(1)
  b'b'

  >>> test_unicode_ascii(2)
  u'c'
  >>> test_unicode(2)
  u'\u00e4'

  >>> test_int_list(2)
  3
  >>> test_str_list(1)
  b'bcd'

  >>> test_int_tuple(2)
  3
  >>> test_str_tuple(0)
  b'a'
  >>> test_mix_tuple(1)
  b'abc'
  >>> test_mix_tuple(0)
  1
"""

import sys
if sys.version_info[0] < 3:
    __doc__ = __doc__.replace("  b'", "  '")
else:
    __doc__ = __doc__.replace("  u'", "  '")


def test_str(n):
    return "abcd"[n]

def test_unicode_ascii(n):
    return u"abcd"[n]

def test_unicode(n):
    return u"\u00fc\u00f6\u00e4"[n]

def test_int_list(n):
    return [1,2,3,4][n]

def test_str_list(n):
    return ["a","bcd","efg","xyz"][n]

def test_int_tuple(n):
    return (1,2,3,4)[n]

def test_str_tuple(n):
    return ("a","bcd","efg","xyz")[n]

def test_mix_tuple(n):
    return (1, "abc", u"\u00fc", 1.1)[n]
