# mode: run
# cython: language_level=2

__doc__ = u"""
>>> print(spam)
eggseggseggseggs
>>> print(uspam)
eggseggseggseggs
>>> print(bspam.decode('ascii'))
eggseggseggseggs

>>> print(grail)
tomatotomatotomatotomatotomatotomatotomato
>>> len(grail_long)
4200
>>> print(ugrail)
tomatotomatotomatotomatotomatotomatotomato
>>> len(ugrail_long)
4200
>>> print(bgrail.decode('ascii'))
tomatotomatotomatotomatotomatotomatotomato
>>> len(bgrail_long)
4200
"""

bspam = b"eggs" * 4
bgrail = 7 * b"tomato"
bgrail_long = 700 * b"tomato"

spam = "eggs" * 4
grail = 7 * "tomato"
grail_long = 700 * "tomato"

uspam = u"eggs" * 4
ugrail = 7 * u"tomato"
ugrail_long = 700 * u"tomato"

cimport cython

@cython.test_assert_path_exists(
    "//UnicodeNode[@value = '-----']",
    "//UnicodeNode[@bytes_value = b'-----']",
    "//BytesNode[@value = b'-----']",
)
def gh3951():
    """
    Bug occurred with language_level=2 and affected StringNode.value
    >>> gh3951()
    ('-----', b'-----')
    """
    return "-"*5, b"-"*5
