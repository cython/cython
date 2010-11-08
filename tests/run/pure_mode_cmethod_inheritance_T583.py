class Base(object):
    '''
    >>> base = Base()
    >>> print(base.noargs())
    Base
    >>> print(base.int_arg(1))
    Base
    >>> print(base._class())
    Base
    '''
    def noargs(self):
        return "Base"
    def int_arg(self, i):
        return "Base"
    @classmethod
    def _class(tp):
        return "Base"


class Derived(Base):
    '''
    >>> derived = Derived()
    >>> print(derived.noargs())
    Derived
    >>> print(derived.int_arg(1))
    Derived
    >>> print(derived._class())
    Derived
    '''
    def noargs(self):
        return "Derived"
    def int_arg(self, i):
        return "Derived"
    @classmethod
    def _class(tp):
        return "Derived"


class DerivedDerived(Derived):
    '''
    >>> derived = DerivedDerived()
    >>> print(derived.noargs())
    DerivedDerived
    >>> print(derived.int_arg(1))
    DerivedDerived
    >>> print(derived._class())
    DerivedDerived
    '''
    def noargs(self):
        return "DerivedDerived"
    def int_arg(self, i):
        return "DerivedDerived"
    @classmethod
    def _class(tp):
        return "DerivedDerived"


class Derived2(Base):
    '''
    >>> derived = Derived2()
    >>> print(derived.noargs())
    Derived2
    >>> print(derived.int_arg(1))
    Derived2
    >>> print(derived._class())
    Derived2
    '''
    def noargs(self):
        return "Derived2"
    def int_arg(self, i):
        return "Derived2"
    @classmethod
    def _class(tp):
        return "Derived2"
