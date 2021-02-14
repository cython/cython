# mode: run
# ticket: 3651
# tag: property, decorator

class Prop(object):
    """
    >>> p = Prop()
    >>> p.p
    Traceback (most recent call last):
    RecursionError: recursion while looking up property
    """
    call_count = 0
    
    def p(self):
        return 42

    @property
    def p(self):
        self.call_count += 1
        # Pure python can detect the recursion, cython does not
        # and will segfault with a stack overflow.
        if self.call_count > 10:
            raise RecursionError("recursion while looking up property")
        return self.p()
