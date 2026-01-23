# cython: auto_pickle=False

import cython

import collections
import itertools
import time

from functools import partial


### Comparisons

item_types1 = cython.fused_type(int, float, str, bytes, bytearray, object)
item_types2 = cython.fused_type(int, float, str, bytes, bytearray, object)


@cython.total_ordering
@cython.cclass
class Wrapped:
    _value: object
    def __init__(self, value):
        self._value = value

    def __lt__(self, other):
        if isinstance(other, Wrapped):
            other = cython.cast(Wrapped, other)._value
        return self._value < other

    def __gt__(self, other):
        if isinstance(other, Wrapped):
            other = cython.cast(Wrapped, other)._value
        return self._value > other


@cython.cfunc
def _bubblesort_steps(items: list, _type1: item_types1, _type2: item_types2):
    """A few iterations of bubblesort that scale linearly with the number of elements.
    """
    if item_types1 is int:
        a: int | None
    elif item_types1 is float:
        a: float | None
    elif item_types1 is str:
        a: str | None
    else:
        a: object

    if item_types2 is int:
        b: int | None
    elif item_types2 is float:
        b: float | None
    elif item_types2 is str:
        b: str | None
    else:
        b: object

    repeat: cython.int
    i: cython.Py_ssize_t
    j: cython.Py_ssize_t

    for repeat in range(10):
        # reverse order
        for i in range(1, len(items)):
            j = i-1
            a = items[j]
            b = items[i]
            if a < b:
                items[i], items[j] = items[j], items[i]
        # ascending order
        for i in range(1, len(items)):
            j = i-1
            a = items[j]
            b = items[i]
            if a > b:
                items[i], items[j] = items[j], items[i]


def _comparisons(type_selection: cython.int, item_type, scale: cython.Py_ssize_t, timer=time.perf_counter):
    items = list(map(item_type, itertools.chain(range(0, scale*10, 3), range(2, scale*10, 3))))
    typeval = item_type(0)

    t = timer()
    # numbers: int/float/Wrapped
    if type_selection == 1:
        _bubblesort_steps[object,object](items, typeval, typeval)
    elif type_selection == 2:
        _bubblesort_steps[object,int](items, typeval, typeval)
    elif type_selection == 3:
        _bubblesort_steps[object,float](items, typeval, typeval)
    elif type_selection == 4:
        _bubblesort_steps[int,object](items, typeval, typeval)
    elif type_selection == 5:
        _bubblesort_steps[float,object](items, typeval, typeval)
    elif type_selection == 6:
        _bubblesort_steps[int,int](items, typeval, typeval)
    elif type_selection == 7:
        _bubblesort_steps[float,float](items, typeval, typeval)
    # str
    elif type_selection == 8:
        _bubblesort_steps[object,str](items, typeval, typeval)
    elif type_selection == 9:
        _bubblesort_steps[str,object](items, typeval, typeval)
    elif type_selection == 10:
        _bubblesort_steps[str,str](items, typeval, typeval)
    # bytes
    elif type_selection == 11:
        _bubblesort_steps[object,bytes](items, typeval, typeval)
    elif type_selection == 12:
        _bubblesort_steps[bytes,object](items, typeval, typeval)
    elif type_selection == 13:
        _bubblesort_steps[bytes,bytes](items, typeval, typeval)
    # bytearray
    elif type_selection == 14:
        _bubblesort_steps[object,bytearray](items, typeval, typeval)
    elif type_selection == 15:
        _bubblesort_steps[bytearray,object](items, typeval, typeval)
    elif type_selection == 16:
        _bubblesort_steps[bytearray,bytearray](items, typeval, typeval)
    # reject everything else
    else:
        assert False
    t = timer() - t

    return t


