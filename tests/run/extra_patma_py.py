# mode: run
# tag: pure3.10

import array
import sys

__doc__ = ""

def test_array_is_sequence(x):
    """
    Because this has to be specifically special-cased on early Python versions
    >>> test_array_is_sequence(array.array('i', [0, 1, 2]))
    1
    >>> test_array_is_sequence(array.array('i', [0, 1, 2, 3, 4]))
    [0, 1, 2, 3, 4]
    """
    match x:
        case [0, y, 2]:
            return y
        case [*z]:
            return z
        case _:
            return "Not a sequence"


def test_duplicate_keys(key1, key2):
    """
    Extra to TestValueErrors in test_patma
    Cython sorts keys into literal and runtime. This tests when two runtime keys clash

    >>> test_duplicate_keys("a", "b")
    True
    >>> test_duplicate_keys("a", "a")
    Traceback (most recent call last):
    ...
    ValueError: mapping pattern checks duplicate key ('a')
    """
    class Keys:
        KEY_1 = key1
        KEY_2 = key2

    match {"a": 1, "b": 2}:
        case {Keys.KEY_1: _, Keys.KEY_2: _}:
            return True
        case _:
            return False


class PyClass(object):
    pass


class PrivateAttrLookupOuter:
    """
    CPython doesn't mangle private names in class patterns
    (so Cython should do the same)

    >>> py_class_inst = PyClass()
    >>> py_class_inst._PyClass__something = 1
    >>> py_class_inst._PrivateAttrLookupOuter__something = 2
    >>> py_class_inst.__something = 3
    >>> PrivateAttrLookupOuter().f(py_class_inst)
    3
    """
    def f(self, x):
        match x:
            case PyClass(__something=y):
                return y


if sys.version_info[0] < 3:
    class OldStyleClass:
        pass

    def test_oldstyle_class_failure(x):
        match x:
            case OldStyleClass():
                return True

    __doc__ += """
    >>> test_oldstyle_class_failure(1)
    Traceback (most recent call last):
    ...
    TypeError: called match pattern must be a new-style class.
    """
