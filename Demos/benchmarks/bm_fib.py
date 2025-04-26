import cython
import time
import util


@cython.ccall
def fib(x: float) -> float:
    return 1 if x < 2 else fib(x-2) + fib(x-1)


def test_fib(iterations, N=30, scale: cython.long = 1, timer=time.perf_counter):
    s: cython.long
    scale_loops = range(scale)
    times = []
    for _ in range(iterations):
        t = timer()
        for s in range(scale):
            result = fib(N)
        t = timer() - t
        times.append(t)
    return times

main = test_fib


def run_benchmark(repeat=10, scale=1, timer=time.perf_counter):
    return test_fib(repeat, 28, scale=scale, timer=timer)


if __name__ == "__main__":
    import optparse
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description=("Test the performance of a recursive fibonacci implementation."))
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, test_fib)
