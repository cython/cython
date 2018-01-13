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
