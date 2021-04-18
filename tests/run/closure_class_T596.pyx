# mode: run
# tag: closures
# ticket: t596

def simple(a, b):
    """
    >>> kls = simple(1, 2)
    >>> kls().result()
    3
    """
    class Foo:
        def result(self):
            return a + b
    return Foo

def nested_classes(a, b):
    """
    >>> kls = nested_classes(1, 2)
    >>> kls().result(-3)
    0
    """
    class Foo:
        class Bar:
            def result(self, c):
                return a + b + c
    return Foo.Bar

def staff(a, b):
    """
    >>> kls = staff(1, 2)
    >>> kls.static()
    (1, 2)
    >>> kls.klass()
    ('Foo', 1, 2)
    >>> obj = kls()
    >>> obj.member()
    (1, 2)
    """
    class Foo:
        def member(self):
            return a, b
        @staticmethod
        def static():
            return a, b
        @classmethod
        def klass(cls):
            return cls.__name__, a, b
    return Foo

def nested2(a):
    """
    >>> obj = nested2(1)
    >>> f = obj.run(2)
    >>> f()
    3
    """
    class Foo:
        def run(self, b):
            def calc():
                return a + b
            return calc
    return Foo()
