from __future__ import absolute_import, print_function

from overflow_perf import *

import sys
import timeit
try:
    import numpy as np
except ImportError:
    np = None


def run_tests(N):
    global f
    for func in most_orthogonal, fib, collatz, factorial:
        print(func.__name__)
        for type in ['int', 'unsigned int', 'long long', 'unsigned long long', 'object']:
            if func == most_orthogonal:
                if type == 'object' or np is None:
                    continue
                type_map = {'int': 'int32', 'unsigned int': 'uint32', 'long long': 'int64', 'unsigned long long': 'uint64'}
                shape = N, 3
                arg = np.ndarray(shape, dtype=type_map[type])
                arg[:] = 1000 * np.random.random(shape)
            else:
                arg = N
            try:
                print("%s[%s](%s)" % (func.__name__, type, N))
                with_overflow = my_timeit(globals()[func.__name__ + "_overflow"][type], arg)
                no_overflow = my_timeit(func[type], arg)
                print("\t%0.04e\t%0.04e\t%0.04f" % (no_overflow, with_overflow, with_overflow / no_overflow))
                if func.__name__ + "_overflow_fold" in globals():
                    with_overflow = my_timeit(globals()[func.__name__ + "_overflow_fold"][type], arg)
                    print("\t%0.04e\t%0.04e\t%0.04f (folded)" % (
                        no_overflow, with_overflow, with_overflow / no_overflow))
            except OverflowError:
                print("    ", "Overflow")

def my_timeit(func, N):
    global f, arg
    f = func
    arg = N
    for exponent in range(10, 30):
        times = 2 ** exponent
        res = min(timeit.repeat("f(arg)", setup="from __main__ import f, arg", repeat=5, number=times))
        if res > .25:
            break
    return res / times


params = sys.argv[1:]
if not params:
    params = [129, 9, 97]
for arg in params:
    print()
    print("N", arg)
    run_tests(int(arg))
