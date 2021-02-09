# mode: run
# ticket: 3651
# tag: property, decorator

class Prop(object):
    """
    >>> p = Prop()
    >>> p.p
    Traceback (most recent call last):
    RecursionError: ...
    """
    def p(self):
        return 42

    @property
    def p(self):
        return self.p()
