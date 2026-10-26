import collections
import time

import cython

DEFAULT_TIMER = time.perf_counter
GETITEM_DATA_SIZE = 25_000


@cython.cclass
class GetItemExt:
    _len: cython.int

    def __init__(self, data):
        self._len = len(data)
    def __len__(self):
        return self._len
    def __getitem__(self, index):
        return index


# Decorator @collection_type() is not supported by older Cython versions.
#[3.3+] #@cython.collection_type("sequence")
@cython.cclass
class GetItemExtSequence:
    _len: cython.int

    def __init__(self, data):
        self._len = len(data)
    def __len__(self):
        return self._len
    def __getitem__(self, index: cython.Py_ssize_t):
        return 5  # do not waste time on PyLong_FromSsize_t()

# Decorator value 'mapping' is not supported by older Cython versions.
#[3.3+] #@cython.collection_type("mapping")
@cython.cclass
class GetItemExtMapping:
    _len: cython.int

    def __init__(self, data):
        self._len = len(data)
    def __len__(self):
        return self._len
    def __getitem__(self, index):
        return index


def _getitems(seq):
    i: cython.Py_ssize_t
    len_seq: cython.Py_ssize_t = len(seq)

    ret = 1  # fake result use
    for i in range(len_seq):
        ret = seq[i] if ret is not None else 1
    return ret


def _getitems_from_py(seq):
    i: cython.Py_ssize_t
    len_seq: cython.Py_ssize_t = len(seq)

    getitem = eval("lambda i, _seq=seq: _seq[i]", {'seq': seq})

    ret = 1  # fake result use
    for i in range(len_seq):
        ret = getitem(i) if ret is not None else 1
    return ret


def _bm_getitems(iterations: cython.Py_ssize_t, seq_factory, timer=DEFAULT_TIMER, bm_func=_getitems):
    seq = seq_factory(range(GETITEM_DATA_SIZE))

    _: cython.Py_ssize_t

    t = timer()
    for _ in range(iterations):
        bm_func(seq)
    t = timer() - t
    return t


def bm_getitem_list(iterations, timer=DEFAULT_TIMER):
    return _bm_getitems(iterations, list, timer)

def bm_getitem_tuple(iterations, timer=DEFAULT_TIMER):
    return _bm_getitems(iterations, tuple, timer)

def bm_getitem_dict(iterations, timer=DEFAULT_TIMER):
    return _bm_getitems(iterations, lambda data: {i:i for i in data}, timer)

def bm_getitem_array(iterations, timer=DEFAULT_TIMER):
    from array import array
    from functools import partial
    return _bm_getitems(iterations, partial(array, 'I'), timer)

def bm_getitem_numpy(iterations, timer=DEFAULT_TIMER):
    import numpy
    return _bm_getitems(iterations, numpy.asarray, timer)

def bm_getitem_memoryview(iterations, timer=DEFAULT_TIMER):
    from array import array
    return _bm_getitems(iterations, lambda data: memoryview(array('I', data)), timer)

def bm_getitem_deque(iterations, timer=DEFAULT_TIMER):
    from collections import deque
    return _bm_getitems(iterations, deque, timer)

def bm_getitem_ext(iterations, timer=DEFAULT_TIMER):
    return _bm_getitems(iterations, GetItemExt, timer)

def bm_getitem_ext_seq(iterations, timer=DEFAULT_TIMER):
    return _bm_getitems(iterations, GetItemExtSequence, timer)

def bm_getitem_ext_map(iterations, timer=DEFAULT_TIMER):
    return _bm_getitems(iterations, GetItemExtMapping, timer)

def bm_getitem_ext_from_py(iterations, timer=DEFAULT_TIMER):
    return _bm_getitems(iterations, GetItemExt, timer, _getitems_from_py)

def bm_getitem_ext_from_py_seq(iterations, timer=DEFAULT_TIMER):
    return _bm_getitems(iterations, GetItemExtSequence, timer, _getitems_from_py)

def bm_getitem_ext_from_py_map(iterations, timer=DEFAULT_TIMER):
    return _bm_getitems(iterations, GetItemExtMapping, timer, _getitems_from_py)


# main

def run_benchmark(repeat=True, scale=1_000):
    from util import repeat_to_accuracy, scale_subbenchmarks

    benchmarks = [
        (name, func)
        for name, func in globals().items()
        if name.startswith('bm_')
    ]

    try:
        import numpy
    except ImportError:
        benchmarks = [
            (name, func)
            for name, func in benchmarks
            if 'numpy' not in name
        ]

    collected_timings = collections.defaultdict(list)

    timings = {}
    for name, func in benchmarks:
        if name.startswith('bm_'):
            timings[name] = func(200)

    scales = scale_subbenchmarks(timings, scale)

    for name, func in benchmarks:
        if name.startswith('bm_'):
            collected_timings[name] = repeat_to_accuracy(
                func, scale=scales[name], repeat=repeat, scale_to=scale)[0]

    for name, timings in collected_timings.items():
        print(f"{name}: {timings}")
