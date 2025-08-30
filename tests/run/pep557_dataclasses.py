# mode: run
# tag: pep557, pure3.7

import dataclasses
from typing import Sequence


@dataclasses.dataclass
class Color:
    """
    >>> list(Color.__dataclass_fields__.keys())
    ['red', 'green', 'blue', 'alpha']
    >>> Color(1, 2, 3)
    Color(red=1, green=2, blue=3, alpha=255)
    >>> Color(1, 2, 3, 4)
    Color(red=1, green=2, blue=3, alpha=4)
    >>> Color(green=1, blue=2, red=3, alpha=40)
    Color(red=3, green=1, blue=2, alpha=40)
    """
    red: int
    green: int
    blue: int
    alpha: int = 255


@dataclasses.dataclass
class NamedColor(Color):
    """
    >>> list(NamedColor.__dataclass_fields__.keys())
    ['red', 'green', 'blue', 'alpha', 'names']
    >>> NamedColor(1, 2, 3)
    NamedColor(red=1, green=2, blue=3, alpha=255, names=[])
    >>> NamedColor(1, 2, 3, 4)
    NamedColor(red=1, green=2, blue=3, alpha=4, names=[])
    >>> NamedColor(green=1, blue=2, red=3, alpha=40)
    NamedColor(red=3, green=1, blue=2, alpha=40, names=[])
    >>> NamedColor(1, 2, 3, names=["blackish", "very dark cyan"])
    NamedColor(red=1, green=2, blue=3, alpha=255, names=['blackish', 'very dark cyan'])
    """
    names: Sequence[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass(frozen=True)
class IceCream:
    """
    >>> IceCream("vanilla")
    IceCream(flavour='vanilla', num_toppings=2)
    >>> IceCream("vanilla") == IceCream("vanilla", num_toppings=3)
    False
    >>> IceCream("vanilla") == IceCream("vanilla", num_toppings=2)
    True
    """
    flavour: str
    num_toppings: int = 2
