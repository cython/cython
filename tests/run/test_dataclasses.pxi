from cython cimport cclass
from dataclasses import (
    dataclass, field,
    fields, FrozenInstanceError, InitVar, is_dataclass, asdict, astuple, replace
)
import unittest
from unittest.mock import Mock
import pickle
import inspect
from typing import ClassVar, Any, List, Union, Tuple, Dict, Generic, TypeVar, Optional
from typing import get_type_hints
from collections import deque, OrderedDict, namedtuple
import sys

def skip_on_versions_below(version):
    def decorator(func):
        if sys.version_info >= version:
            return func
    return decorator
