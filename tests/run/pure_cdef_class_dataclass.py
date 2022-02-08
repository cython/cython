# mode: run
# tag: dataclass, pure3.7

from __future__ import print_function

import cython

@cython.dataclasses.dataclass(order=True, unsafe_hash=True)
@cython.cclass
class MyDataclass:
    """
    >>> sorted(list(MyDataclass.__dataclass_fields__.keys()))
    ['a', 'self']
    >>> inst1 = MyDataclass(2.0, ['a', 'b'])
    >>> print(inst1)
    MyDataclass(a=2.0, self=['a', 'b'])
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
    """

    a: int = 1
    self: list = cython.dataclasses.field(default_factory=list, hash=False)  # test that arguments of init don't conflict
