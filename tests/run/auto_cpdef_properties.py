# cython: auto_cpdef=True
# mode:run
# tag: directive,auto_cpdef,property

from cython import cclass, int


@cclass
class SimpleProperty:
    """Test basic @property with setter no type annotations"""

    def __init__(self):
        self._x = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value


def test_simple_property() -> None:
    """
    >>> test_simple_property()
    """
    obj = SimpleProperty()
    assert obj.x == 0
    obj.x = 42
    assert obj.x == 42


@cclass
class SimpleProperty2:
    """Test basic @property with setter and typing"""

    _x: int

    def __init__(self) -> None:
        self._x = 0

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value


def test_simple_property2() -> None:
    """
    >>> test_simple_property2()
    """
    obj = SimpleProperty2()
    assert obj.x == 0
    obj.x = 42
    assert obj.x == 42


@cclass
class SimpleProperty3:
    """Test basic @property readonly"""

    def __init__(self) -> None:
        self._x: int = 43

    @property
    def x(self) -> int:
        return self._x


def test_simple_property3() -> None:
    """
    >>> test_simple_property3()
    """
    obj = SimpleProperty3()
    assert obj.x == 43



@cclass
class SimpleProperty4(SimpleProperty):
    """Test basic @property with hierarchy"""

    def __init__(self) -> None:
        super().__init__()
        self._x = 43

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value + 2


def test_simple_property4() -> None:
    """
    >>> test_simple_property4()
    """
    obj = SimpleProperty4()
    assert obj.x == 43
    obj.x = 42
    assert obj.x == 44


@cclass
class SimpleProperty5:
    """Test basic @property non-eligible for auto-cpdef"""

    def __init__(self) -> None:
        self._x = [1,2,7,4]

    @property
    def x(self) -> int:
        return 1 if any(x > 5 for x in self._x) else 0


def test_simple_property5() -> None:
    """
    >>> test_simple_property5()
    """
    obj = SimpleProperty5()
    assert obj.x == 1
