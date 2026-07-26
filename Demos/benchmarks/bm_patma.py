# a really simple micro-benchmark for pattern matching
# used to test that the Cython version is working well

import cython
from array import array


class A:
    b = 1
    def __repr__(self):
        return f'A({self.b})'


class C:
    __match_args__ = ("a", "b", "c")

    def __init__(self):
        self.a = 1
        self.b = None
        self.c = "string"


def speed_test(x):
    match x:
        case [0, 1, 2]:
            return x
        case [0, *x, 0]:
            return x
        case {"a": "xxx", A.b: x, **extra}:
            return x
        case 5 as y:
            return y
        case set(y):
            return y
        case A(b=1):
            return x
        case C(a, None):
            return a


class D(dict):
    def __repr__(self):
        return "D(%s)" % super(D, self).__repr__()

class E(dict):
    def __repr__(self):
        return "E(%s)" % super(E, self).__repr__()
    def get(self, key, default):
        return super().get(key, default)

d1 = {"a": "xxx", 1: 500}
d2 = D(d1)
d3 = E(d1)
l1 = [0, 1, 2]
l2 = []
l3 = [0] + list(range(10)) + [0]
l4 = (
    (0,) + tuple(range(1000000)) + (0,)
)  # the test here is to avoid making intermediates for the star pattern
l5 = array('i', l4)
v1 = 5
v2 = 6
c1 = set(l3)
c2 = A()
c3 = A()
c3.b = 2
c4 = C

tests = [d1, d2, d3, l1, l2, l3, l4, l5, v1, v2, c1, c2, c3, c4]

def get_benchmarks():
    def as_string(subject):
        try:
            len_ = len(subject)
        except TypeError:
            len_ = 1
        return repr(subject) if len_ <= 10 else f"long({len_}) {type(subject).__name__}"
    def make_runner(subject):
        def runner(number: cython.int, timer):
            t = timer()
            for _ in range(number):
                speed_test(subject)
            t = timer() - t
            return t
        return runner
    return {
        f'patma {as_string(subject)}': make_runner(subject) for subject in tests
    }


def run_benchmark(repeat=True, scale=100):
    from util import repeat_to_accuracy, scale_subbenchmarks
    import time

    benchmarks = get_benchmarks()

    timings = {
        name: func(1000, time.perf_counter)
        for name, func in benchmarks.items()
    }
    scales = scale_subbenchmarks(timings, scale)

    collected_timings = {}

    for name, func in benchmarks.items():
        collected_timings[name] = repeat_to_accuracy(
            func, scale=scales[name], repeat=repeat)[0]

    for name, timings in collected_timings.items():
        print(f"{name}: {timings}")
