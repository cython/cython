# mode: run
# tag: dataclass, pure3.7

from __future__ import print_function

import cython

# cython.dataclasses implicitly implies cclass
@cython.dataclasses.dataclass(order=True, unsafe_hash=True)
class MyDataclass:
    """
    >>> sorted(list(MyDataclass.__dataclass_fields__.keys()))
    ['a', 'self']
    >>> inst1 = MyDataclass(2, ['a', 'b'])
    >>> print(inst1)
    MyDataclass(a=2, self=['a', 'b'])
    >>> inst2 = MyDataclass()
    >>> print(inst2)
    MyDataclass(a=1, self=[])
    >>> inst1 == inst2
    False
    >>> inst1 > inst2
    True
    >>> inst2 == MyDataclass()
    True
    >>> hash(inst1) != id(inst1)
    True
    >>> inst1.func_with_annotations(2.0)
    4.0
    """

    a: int = 1
    self: list = cython.dataclasses.field(default_factory=list, hash=False)  # test that arguments of init don't conflict

    def func_with_annotations(self, b: float):
        c: float = b
        return self.a * c


class DummyObj:
    def __repr__(self):
        return "DummyObj()"


@cython.dataclasses.dataclass
@cython.cclass
class NoInitFields:
    """
    >>> NoInitFields()
    NoInitFields(has_default=DummyObj(), has_factory='From a lambda', neither=None)
    >>> NoInitFields().has_default is NoInitFields().has_default
    True

    >>> NoInitFields(1)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: NoInitFields.__init__() takes 1 positional argument but 2 were given

    >>> NoInitFields(has_default=1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...has_default...
    >>> NoInitFields(has_factory=1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...has_factory...
    >>> NoInitFields(neither=1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    TypeError: ...neither...
    """
    has_default : object = cython.dataclasses.field(default=DummyObj(), init=False)
    has_factory : object = cython.dataclasses.field(default_factory=lambda: "From a lambda", init=False)
    # Cython will default-initialize to None
    neither : object = cython.dataclasses.field(init=False)

    def __post_init__(self):
        if not cython.compiled:
            # Cython will default-initialize this to None, while Python won't
            # and not initializing it will mess up repr
            assert not hasattr(self, "neither")
            self.neither = None


@cython.dataclasses.dataclass
class NonInitDefaultArgument:
    """
    >>> NonInitDefaultArgument(1.0, "hello")
    NonInitDefaultArgument(x=1.0, y=10, z='hello')
    """
    x: float
    y: int = cython.dataclasses.field(default=10, init=False)
    z: str  # This is allowed despite following a default argument, because the default argument isn't in init
