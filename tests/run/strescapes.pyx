__doc__ = u"""

>>> py_strings = [
... b'\\x1234',
... b'\\x0A12\\x0C34',
... b'\\x0A57',
... b'\\x0A',
... b'\\'',
... b"\\'",
... b"\\"",
... b'\\"',
... b'abc\\x12def',
... '\\u1234',
... '\\U00001234',
... b'\\u1234',
... b'\\U00001234',
... b'\\n\\r\\t',
... b':>',
... b'??>',
... b'\\0\\0\\0',
... ]

>>> for i, (py_string, (c_string, length)) in enumerate(zip(py_strings, c_strings)):
...     assert py_string == c_string, "%d: %r != %r" % (i, py_string, c_string)
...     assert len(py_string) == length, (
...         "%d: wrong length of %r, got %d, expected %d" % (
...             i, py_string, len(py_string), length))
...     assert len(c_string) == length, (
...         "%d: wrong length of %r, got %d, expected %d" % (
...             i, c_string, len(c_string), length))

"""

c_strings = [
(b'\x1234', 3),
(b'\x0A12\x0C34', 6),
(b'\x0A57', 3),
(b'\x0A', 1),
(b'\'', 1),
(b"\'", 1),
(b"\"", 1),
(b'\"', 1),
(b'abc\x12def', 7),
(u'\u1234', 1),
(u'\U00001234', 1),
(b'\u1234', 6),
(b'\U00001234', 10),
(b'\n\r\t', 3),
(b':>', 2),
(b'??>', 3),
(b'\0\0\0', 3),
]
