# mode: run
# ticket: 264
# tag: property, decorator

cdef class Prop:
    """
    >>> p = Prop()
    >>> p.prop
    GETTING 'None'
    >>> p.prop = 1
    SETTING '1' (previously: 'None')
    >>> p.prop
    GETTING '1'
    1
    >>> p.prop = 2
    SETTING '2' (previously: '1')
    >>> p.prop
    GETTING '2'
    2
    >>> del p.prop
    DELETING '2'
    >>> p.prop
    GETTING 'None'
    >>> p.alias_prop
    GETTING 'None'
    """
    cdef _value
    def __init__(self):
        self._value = None

    @property
    def prop(self):
        print("FAIL")
        return 0

    @prop.getter
    def prop(self):
        print("FAIL")

    @property
    def prop(self):
        print("GETTING '%s'" % self._value)
        return self._value

    @prop.setter
    def prop(self, value):
        print("SETTING '%s' (previously: '%s')" % (value, self._value))
        self._value = value

    @prop.deleter
    def prop(self):
        print("DELETING '%s'" % self._value)
        self._value = None

    alias_prop = prop
