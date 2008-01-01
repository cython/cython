__doc__ = """
    >>> C().xxx(5)
    5
    >>> C().xxx()
    'a b'
    >>> C().xxx(42)
    42
    >>> C().xxx()
    'a b'
"""

class C:
    def xxx(self, p="a b"):
        return p
