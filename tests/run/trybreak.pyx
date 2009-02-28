__doc__ = u"""
>>> print(foo())
a
"""

# Indirectly makes sure the cleanup happens correctly on breaking.
def foo():
    for x in u"abc":
        try:
            x()
        except:
            break
    for x in u"abc":
        try:
            x()
        except:
            return x
