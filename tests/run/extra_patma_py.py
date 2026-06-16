# mode: run
# tag: pure3.10

from __future__ import annotations, print_function

import array
import sys

import cython

__doc__ = ""

def skip_if_no_frozendict(f):
    if cython.compiled or sys.version_info >= (3, 15):
        return f


def test_type_inference(x):
    """
    The type should not be inferred to be anything specific
    >>> test_type_inference(1)
    one 1
    >>> test_type_inference([])
    any object []
    """
    match x:
        case 1 as a:
            print("one", a)
        case a:
            print("any object", a)


def test_assignment_and_guards(x):
    """
    Tests that the flow control is right. The second case can be
    reached either by failing the pattern or by failing the guard,
    and this affects whether variables are assigned
    >>> test_assignment_and_guards([1])
    ('first', 1)
    >>> test_assignment_and_guards([1, 2])
    ('second', 1)
    >>> test_assignment_and_guards([-1, 2])
    ('second', -1)
    """
    match x:
        case [a] if a>0:
            return "first", a
        case [a, *_]:
            return "second", a


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
    >>> test_duplicate_keys("a", "a")  # doctest: +ELLIPSIS
    Traceback (most recent call last):
       ...
    ValueError: mapping pattern checks duplicate key ...
    """
    class Keys:
        KEY_1 = key1
        KEY_2 = key2

    match {"a": 1, "b": 2}:
        case {Keys.KEY_1: _, Keys.KEY_2: _}:
            return True
        case _:
            return False


def make_frozendict(*args, **kwds):
    import sys
    if sys.version_info < (3, 15):
        return dict(*args, **kwds)
    return frozendict(*args, **kwds)


def test_untyped_frozendict(arg):
    """
    >>> test_untyped_frozendict(make_frozendict(a=1, b=2))
    case ab: 1 2
    >>> test_untyped_frozendict(make_frozendict(x=1, y=2))
    case xy: 1 2 {}
    >>> test_untyped_frozendict(make_frozendict(x=1, y=2, z=3))
    case xy: 1 2 {'z': 3}
    >>> test_untyped_frozendict(make_frozendict(p=1, q=2))
    case keys: {'p': 1, 'q': 2}
    >>> test_untyped_frozendict(None)
    Unmatched
    """
    match arg:
        case {"a": a, "b": b}:
            print(f"case ab: {a} {b}")
        case {"x": x, "y": y, **keys}:
            print(f"case xy: {x} {y} {keys}")
        case {**keys}:
            print(f"case keys: {keys}")
        case _:
            print("Unmatched")


def test_typed_frozendict(arg: frozendict):
    """
    >>> test_typed_frozendict(make_frozendict(a=1, b=2))
    case ab: 1 2
    >>> test_typed_frozendict(make_frozendict(x=1, y=2))
    case xy: 1 2 {}
    >>> test_typed_frozendict(make_frozendict(x=1, y=2, z=3))
    case xy: 1 2 {'z': 3}
    >>> test_typed_frozendict(make_frozendict(p=1, q=2))
    case keys: {'p': 1, 'q': 2}
    """
    match arg:
        case {"a": a, "b": b}:
            print(f"case ab: {a} {b}")
        case {"x": x, "y": y, **keys}:
            print(f"case xy: {x} {y} {keys}")
        case {**keys}:
            print(f"case keys: {keys}")
        case _:
            print("Unmatched")


def test_typed_optional_frozendict(arg: frozendict | None):
    """
    >>> test_typed_optional_frozendict(make_frozendict(a=1, b=2))
    case ab: 1 2
    >>> test_typed_optional_frozendict(make_frozendict(x=1, y=2))
    case xy: 1 2 {}
    >>> test_typed_optional_frozendict(make_frozendict(x=1, y=2, z=3))
    case xy: 1 2 {'z': 3}
    >>> test_typed_optional_frozendict(make_frozendict(p=1, q=2))
    case keys: {'p': 1, 'q': 2}
    >>> test_typed_optional_frozendict(None)
    Unmatched
    """
    match arg:
        case {"a": a, "b": b}:
            print(f"case ab: {a} {b}")
        case {"x": x, "y": y, **keys}:
            print(f"case xy: {x} {y} {keys}")
        case {**keys}:
            print(f"case keys: {keys}")
        case _:
            print("Unmatched")

def test_dict_without_subjects(arg: dict):
    """
    dict/frozendict without subjects takes a shortcut in Cython
    that's worth testing specifically.

    >>> test_dict_without_subjects({})
    unmatched
    >>> test_dict_without_subjects({'a': 1, 'b': 2, 'c': 3})
    ab
    >>> test_dict_without_subjects({'a': 1, 'b': 2})
    ab
    """
    match arg:
        case {"a": _, "b": _}:
            print("ab")
        case _:
            print("unmatched")


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


@skip_if_no_frozendict
def match_untyped_frozendict_as_class(v):
    """
    >>> fd = make_frozendict()
    >>> match_untyped_frozendict_as_class(fd) == fd
    True
    >>> match_untyped_frozendict_as_class("not a frozendict")
    """
    match v:
        case frozendict(d):
            return d

@skip_if_no_frozendict
def match_frozendict_as_class(v: frozendict):
    """
    >>> fd = make_frozendict()
    >>> match_frozendict_as_class(fd) == fd
    True
    """
    match v:
        case frozendict(d):
            return d

@skip_if_no_frozendict
def match_optional_frozendict_as_class(v: frozendict | None):
    """
    >>> fd = make_frozendict()
    >>> match_optional_frozendict_as_class(fd) == fd
    True
    >>> match_optional_frozendict_as_class(None)
    'unmatched'
    """
    match v:
        case frozendict(d):
            return d
        case _:
            return "unmatched"


def match_mystery_class_self(arg, cls):
    """
    Most of the time, we're able to replace match-class with a
    simple known type-check (i.e. `dict(_)` becomes PyDict_Check).
    This does mean the generic test code is undertested.

    >>> match_mystery_class_self([], list)
    match
    >>> match_mystery_class_self(10, list)
    no match
    >>> class Cls:
    ...    __match_args__ = ('arg',)
    ...    arg = 1
    >>> match_mystery_class_self(Cls(), Cls)
    match
    >>> match_mystery_class_self([], Cls)
    no match
    >>> match_mystery_class_self(None, Cls)
    no match
    >>> match_mystery_class_self(None, type(None))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: ... accepts 0 positional sub-patterns (1 given)
    """
    match arg:
        case cls(_):
            print("match")
        case _:
            print("no match")

if sys.version_info >= (3, 15):
    __doc__ += """
    >>> match_mystery_class_self(frozendict(), frozendict)
    match
    >>> match_mystery_class_self({}, frozendict)
    no match
    """

class ListSubclass(list):
    __match_args__ = ("special_arg",)
    special_arg = "SPECIAL!"

def test_match_args_overrides_match_self(x):
    """
    >>> test_match_args_overrides_match_self(ListSubclass())
    'SPECIAL!'
    >>> test_match_args_overrides_match_self([])
    >>> test_match_args_overrides_match_self(None)
    """
    match x:
        case ListSubclass(v):
            return v

def test_no_memoryview_match_self(x: memoryview):
    """
    >>> test_no_memoryview_match_self(memoryview(b'123'))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: ...() accepts 0 positional sub-patterns (1 given)
    """
    match x:
        case memoryview(_):
            print("This shouldn't happen")


class DuplicateSubjectCornerCase:
    __match_args__ = ('a', 'b', 'b')  # Note duplicate b
    a = 1
    b = 2
    c = 3


def test_duplicate_subject_corner_case(x):
    """
    >>> test_duplicate_subject_corner_case(['good', DuplicateSubjectCornerCase()])
    1 2 3
    >>> test_duplicate_subject_corner_case(['bad', DuplicateSubjectCornerCase()])  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    TypeError: ...() got multiple sub-patterns for attribute 'b'
    """
    match x:
        # This works because the duplicate 'b' is never examined
        case ['good', DuplicateSubjectCornerCase(x, y, c=z) ]:
            print(x, y, z)
        case ['bad', DuplicateSubjectCornerCase(x, y, z)]:
            print("Not allowed")


class Namespace:
    pass

def test_or_evaluation_failure(x):
    """
    >>> test_or_evaluation_failure(1)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    AttributeError: ...'Namespace'... has no attribute 'fake_name'
    """
    match x:
        case Namespace.fake_name | _:
            print("Here")