# Number benchmarks
bm_cmp_obj_obj_mix = partial(_comparisons, 1, lambda v: v if v&1 else float(v))
bm_cmp_obj_obj_numext = partial(_comparisons, 1, lambda v: Wrapped(v) if v % 3 == 0 else float(v) if v % 3 == 1 else v)
bm_cmp_obj_obj_int = partial(_comparisons, 1, int)
bm_cmp_obj_obj_float = partial(_comparisons, 1, float)
bm_cmp_obj_int = partial(_comparisons, 2, int)
bm_cmp_obj_float = partial(_comparisons, 3, float)
bm_cmp_int_obj = partial(_comparisons, 4, int)
bm_cmp_float_obj = partial(_comparisons, 5, float)
bm_cmp_int_int = partial(_comparisons, 6, int)
bm_cmp_float_float = partial(_comparisons, 7, float)

# str benchmarks
def _make_long_str(num):
    return ' ' * (num % 349) + "%c" % (num % 97)

bm_cmp_obj_obj_str = partial(_comparisons, 1, str)
bm_cmp_obj_obj_strext = partial(_comparisons, 1, lambda v: Wrapped(str(v)) if v % 2 == 0 else str(v))
bm_cmp_obj_str = partial(_comparisons, 8, str)
bm_cmp_obj_str_long = partial(_comparisons, 8, _make_long_str)
bm_cmp_str_obj = partial(_comparisons, 9, str)
bm_cmp_str_str = partial(_comparisons, 10, str)
bm_cmp_str_str_long = partial(_comparisons, 10, _make_long_str)

# bytes/bytearray benchmarks
def _make_bytes(num):
    return b"%c" % (num % 256)
def _make_long_bytes(num):
    return b' ' * (num % 349) + b"%c" % (num % 97)

def _make_bytearray(num):
    return bytearray(_make_bytes(num))
def _make_long_bytearray(num):
    return bytearray(_make_long_bytes(num))

bm_cmp_obj_obj_bytes = partial(_comparisons, 1, _make_bytes)
bm_cmp_obj_obj_bytearray = partial(_comparisons, 1, _make_bytearray)
bm_cmp_obj_obj_bytemix = partial(_comparisons, 1, lambda v: _make_bytearray(v) if v % 3 == 0 else _make_bytes(v))
bm_cmp_obj_obj_bytesext = partial(_comparisons, 1, lambda v: Wrapped(_make_bytes(v)) if v % 2 == 0 else _make_bytes(v))

bm_cmp_obj_bytes = partial(_comparisons, 11, _make_bytes)
bm_cmp_obj_bytes_long = partial(_comparisons, 11, _make_long_bytes)
bm_cmp_bytes_obj = partial(_comparisons, 12, _make_bytes)
bm_cmp_bytes_bytes = partial(_comparisons, 13, _make_bytes)
bm_cmp_bytes_bytes_long = partial(_comparisons, 13, _make_long_bytes)

bm_cmp_obj_bytearray = partial(_comparisons, 14, _make_bytearray)
bm_cmp_obj_bytearray_long = partial(_comparisons, 14, _make_long_bytearray)
bm_cmp_bytearray_obj = partial(_comparisons, 15, _make_bytearray)
bm_cmp_bytearray_bytearray = partial(_comparisons, 16, _make_bytearray)
bm_cmp_bytearray_bytearray_long = partial(_comparisons, 16, _make_long_bytearray)


#### main ####

def time_benchmarks(scale):
    timings = {}
    for name, func in globals().items():
        if not name.startswith('bm_'):
            continue
        timings[name] = func(scale)
    return timings


def run_benchmark(repeat: bool, scale=1000):
    from util import repeat_to_accuracy, scale_subbenchmarks

    scales = scale_subbenchmarks(time_benchmarks(1000), scale)

    collected_timings = collections.defaultdict(list)

    for name, func in globals().items():
        if not name.startswith('bm_'):
            continue
        collected_timings[name] = repeat_to_accuracy(func, scale=scales[name], repeat=repeat, scale_to=scale)[0]

    for name, timings in collected_timings.items():
        print(f"{name}: {timings}")
