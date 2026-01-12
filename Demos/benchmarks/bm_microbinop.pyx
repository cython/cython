# cython: auto_pickle=False

import cython

import collections
import itertools
import time

from functools import partial


### Comparisons

number_types1 = cython.fused_type(int, float, object)
number_types2 = cython.fused_type(int, float, object)


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
def _bubblesort_steps(items: list, _type1: number_types1=0, _type2: number_types2=0):
    """A few iterations of bubblesort that scale linearly with the number of elements.
    """
    if number_types1 is int:
        a: int | None
    elif number_types1 is float:
        a: float | None
    else:
        a: object

    if number_types2 is int:
        b: int | None
    elif number_types2 is float:
        b: float | None
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

    t = timer()
    if type_selection == 1:
        _bubblesort_steps[object,object](items)
    elif type_selection == 2:
        _bubblesort_steps[object,int](items)
    elif type_selection == 3:
        _bubblesort_steps[object,float](items)
    elif type_selection == 4:
        _bubblesort_steps[int,object](items)
    elif type_selection == 5:
        _bubblesort_steps[float,object](items)
    elif type_selection == 6:
        _bubblesort_steps[int,int](items)
    elif type_selection == 7:
        _bubblesort_steps[float,float](items)
    else:
        assert False
    t = timer() - t

    return t


bm_cmp_obj_obj_mix = partial(_comparisons, 1, lambda v: v if v&1 else float(v))
bm_cmp_obj_obj_ext = partial(_comparisons, 1, lambda v: Wrapped(v) if v % 3 == 0 else float(v) if v % 3 == 1 else v)
bm_cmp_obj_obj_int = partial(_comparisons, 1, int)
bm_cmp_obj_obj_float = partial(_comparisons, 1, float)
bm_cmp_obj_int = partial(_comparisons, 2, int)
bm_cmp_obj_float = partial(_comparisons, 3, float)
bm_cmp_int_obj = partial(_comparisons, 4, int)
bm_cmp_float_obj = partial(_comparisons, 5, float)
bm_cmp_int_int = partial(_comparisons, 6, int)
bm_cmp_float_float = partial(_comparisons, 7, float)


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
