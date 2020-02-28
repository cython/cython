# mode: run
# ticket: 264
# tag: property, decorator

cimport cython

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

@cython.test_assert_path_exists("//PropertyNode")
cdef class HasEfficientProp:
    """
    Just a test that "a" is actually transformed into a built-in-type property

    The exact output of the type-test may be version specific so it isn't an issue
    if it needs changing in future
    >>> type(HasEfficientProp.a).__name__
    'getset_descriptor'
    """
    @property
    def a(self):
        return True
    @a.setter
    def a(self, value):
        pass
    @a.deleter
    def a(self):
        pass

def really_boring_decorator(f):
    return f

@cython.test_fail_if_path_exists("//PropertyNode")
cdef class CantHaveEfficientProp:
    """
    Even one function that fits the pattern will prevent this from working
    >>> type(CantHaveEfficientProp.a).__name__
    'property'
    >>> inst = CantHaveEfficientProp()
    >>> inst.a = 2
    >>> print(inst.a)
    2
    >>> inst.b = 2
    >>> print(inst.b)
    2
    """
    cdef int _a, _b

    @property
    def a(self):
        return self._a
    @a.setter
    @really_boring_decorator
    def a(self, value):
        self._a = value
    @a.deleter
    def a(self):
        self._a = -1

    @really_boring_decorator
    @property
    def b(self):
        return self._b
    @b.setter
    def b(self, value):
        self._b = value
    @b.deleter
    def b(self):
        self._b = -1
