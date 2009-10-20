__doc__ = u"""
    >>> boolExpressionsFail()
    'Not 2b'
"""

def boolExpressionsFail():
    dict = {1: 1}
    if not "2b" in dict:
        return "Not 2b"
    else:
        return "2b?"
