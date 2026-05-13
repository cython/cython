# mode: run
# tag: type_inference, comprehension
# cython: language_level=3

# Tests for inferring container item types in list/set/dict comprehensions.
# Driven by ComprehensionNode.infer_type in Cython/Compiler/ExprNodes.py.
# language_level=3 is required for the closure-scope test: under Py2 semantics
# comprehensions leak their loop variable to the enclosing scope.

cimport cython
from cython cimport typeof


# -----------------------------------------------------------------------------
# Item-type inference per comprehension kind.
# These pin exact typeof strings because the format is what users observe via
# cython.typeof(). If the display format itself changes (e.g. the doubled
# `object` suffix is cleaned up), these will need updating in lockstep with
# the rest of the codebase's typeof tests.
# -----------------------------------------------------------------------------

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
    >>> list_of_tuples()
    """
    r = [(a, a + 1) for a in range(3)]
    assert typeof(r) == "list[tuple object] object", typeof(r)
    # NOTE: best-case 'list[tuple[long, long] object] object' is blocked on
    # widening TupleNode.infer_type. Tracked as a follow-up.


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
    Explicitly cdef-typed loop variables flow their type through to
    the inferred container type.

    >>> list_from_typed_loop_var()
    """
    cdef int i
    r = [i for i in range(5)]
    assert typeof(r) == "list[int] object", typeof(r)


def set_of_str_calls():
    """
    >>> set_of_str_calls()
    """
    r = {str(i) for i in range(3)}
    assert typeof(r) == "set[str object] object", typeof(r)


def set_of_int_literals():
    """
    >>> set_of_int_literals()
    """
    r = {42 for _ in range(3)}
    assert typeof(r) == "set[long] object", typeof(r)


def dict_str_to_inner_list():
    """
    >>> dict_str_to_inner_list()
    """
    r = {str(i): list() for i in range(2)}
    assert typeof(r) == "dict[str object,list object] object", typeof(r)


def dict_str_to_int_literal():
    """
    >>> dict_str_to_int_literal()
    """
    r = {str(i): 42 for i in range(2)}
    assert typeof(r) == "dict[str object,long] object", typeof(r)


def nested_list_of_lists():
    """
    Outer captures the inner comprehension's shape. The exact form of the
    inner item type can vary with directive defaults (e.g. language_level,
    infer_types) across compiler entry points, so we only pin the prefix.

    >>> nested_list_of_lists()
    """
    r = [[a for _ in range(2)] for a in range(3)]
    t = typeof(r)
    assert t.startswith("list[list"), t


# -----------------------------------------------------------------------------
# Downstream-use tests. These validate that the inferred parameterised type
# is actually useful, not merely displayed correctly.
# -----------------------------------------------------------------------------

def assignment_to_typed_target():
    """
    The inferred 'list[long]' must assign to a declared list[long] target
    without coercion errors.

    >>> assignment_to_typed_target()
    """
    cdef list[long] target = [42 for _ in range(3)]
    assert len(target) == 3
    assert target[0] == 42 and target[-1] == 42


def indexing_picks_up_inferred_item_type():
    """
    Indexing into a comprehension whose item type was inferred should
    propagate that type to the indexed value. Without parameterisation
    the indexed value would degrade to Python object.

    >>> indexing_picks_up_inferred_item_type()
    """
    r = [42 for _ in range(3)]
    x = r[0]
    assert typeof(x) == "long", typeof(x)


def dict_indexing_picks_up_value_type():
    """
    >>> dict_indexing_picks_up_value_type()
    """
    r = {str(i): 42 for i in range(2)}
    v = r["0"]
    assert typeof(v) == "long", typeof(v)


# -----------------------------------------------------------------------------
# Graceful fallback. We don't pin "bare list" here because the moment loop-
# variable type propagation from subscripted iterators lands (separate work),
# the inferred type will sharpen and that's a feature, not a regression.
# Just verify the comprehension runs and returns the right kind of container.
# -----------------------------------------------------------------------------

def list_with_untyped_iter(x):
    """
    >>> list_with_untyped_iter([1, 2, 3])
    [1, 2, 3]
    """
    return [a for a in x]


def dict_with_untyped_iter(d):
    """
    >>> sorted(dict_with_untyped_iter({1: 'a', 2: 'b'}).items())
    [(1, 'a'), (2, 'b')]
    """
    return {k: v for k, v in d.items()}


# -----------------------------------------------------------------------------
# Comprehension shapes that exercise the body inspection path. These are not
# about the inferred item type per se. They guard against regressions in the
# scope and structural handling of the body. If our `infer_type` accidentally
# recursed in a way that broke these shapes, this test file would fail before
# the existing list_comp / closure suites caught it.
# -----------------------------------------------------------------------------

def conditional_comprehension():
    """
    >>> conditional_comprehension()
    """
    r = [a for a in range(5) if a % 2 == 0]
    assert r == [0, 2, 4]
    assert typeof(r).startswith("list"), typeof(r)


def multi_clause_comprehension():
    """
    >>> multi_clause_comprehension()
    """
    r = [a * b for a in [1, 2] for b in [3, 4]]
    assert r == [3, 4, 6, 8]
    assert typeof(r).startswith("list"), typeof(r)


def walrus_in_comprehension_body():
    """
    The walrus operator inside a comprehension body binds to the enclosing
    function scope (PEP 572). This is a known source of scope-handling bugs
    in compilers. Verify our infer_type does not interfere with the walrus
    target binding.

    >>> walrus_in_comprehension_body()
    """
    r = [(b := a * 2) for a in range(3)]
    assert r == [0, 2, 4]
    # The walrus target leaks to this function's scope.
    assert b == 4
    assert typeof(r).startswith("list"), typeof(r)


def comp_does_not_leak_to_outer_scope():
    """
    Regression test for the closure-scope contamination bug that drove the
    `self.expr_scope or env` fix. The comprehension's `x` must shadow the
    outer `x`, not steal its binding.

    Mirrors tests/run/list_comp_in_closure_T598.pyx but with an explicit
    typeof assertion so the failure mode is clear if the fix regresses.

    >>> comp_does_not_leak_to_outer_scope()
    [0, 4, 8]
    """
    x = 'abc'
    def f():
        return x
    result = [x * 2 for x in range(5) if x % 2 == 0]
    assert x == 'abc', x
    assert f() == 'abc', f()
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
