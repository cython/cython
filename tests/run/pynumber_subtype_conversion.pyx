# mode: run
# tag: python, float, builtin


class MyFloat(float):
    """
    >>> x = MyFloat(1.0)
    >>> x
    1.0
    >>> float(x)
    12.0
    >>> x.float()
    12.0
    """
    def __float__(self):
        return 12.0

    def float(self):
        return float(self)


class MyInt(int):
    """
    >>> x = MyInt(1)
    >>> x
    1
    >>> int(x)
    2
    >>> x.int()
    2
    """
    def __int__(self):
        return 2

    def int(self):
        return int(self)
