# coding=utf-8
# NOTE: requires Python 3.6 or later if not compiled with Cython

from math import fsum
import time

import cython


def run(timer=time.perf_counter):
    t0 = timer()

    f: object = 1.0
    n: cython.int = 5
    i: object = 12345678
    s = 'abc'
    u = u'üöä'

    # repeat without fast looping ...
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:3.2}--{n:2}{n:5}oo{i}{s}"
    f"{n}oo{n*10}{f:5.2}--{n:2}{n:5}oo{i}{u}"
    f"{n}oo{n*10}{f:2.2}--{n:2}{n:5}oo{i}{s}xx{u}"

    # repeat without fast looping ...
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:3.2}--{n:2}{n:5}oo{i}{s}"
    f"{n}oo{n*10}{f:5.2}--{n:2}{n:5}oo{i}{u}"
    f"{n}oo{n*10}{f:2.2}--{n:2}{n:5}oo{i}{s}xx{u}"

    # repeat without fast looping ...
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:3.2}--{n:2}{n:5}oo{i}{s}"
    f"{n}oo{n*10}{f:5.2}--{n:2}{n:5}oo{i}{u}"
    f"{n}oo{n*10}{f:2.2}--{n:2}{n:5}oo{i}{s}xx{u}"

    # repeat without fast looping ...
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:3.2}--{n:2}{n:5}oo{i}{s}"
    f"{n}oo{n*10}{f:5.2}--{n:2}{n:5}oo{i}{u}"
    f"{n}oo{n*10}{f:2.2}--{n:2}{n:5}oo{i}{s}xx{u}"

    # repeat without fast looping ...
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:3.2}--{n:2}{n:5}oo{i}{s}"
    f"{n}oo{n*10}{f:5.2}--{n:2}{n:5}oo{i}{u}"
    f"{n}oo{n*10}{f:2.2}--{n:2}{n:5}oo{i}{s}xx{u}"

    # repeat without fast looping ...
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:3.2}--{n:2}{n:5}oo{i}{s}"
    f"{n}oo{n*10}{f:5.2}--{n:2}{n:5}oo{i}{u}"
    f"{n}oo{n*10}{f:2.2}--{n:2}{n:5}oo{i}{s}xx{u}"

    # repeat without fast looping ...
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:3.2}--{n:2}{n:5}oo{i}{s}"
    f"{n}oo{n*10}{f:5.2}--{n:2}{n:5}oo{i}{u}"
    f"{n}oo{n*10}{f:2.2}--{n:2}{n:5}oo{i}{s}xx{u}"

    # repeat without fast looping ...
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:3.2}--{n:2}{n:5}oo{i}{s}"
    f"{n}oo{n*10}{f:5.2}--{n:2}{n:5}oo{i}{u}"
    f"{n}oo{n*10}{f:2.2}--{n:2}{n:5}oo{i}{s}xx{u}"

    # repeat without fast looping ...
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:3.2}--{n:2}{n:5}oo{i}{s}"
    f"{n}oo{n*10}{f:5.2}--{n:2}{n:5}oo{i}{u}"
    f"{n}oo{n*10}{f:2.2}--{n:2}{n:5}oo{i}{s}xx{u}"

    # repeat without fast looping ...
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:3.2}--{n:2}{n:5}oo{i}{s}"
    f"{n}oo{n*10}{f:5.2}--{n:2}{n:5}oo{i}{u}"
    f"{n}oo{n*10}{f:2.2}--{n:2}{n:5}oo{i}{s}xx{u}"

    # repeat without fast looping ...
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:3.2}--{n:2}{n:5}oo{i}{s}"
    f"{n}oo{n*10}{f:5.2}--{n:2}{n:5}oo{i}{u}"
    f"{n}oo{n*10}{f:2.2}--{n:2}{n:5}oo{i}{s}xx{u}"

    # repeat without fast looping ...
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"
    f"{n}oo{n*10}{f:.2}--{n:2}{n:5}oo{i}"

    f"{n}oo{n*10}{f:3.2}--{n:2}{n:5}oo{i}{s}"
    f"{n}oo{n*10}{f:5.2}--{n:2}{n:5}oo{i}{u}"
    f"{n}oo{n*10}{f:2.2}--{n:2}{n:5}oo{i}{s}xx{u}"

    tk = timer()
    return tk - t0


def main(n: cython.int, scale: cython.int = 10, timer=time.perf_counter):
    s: cython.long

    run()  # warmup

    times = []
    for i in range(n):
        times.append(fsum(run(timer) for s in range(scale)))
    return times


def run_benchmark(repeat=10, scale=1, timer=time.perf_counter):
    return main(repeat, scale, timer)


if __name__ == "__main__":
    import optparse
    import util
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description="Test the performance of fstring literal formatting")
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, main)
