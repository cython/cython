__doc__ = u"""
    >>> eggs()
    Args: 1 2 3
    Args: buckle my shoe
"""

def spam(a, b, c):
    print "Args:", a, b, c

def eggs():
    spam(*(1,2,3))
    spam(*["buckle","my","shoe"])

