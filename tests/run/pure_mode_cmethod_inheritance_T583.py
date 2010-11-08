class Base(object):
    '''
    >>> base = Base()
    >>> print(base.method())
    Base
    '''
    def method(self):
        return "Base"


class Derived(Base):
    '''
    >>> derived = Derived()
    >>> print(derived.method())
    Derived
    '''
    def method(self):
        return "Derived"
