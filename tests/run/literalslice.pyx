__doc__ = u"""
  >>> test_str(1)
  'b'

  >>> test_unicode_ascii(2)
  'c'
  >>> test_unicode(2) == '\u00e4'
  True

  >>> test_int_list(2)
  3
  >>> test_str_list(1)
  'bcd'

  >>> test_int_tuple(2)
  3
  >>> test_str_tuple(0)
  'a'
  >>> test_mix_tuple(1)
  'abc'
  >>> test_mix_tuple(0)
  1
"""

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
