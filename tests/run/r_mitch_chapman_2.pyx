__doc__ = """
    >>> boolExpressionsFail()
    'Not 2b'
"""

def boolExpressionsFail():
    dict = {1: 1}
    if not dict.has_key("2b"):
        return "Not 2b"
    else:
        return "2b?"
