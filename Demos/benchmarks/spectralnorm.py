# -*- coding: utf-8 -*-
# The Computer Language Benchmarks Game
# http://shootout.alioth.debian.org/
# Contributed by Sebastien Loisel
# Fixed by Isaac Gouy
# Sped up by Josh Goldfoot
# Dirtily sped up by Simon Descarpentries
# Concurrency by Jason Stitt

import cython

import time


@cython.cfunc
def eval_A(i: cython.long, j: cython.long) -> float:
    return 1.0 / ((i + j) * (i + j + 1) / 2 + i + 1)

@cython.cfunc
def eval_A_times_u(u: list) -> list:
    return [ part_A_times_u(i,u) for i in range(len(u)) ]

@cython.cfunc
def eval_At_times_u(u: list) -> list:
    return [ part_At_times_u(i,u) for i in range(len(u)) ]

@cython.cfunc
def eval_AtA_times_u(u: list) -> list:
    return eval_At_times_u(eval_A_times_u(u))

@cython.cfunc
def part_A_times_u(i: cython.long, u: list) -> float:
    partial_sum: float = 0.0
    u_j: float
    j: cython.Py_ssize_t

    for j, u_j in enumerate(u):
        partial_sum += eval_A(i, j) * u_j
    return partial_sum

@cython.cfunc
def part_At_times_u(i: cython.long, u: list) -> float:
    partial_sum: float = 0.0
    u_j: float
    j: cython.Py_ssize_t

    for j, u_j in enumerate(u):
        partial_sum += eval_A(j, i) * u_j
    return partial_sum


DEFAULT_N = 130

def main(repeat: cython.int = 10, N: cython.int = DEFAULT_N, timer=time.perf_counter):
    times = []
    for i in range(repeat):
        t0 = timer()
        u = [1] * N

        for dummy in range(10):
            v = eval_AtA_times_u(u)
            u = eval_AtA_times_u(v)

        vBv = vv = 0

        for ue, ve in zip(u, v):
            vBv += ue * ve
            vv  += ve * ve
        tk = timer()
        times.append(tk - t0)
    return times


def run_benchmark(repeat=10, count=DEFAULT_N, timer=time.perf_counter):
    return main(repeat, count, timer)


if __name__ == "__main__":
    import util
    import optparse

    parser = optparse.OptionParser(
        usage="%prog [options]",
        description="Test the performance of the spectralnorm benchmark")
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    util.run_benchmark(options, options.num_runs, main)
