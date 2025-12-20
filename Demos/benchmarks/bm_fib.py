import cython
import time


@cython.ccall
def fib(x: float) -> float:
    return 1 if x < 2 else fib(x-2) + fib(x-1)


def run_fib(N, scale: cython.int, timer=time.perf_counter):
    fake_result = 0.

    t = timer()
    for _ in range(scale):
        fake_result += fib(N)
    t = timer() - t

    if fake_result < 1.:
        # Unreachable, but hopefully difficult to detect. :)
        return 0.0
    return t


def run_benchmark(repeat=True, scale=1):
    from util import repeat_to_accuracy
    return repeat_to_accuracy(run_fib, 28, scale=scale, repeat=repeat)[0]
