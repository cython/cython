# mode: run
# ticket: 593
# tag: property, decorator

my_property = property

class Prop(object):
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
    DELETING (previously: '2')

    >>> p.my_prop
    GETTING 'my_prop'
    389

    >>> list(p.generator_prop)
    [42]
    """
    _value = None

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
        print("DELETING (previously: '%s')" % self._value)
        self._value = None

    @my_property
    def my_prop(self):
        print("GETTING 'my_prop'")
        return 389

    @property
    def generator_prop(self):
        yield 42
