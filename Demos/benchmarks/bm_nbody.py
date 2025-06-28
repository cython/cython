#!/usr/bin/env python

"""N-body benchmark from the Computer Language Benchmarks Game.

This is intended to support Unladen Swallow's perf.py. Accordingly, it has been
modified from the Shootout version:
- Accept standard Unladen Swallow benchmark options.
- Run report_energy()/advance() in a loop.
- Reimplement itertools.combinations() to work with older Python versions.
"""

# Pulled from http://shootout.alioth.debian.org/u64q/benchmark.php?test=nbody&lang=python&id=4
# Contributed by Kevin Carson.
# Modified by Tupteq, Fredrik Johansson, and Daniel Nanz.

import cython

# Python imports
import optparse
import time


@cython.cfunc
def combinations(l: list):
    """Pure-Python implementation of itertools.combinations(l, 2)."""
    x: cython.Py_ssize_t

    result = []
    for x in range(len(l) - 1):
        ls = l[x+1:]
        for y in ls:
            result.append((l[x],y))
    return result


PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

BODIES = {
    'sun': ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], SOLAR_MASS),

    'jupiter': ([4.84143144246472090e+00,
                 -1.16032004402742839e+00,
                 -1.03622044471123109e-01],
                [1.66007664274403694e-03 * DAYS_PER_YEAR,
                 7.69901118419740425e-03 * DAYS_PER_YEAR,
                 -6.90460016972063023e-05 * DAYS_PER_YEAR],
                 9.54791938424326609e-04 * SOLAR_MASS),

    'saturn': ([8.34336671824457987e+00,
                4.12479856412430479e+00,
                -4.03523417114321381e-01],
               [-2.76742510726862411e-03 * DAYS_PER_YEAR,
                4.99852801234917238e-03 * DAYS_PER_YEAR,
                2.30417297573763929e-05 * DAYS_PER_YEAR],
                2.85885980666130812e-04 * SOLAR_MASS),

    'uranus': ([1.28943695621391310e+01,
                -1.51111514016986312e+01,
                -2.23307578892655734e-01],
               [2.96460137564761618e-03 * DAYS_PER_YEAR,
                2.37847173959480950e-03 * DAYS_PER_YEAR,
                -2.96589568540237556e-05 * DAYS_PER_YEAR],
                4.36624404335156298e-05 * SOLAR_MASS),

    'neptune': ([1.53796971148509165e+01,
                 -2.59193146099879641e+01,
                 1.79258772950371181e-01],
                [2.68067772490389322e-03 * DAYS_PER_YEAR,
                 1.62824170038242295e-03 * DAYS_PER_YEAR,
                 -9.51592254519715870e-05 * DAYS_PER_YEAR],
                 5.15138902046611451e-05 * SOLAR_MASS) }


SYSTEM = list(BODIES.values())
PAIRS = combinations(SYSTEM)

@cython.cfunc
def advance(dt: float, n: cython.long, bodies: list = SYSTEM, pairs: list = PAIRS):
    x1: float
    x2: float
    y1: float
    y2: float
    z1: float
    z2: float
    m1: float
    m2: float
    vx: float
    vy: float
    vz: float
    i: cython.long
    v1: list
    v2: list
    r: list

    for i in range(n):
        for (([x1, y1, z1], v1, m1),
             ([x2, y2, z2], v2, m2)) in pairs:
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            mag = dt * ((dx * dx + dy * dy + dz * dz) ** (-1.5))
            b1m = m1 * mag
            b2m = m2 * mag
            v1[0] -= dx * b2m
            v1[1] -= dy * b2m
            v1[2] -= dz * b2m
            v2[0] += dx * b1m
            v2[1] += dy * b1m
            v2[2] += dz * b1m
        for (r, [vx, vy, vz], m) in bodies:
            r[0] += dt * vx
            r[1] += dt * vy
            r[2] += dt * vz


@cython.cfunc
def report_energy(bodies: list = SYSTEM, pairs: list = PAIRS, e: float = 0.0):
    x1: float
    x2: float
    y1: float
    y2: float
    z1: float
    z2: float
    m: float
    m1: float
    m2: float
    vx: float
    vy: float
    vz: float

    for (((x1, y1, z1), v1, m1),
         ((x2, y2, z2), v2, m2)) in pairs:
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        e -= (m1 * m2) / ((dx * dx + dy * dy + dz * dz) ** 0.5)
    for (r, [vx, vy, vz], m) in bodies:
        e += m * (vx * vx + vy * vy + vz * vz) / 2.
    return e


@cython.cfunc
def offset_momentum(ref: tuple, bodies: list = SYSTEM, px: float = 0.0, py: float = 0.0, pz: float = 0.0):
    m: float
    vx: float
    vy: float
    vz: float
    v: list

    for (r, [vx, vy, vz], m) in bodies:
        px -= vx * m
        py -= vy * m
        pz -= vz * m
    (r, v, m) = ref
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m


def test_nbody(iterations: cython.int, count: cython.long=20_000, scale: cython.long = 1, timer=time.perf_counter):
    s: cython.long

    # Warm-up runs.
    report_energy()
    advance(0.01, count)
    report_energy()

    times = []
    for _ in range(iterations):
        t0 = timer()
        for s in range(scale):
            report_energy()
            advance(0.01, count)
            report_energy()
        t1 = timer()
        times.append(t1 - t0)
    return times

main = test_nbody


def run_benchmark(repeat=10, scale=1, timer=time.perf_counter):
    return test_nbody(repeat, scale=scale, timer=timer)


if __name__ == '__main__':
    import util
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description=("Run the n-body benchmark."))
    util.add_standard_options_to(parser)
    options, args = parser.parse_args()

    offset_momentum(BODIES['sun'])  # Set up global state
    util.run_benchmark(options, options.num_runs, test_nbody)
