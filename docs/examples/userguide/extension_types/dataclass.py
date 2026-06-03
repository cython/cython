import cython
try:
    import typing
    import dataclasses
except ImportError:
    pass  # The modules don't actually have to exists for Cython to use them as annotations

@dataclasses.dataclass
@cython.cclass
class MyDataclass:
    # fields can be declared using annotations
    a: cython.int = 0
    b: double = dataclasses.field(default_factory = lambda: 10, repr=False)


    c: str = 'hello'


    # typing.InitVar and typing.ClassVar also work
    d: dataclasses.InitVar[double] = 5
    e: typing.ClassVar[list] = []
