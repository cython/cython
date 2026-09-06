# mode: run
# tag: type_inference, comprehension
# cython: language_level=3

cimport cython
from cython cimport typeof


def list_of_int_literals():
    """
    >>> list_of_int_literals()
    """
    r = [42 for _ in range(3)]
    assert typeof(r) == "list[long] object", typeof(r)


def list_of_str_calls():
    """
    >>> list_of_str_calls()
    """
    r = [str(i) for i in range(3)]
    assert typeof(r) == "list[str object] object", typeof(r)


def list_of_tuples():
    """
    The issue's example shape. Best case 'list[tuple[long, long]]' depends
    on a separate widening of TupleNode.infer_type (follow-up).

    >>> list_of_tuples()
    """
    r = [(a, a + 1) for a in range(3)]
    assert typeof(r) == "list[tuple object] object", typeof(r)


def list_of_inner_lists():
    """
    >>> list_of_inner_lists()
    """
    r = [list(x) for x in [[1], [2]]]
    assert typeof(r) == "list[list object] object", typeof(r)


def list_of_inner_dicts():
    """
    >>> list_of_inner_dicts()
    """
    r = [dict() for _ in range(2)]
    assert typeof(r) == "list[dict object] object", typeof(r)


def list_of_inner_sets():
    """
    >>> list_of_inner_sets()
    """
    r = [set() for _ in range(2)]
    assert typeof(r) == "list[set object] object", typeof(r)


def list_from_typed_loop_var():
    """
    >>> list_from_typed_loop_var()
    """
    cdef int i
    r = [i for i in range(5)]
    assert typeof(r) == "list[int] object", typeof(r)


def set_of_int_literals():
    """
    >>> set_of_int_literals()
    """
    r = {42 for _ in range(3)}
    assert typeof(r) == "set[long] object", typeof(r)


def dict_str_to_int_literal():
    """
    >>> dict_str_to_int_literal()
    """
    r = {str(i): 42 for i in range(2)}
    assert typeof(r) == "dict[str object,long] object", typeof(r)


def nested_list_of_lists():
    """
    >>> nested_list_of_lists()
    """
    r = [[a for _ in range(2)] for a in range(3)]
    assert typeof(r).startswith("list[list"), typeof(r)


def assignment_to_typed_target():
    """
    Inferred 'list[long]' must assign to a declared list[long] target.

    >>> assignment_to_typed_target()
    """
    cdef list[long] target = [42 for _ in range(3)]
    assert len(target) == 3 and target[0] == 42


def indexing_picks_up_inferred_item_type():
    """
    Inferred item type flows through indexing.

    >>> indexing_picks_up_inferred_item_type()
    """
    r = [42 for _ in range(3)]
    x = r[0]
    assert typeof(x) == "long", typeof(x)


def list_with_untyped_iter(x):
    """
    Fallback when the loop variable's type is unknown. Asserts behaviour
    only, not the inferred type, since loop-variable propagation work may
    sharpen this in future.

    >>> list_with_untyped_iter([1, 2, 3])
    [1, 2, 3]
    """
    return [a for a in x]


def walrus_in_comprehension_body():
    """
    The walrus operator binds to the enclosing function scope (PEP 572).
    Our body_env choice must not interfere with that.

    >>> walrus_in_comprehension_body()
    """
    r = [(b := a * 2) for a in range(3)]
    assert r == [0, 2, 4] and b == 4


def comp_does_not_leak_to_outer_scope():
    """
    Regression for the closure bug that drove the `self.expr_scope or env`
    fix. Mirrors list_comp_in_closure_T598.

    >>> comp_does_not_leak_to_outer_scope()
    [0, 4, 8]
    """
    x = 'abc'
    def f():
        return x
    result = [x * 2 for x in range(5) if x % 2 == 0]
    assert x == 'abc' and f() == 'abc'
    return result


async def _aiter_ints():
    for i in range(3):
        yield i


def async_comprehension():
    """
    Async comprehensions go through the same ComprehensionNode path as sync
    ones. Verify our infer_type does not break compilation or runtime for
    them.

    >>> async_comprehension()
    [0, 1, 2]
    """
    import asyncio

    async def inner():
        r = [x async for x in _aiter_ints()]
        assert typeof(r).startswith("list"), typeof(r)
        return r

    return asyncio.run(inner())
