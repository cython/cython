import cython
import time


def fib_untyped(x):
    return 1 if x < 2 else fib_untyped(x-2) + fib_untyped(x-1)

@cython.ccall
def fib_float(x: float) -> float:
    return 1 if x < 2 else fib_float(x-2) + fib_float(x-1)

def fib_float_pycall(x: float) -> float:
    return 1 if x < 2 else fib_float_pycall(x-2) + fib_float_pycall(x-1)

@cython.ccall
def fib_int(x: int) -> int:
    return 1 if x < 2 else fib_int(x-2) + fib_int(x-1)

def fib_int_pycall(x: int) -> int:
    return 1 if x < 2 else fib_int_pycall(x-2) + fib_int_pycall(x-1)

@cython.ccall
def fib_cull(x: cython.ulonglong) -> cython.ulonglong:
    return 1 if x < 2 else fib_cull(x-2) + fib_cull(x-1)

def fib_cull_pycall(x: cython.ulonglong) -> cython.ulonglong:
    return 1 if x < 2 else fib_cull_pycall(x-2) + fib_cull_pycall(x-1)


def run_fib(fib, N, scale: cython.int, timer=time.perf_counter):
    fake_result = 0

    t = timer()
    for _ in range(scale):
        fake_result += fib(N)
    t = timer() - t

    if fake_result < 1:
        # Unreachable, but hopefully difficult to detect. :)
        return 0.0
    return t


def run_benchmark(repeat=True, scale=1):
    from util import repeat_to_accuracy

    collected_timings = {
        f'bm_{bm_func.__name__}': repeat_to_accuracy(run_fib, bm_func, 28, scale=scale, repeat=repeat)[0]
        for bm_func in [fib_untyped, fib_float, fib_float_pycall, fib_int, fib_int_pycall, fib_cull, fib_cull_pycall]
    }

    for name, timings in collected_timings.items():
        print(f"{name}: {timings}")
