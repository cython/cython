# cython: language_level=3
# mode: run
# tag: pure3.7, pep526, pep484

from __future__ import annotations

import sys

try:
    from typing import ClassVar
except ImportError:  # Py<=3.5
    ClassVar = {int: int}

class NotAStr:
    pass

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
    # https://github.com/cython/cython/issues/4196 and https://github.com/cython/cython/issues/4198
    not_object: float = 0.1  # Shouldn't try to create a c attribute
    lie_about_type: str = NotAStr  # Shouldn't generate a runtime type-check


class PyVanillaClass:
    """
    Before Py3.10, unannotated classes did not have '__annotations__'.

    >>> try:
    ...     a = PyVanillaClass.__annotations__
    ... except AttributeError:
    ...     assert sys.version_info < (3, 10)
    ... else:
    ...     assert sys.version_info >= (3, 10)
    ...     assert a == {}
    """
