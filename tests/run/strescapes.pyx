__doc__ = u"""

>>> py_strings = [
... '\\x1234',
... '\\x0A12\\x0C34',
... '\\x0A57',
... 'abc\\x12def',
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
    __doc__ = __doc__.replace(" b'", " '")
else:
    __doc__ = __doc__.replace(" u'", " '")

c_strings = [
'\x1234',
'\x0A12\x0C34',
'\x0A57',
'abc\x12def',
u'\u1234',
u'\U00041234',
b'\u1234',
b'\U00041234',
]
