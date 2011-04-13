# mode:run
# tag: class, scope

class MethodRedef(object):
    """
    >>> MethodRedef().a(5)
    7
    """

    def a(self, i):
        return i+1

    def a(self, i):
        return i+2
