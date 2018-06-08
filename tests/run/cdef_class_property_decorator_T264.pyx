# mode: run
# ticket: 264
# tag: property, decorator

my_property = property

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
    >>> p.my_prop
    GETTING '2' via my_prop
    2
    >>> del p.prop
    DELETING '2'
    >>> p.prop
    GETTING 'None'
    >>> list(p.generator_prop)
    [42]
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

    @my_property
    def my_prop(self):
        print("GETTING '%s' via my_prop" % self._value)
        return self._value

    @property
    def generator_prop(self):
        yield 42
