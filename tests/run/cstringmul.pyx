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

@cython.test_assert_path_exists("//StringNode[@value = '-----']")
@cython.test_assert_path_exists("//StringNode[@unicode_value = '-----']")
def gh3951():
    """
    Bug occurs with language_level=2 and affects StringNode.value
    >>> gh3951()
    '-----'
    """
    return "-"*5
