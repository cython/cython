
class C:
    """
    >>> C().xxx(5)
    5
    >>> C().xxx()
    u'a b'
    >>> C().xxx(42)
    42
    >>> C().xxx() == 'a b'
    True
    """
    def xxx(self, p=u"a b"):
        return p
