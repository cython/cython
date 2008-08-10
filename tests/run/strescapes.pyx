__doc__ = u"""

>>> py_strings = [
... b'\\x1234',
... b'\\x0A12\\x0C34',
... b'\\x0A57',
... b'abc\\x12def',
... u'\\u1234',
... u'\\U00041234',
... b'\\u1234',
... b'\\U00041234',
... ]

>>> for i, (py_string, c_string) in enumerate(zip(py_strings, c_strings)):
...     assert py_string == c_string, "%d: %r != %r" % (i, py_string, c_string)

"""

import sys
if sys.version_info[0] < 3:
    __doc__ = __doc__.replace(u" b'", u" '")
else:
    __doc__ = __doc__.replace(u" u'", u" '")

c_strings = [
b'\x1234',
b'\x0A12\x0C34',
b'\x0A57',
b'abc\x12def',
u'\u1234',
u'\U00041234',
b'\u1234',
b'\U00041234',
]
