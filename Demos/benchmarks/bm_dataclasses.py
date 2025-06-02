import cython
from cython.cimports.libc.math import sin, cos, sqrt

from collections import defaultdict
from itertools import pairwise
import time


@cython.dataclasses.dataclass(init=False, order=True)
class Point(object):
    x: float
    y: float
    z: float

    def __init__(self, i):
        self.x = x = sin(i)
        self.y = cos(i) * 3
        self.z = (x * x) / 2

    def normalize(self):
        x = self.x
        y = self.y
        z = self.z
        norm = sqrt(x * x + y * y + z * z)
        self.x /= norm
        self.y /= norm
        self.z /= norm

    def maximize(self, other):
        self.x = self.x if self.x > other.x else other.x
        self.y = self.y if self.y > other.y else other.y
        self.z = self.z if self.z > other.z else other.z
        return self


def benchmark_create(n: cython.Py_ssize_t) -> list[Point]:
    points = [None] * n
    for i in range(n):
        points[i] = Point(i)
    return points


def benchmark_float(points: list[Point]):
    for p in points:
        p.normalize()

    next = points[0]
    for p in points[1:]:
        next = next.maximize(p)
    return next


def benchmark_repr(points: list[Point]):
    for p in points:
        repr(p)


def benchmark_compare(points: list[Point]):
    all_results: bint = False
    result: bint

    for p1, p2 in pairwise(points):
        result = False
        result |= p1 == p2
        result |= p1 != p2
        result |= p1 < p2
        result |= p1 > p2
        result |= p1 <= p2
        result |= p1 >= p2
        all_results |= result
    return all_results


def benchmark(n, timer=time.perf_counter):
    t0 = timer()
    points = benchmark_create(n)
    t1 = timer()
    benchmark_float(points)
    t2 = timer()
    benchmark_repr(points)
    t3 = timer()
    benchmark_compare(points)
    t4 = timer()
    return {
        'create': t1 - t0,
        'float': t2 - t1,
        'repr': t3 - t2,
        'compare': t4 - t3,
    }


POINTS = 10_000

def run_benchmark(repeat: int = 9, scale=POINTS, timer=time.perf_counter):
    timings = defaultdict(list)
    for _ in range(repeat):
        for name, timing in benchmark(scale, timer).items():
            timings[name].append(timing)

    for name, times in timings.items():
        print(f"dataclasses[{name}]: {times}")
