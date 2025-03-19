import cython
import time
import util


@cython.ccall
def fib(x: float) -> float:
    return 1 if x < 2 else fib(x-2) + fib(x-1)


def test_fib(iterations, N=30, _time=time.perf_counter):
    times = []
    for _ in range(iterations):
        t = _time()
        result = fib(N)
        t = _time() - t
        times.append(t)
    return times

main = test_fib


def run_benchmark(repeat=10, count=35, timer=time.perf_counter):
    return test_fib(repeat, count, timer)


if __name__ == "__main__":
    import optparse
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description=("Test the performance of a recursive fibonacci implementation."))
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, test_fib)
