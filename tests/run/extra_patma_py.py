# mode: run
# tag: pure3.10

import array

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
