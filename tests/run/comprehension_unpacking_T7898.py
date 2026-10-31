# mode: run
# tag: comprehension, pure3.15
# cython: language_level=3

# cython: test_assert_c_code_has = __Pyx_PyList_Extend\(
# cython: test_assert_c_code_has = __Pyx_PySet_Update\(
# cython: test_assert_c_code_has = PyDict_Update\(

import cython

import platform

IS_GRAAL = platform.python_implementation() == 'GraalVM'


@cython.test_assert_path_exists("//ComprehensionAppendNode")
def list_unpacking():
    """
    >>> list_unpacking()
    [1, 2, 3, 4, 5]
    """
    values = ([1, 2], (), (value for value in [3, 4]), [5])
    return [*value for value in values]


def filtered_nested_list_unpacking():
    """
    >>> filtered_nested_list_unpacking()
    [0, 1, 2, 3]
    """
    groups = (([0], [1, 2]), ([3], []))
    return [*chunk for group in groups for chunk in group if chunk]


def list_expression_evaluated_once():
    """
    >>> list_expression_evaluated_once()
    ([1, -1, 2, -2, 3, -3], [1, 2, 3])
    """
    events = []

    def produce(value):
        events.append(value)
        return value, -value

    result = [*produce(value) for value in range(1, 4)]
    return result, events


def list_unpacking_assignment_expression_scope():
    """
    >>> list_unpacking_assignment_expression_scope()
    ([0, 0, 1, 2, 4, 8, 9, 18], 9)
    """
    result = [*((square := value ** 2), 2 * square) for value in range(4)]
    return result, square


@cython.test_assert_path_exists("//ComprehensionAppendNode")
def set_unpacking():
    """
    >>> set_unpacking()
    [1, 2, 3, 4]
    """
    return sorted({*value for value in ([1, 2], (2, 3), range(3, 5))})


@cython.test_assert_path_exists("//DictComprehensionAppendNode")
def dict_unpacking():
    """
    >>> dict_unpacking()
    [('a', 1), ('b', 20), ('c', 3)]
    """
    mappings = ({'a': 1, 'b': 2}, {'b': 20}, {'c': 3})
    return list({**mapping for mapping in mappings}.items())


class Mapping:
    def __init__(self, values):
        self.values = values

    def keys(self):
        return self.values.keys()

    def __getitem__(self, key):
        return self.values[key]


def dict_unpacking_mapping_protocol():
    """
    >>> dict_unpacking_mapping_protocol()
    {'answer': 42}
    """
    return {**mapping for mapping in [Mapping({'answer': 42})]}


def invalid_list_unpacking():
    """
    >>> invalid_list_unpacking()
    ('TypeError', True)
    """
    try:
        return [*value for value in [None]]
    except TypeError as exc:
        return type(exc).__name__, 'iterable' in str(exc)


def invalid_set_unpacking():
    """
    >>> invalid_set_unpacking()
    ('TypeError', True)
    """
    try:
        return {*value for value in [None]}
    except TypeError as exc:
        return type(exc).__name__, 'iterable' in str(exc)


def invalid_dict_unpacking():
    """
    >>> invalid_dict_unpacking()  if not IS_GRAAL else  ('TypeError', True)
    ('TypeError', True)
    """
    try:
        return {**mapping for mapping in [[('answer', 42)]]}
    except TypeError as exc:
        return type(exc).__name__, 'mapping' in str(exc)


async def async_values():
    yield [1, 2]
    yield [3]


async def async_list_unpacking():
    return [*value async for value in async_values()]


def run_async_list_unpacking():
    """
    >>> run_async_list_unpacking()
    [1, 2, 3]
    """
    import asyncio
    return asyncio.run(async_list_unpacking())
