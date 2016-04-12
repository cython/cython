# coding=utf-8
# NOTE: requires Python 3.6 or later if not compiled with Cython

from time import time

import cython


@cython.locals(x=int, n=int)
def run():
    t0 = time()

    f = 1.0
    x = 2
    n = 5
    i = 12345678
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

    tk = time()
    return tk - t0


def main(n):
    run()  # warmup
    times = []
    for i in range(n):
        times.append(run())
    return times


if __name__ == "__main__":
    import optparse
    import util
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description="Test the performance of fstring literal formatting")
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, main)
