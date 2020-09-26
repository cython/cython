# cython: language_level=3
# mode: run
# tag: pure3.7, pep526, pep484

from __future__ import annotations

try:
    from typing import ClassVar
except ImportError:  # Py3.5
    try:
        from typing import Optional as ClassVar  # Good enough for jazz.
    except ImportError:   # Py<=3.4
        from collections import defaultdict as ClassVar  # Now we're hacking!


class PyAnnotatedClass:
    """
    >>> PyAnnotatedClass.__annotations__["CLASS_VAR"]
    'ClassVar[int]'
    >>> PyAnnotatedClass.__annotations__["obj"]
    'str'
    >>> PyAnnotatedClass.__annotations__["literal"]
    "'int'"
    >>> PyAnnotatedClass.__annotations__["recurse"]
    "'PyAnnotatedClass'"
    >>> PyAnnotatedClass.__annotations__["default"]
    'bool'
    >>> PyAnnotatedClass.CLASS_VAR
    1
    >>> PyAnnotatedClass.default
    False
    >>> PyAnnotatedClass.obj
    Traceback (most recent call last):
      ...
    AttributeError: type object 'PyAnnotatedClass' has no attribute 'obj'
    """
    CLASS_VAR: ClassVar[int] = 1
    obj: str
    literal: "int"
    recurse: "PyAnnotatedClass"
    default: bool = False


class PyVanillaClass:
    """
    >>> PyVanillaClass.__annotations__
    Traceback (most recent call last):
      ...
    AttributeError: type object 'PyVanillaClass' has no attribute '__annotations__'
    """
