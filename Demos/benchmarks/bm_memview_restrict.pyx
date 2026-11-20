# cython: auto_pickle=False, boundscheck=False, wraparound=False, initializedcheck=False

# Benchmarks for 'restrict' memoryview arguments.
#
# Each kernel exists twice with an identical body: once with plain memoryview arguments
# and once with 'restrict' memoryview arguments.  Without 'restrict', the C compiler has
# to assume that the data buffers of the memoryviews may overlap.  It then either needs
# a runtime overlap check (GCC gives up when too many pointer pairs need checking) or
# cannot vectorise the loop at all.  The 'restrict' versions tell the compiler that the
# buffers are independent, which lets it keep values in registers and use SIMD.
#
# The data is single precision ('float') to get more SIMD lanes per vector register.

import cython

import collections
import time

from array import array


ctypedef float real

cdef Py_ssize_t N = 1024
cdef Py_ssize_t ROWS = 32


### SoA particle integration step: 6 written and 4 read-only arrays.
# Far too many pointer pairs for a runtime overlap check, so the plain version stays scalar.

cdef void particles_plain(real[::1] x, real[::1] y, real[::1] z,
                          real[::1] vx, real[::1] vy, real[::1] vz,
                          const real[::1] fx, const real[::1] fy, const real[::1] fz,
                          const real[::1] inv_mass, real dt) noexcept nogil:
    cdef Py_ssize_t i
    cdef real s
    for i in range(x.shape[0]):
        s = dt * inv_mass[i]
        vx[i] += fx[i] * s
        vy[i] += fy[i] * s
        vz[i] += fz[i] * s
        x[i] += vx[i] * dt
        y[i] += vy[i] * dt
        z[i] += vz[i] * dt


cdef void particles_restrict(real[::1] restrict x, real[::1] restrict y, real[::1] restrict z,
                             real[::1] restrict vx, real[::1] restrict vy, real[::1] restrict vz,
                             const real[::1] restrict fx, const real[::1] restrict fy, const real[::1] restrict fz,
                             const real[::1] restrict inv_mass, real dt) noexcept nogil:
    cdef Py_ssize_t i
    cdef real s
    for i in range(x.shape[0]):
        s = dt * inv_mass[i]
        vx[i] += fx[i] * s
        vy[i] += fy[i] * s
        vz[i] += fz[i] * s
        x[i] += vx[i] * dt
        y[i] += vy[i] * dt
        z[i] += vz[i] * dt


def _particles(use_restrict: cython.bint, scale, timer):
    i: cython.long
    arrays = [array('f', [1.0 + (k % 7) * 0.1 for k in range(N)]) for _ in range(10)]
    x: real[::1] = arrays[0]
    y: real[::1] = arrays[1]
    z: real[::1] = arrays[2]
    vx: real[::1] = arrays[3]
    vy: real[::1] = arrays[4]
    vz: real[::1] = arrays[5]
    fx: real[::1] = arrays[6]
    fy: real[::1] = arrays[7]
    fz: real[::1] = arrays[8]
    inv_mass: real[::1] = arrays[9]
    dt: real = 1e-4

    t = timer()
    if use_restrict:
        for i in range(scale):
            particles_restrict(x, y, z, vx, vy, vz, fx, fy, fz, inv_mass, dt)
    else:
        for i in range(scale):
            particles_plain(x, y, z, vx, vy, vz, fx, fy, fz, inv_mass, dt)
    t = timer() - t
    return t


def bm_particles_plain(scale, timer=time.perf_counter):
    return _particles(False, scale, timer)


def bm_particles_restrict(scale, timer=time.perf_counter):
    return _particles(True, scale, timer)


### RGB to YUV colour conversion on 2D image planes: 3 read and 3 written planes.
# The outputs are also read back in the loop, which the plain version has to reload from memory.

cdef void rgb_to_yuv_plain(const real[:, ::1] r, const real[:, ::1] g, const real[:, ::1] b,
                           real[:, ::1] y, real[:, ::1] u, real[:, ::1] v) noexcept nogil:
    cdef Py_ssize_t i, j
    for i in range(r.shape[0]):
        for j in range(r.shape[1]):
            y[i, j] = 0.299 * r[i, j] + 0.587 * g[i, j] + 0.114 * b[i, j]
            u[i, j] = 0.492 * (b[i, j] - y[i, j])
            v[i, j] = 0.877 * (r[i, j] - y[i, j])


cdef void rgb_to_yuv_restrict(const real[:, ::1] restrict r, const real[:, ::1] restrict g,
                              const real[:, ::1] restrict b, real[:, ::1] restrict y,
                              real[:, ::1] restrict u, real[:, ::1] restrict v) noexcept nogil:
    cdef Py_ssize_t i, j
    for i in range(r.shape[0]):
        for j in range(r.shape[1]):
            y[i, j] = 0.299 * r[i, j] + 0.587 * g[i, j] + 0.114 * b[i, j]
            u[i, j] = 0.492 * (b[i, j] - y[i, j])
            v[i, j] = 0.877 * (r[i, j] - y[i, j])


def _make_plane(value):
    return memoryview(array('f', [value]) * N).cast('B').cast('f', (ROWS, N // ROWS))


def _rgb_to_yuv(use_restrict: cython.bint, scale, timer):
    i: cython.long
    r: real[:, ::1] = _make_plane(0.2)
    g: real[:, ::1] = _make_plane(0.5)
    b: real[:, ::1] = _make_plane(0.8)
    y: real[:, ::1] = _make_plane(0.0)
    u: real[:, ::1] = _make_plane(0.0)
    v: real[:, ::1] = _make_plane(0.0)

    t = timer()
    if use_restrict:
        for i in range(scale):
            rgb_to_yuv_restrict(r, g, b, y, u, v)
    else:
        for i in range(scale):
            rgb_to_yuv_plain(r, g, b, y, u, v)
    t = timer() - t
    return t


def bm_rgb_to_yuv_plain(scale, timer=time.perf_counter):
    return _rgb_to_yuv(False, scale, timer)


def bm_rgb_to_yuv_restrict(scale, timer=time.perf_counter):
    return _rgb_to_yuv(True, scale, timer)


### Indirect indexing (gather): out[i] = s * x[idx[i]].
# No runtime overlap check is possible for the indirect read, so the plain version stays scalar.

cdef void gather_plain(const real[::1] x, const int[::1] idx, real[::1] out, real s) noexcept nogil:
    cdef Py_ssize_t i
    for i in range(out.shape[0]):
        out[i] = s * x[idx[i]]


cdef void gather_restrict(const real[::1] restrict x, const int[::1] restrict idx,
                          real[::1] restrict out, real s) noexcept nogil:
    cdef Py_ssize_t i
    for i in range(out.shape[0]):
        out[i] = s * x[idx[i]]


def _gather(use_restrict: cython.bint, scale, timer):
    i: cython.long
    x: real[::1] = array('f', [(k % 7) * 0.1 for k in range(N)])
    idx: cython.int[::1] = array('i', [(k * 7919) % N for k in range(N)])
    out: real[::1] = array('f', [0.0]) * N

    t = timer()
    if use_restrict:
        for i in range(scale):
            gather_restrict(x, idx, out, 2.0)
    else:
        for i in range(scale):
            gather_plain(x, idx, out, 2.0)
    t = timer() - t
    return t


def bm_gather_plain(scale, timer=time.perf_counter):
    return _gather(False, scale, timer)


def bm_gather_restrict(scale, timer=time.perf_counter):
    return _gather(True, scale, timer)


#### main ####

def time_benchmarks(scale):
    timings = {}
    for name, func in globals().items():
        if not name.startswith('bm_'):
            continue
        timings[name] = func(scale)
    return timings


def run_benchmark(repeat: bool, scale=1000):
    from util import repeat_to_accuracy, scale_subbenchmarks

    scales = scale_subbenchmarks(time_benchmarks(1000), scale)

    collected_timings = collections.defaultdict(list)

    for name, func in globals().items():
        if not name.startswith('bm_'):
            continue
        collected_timings[name] = repeat_to_accuracy(func, scale=scales[name], repeat=repeat, scale_to=scale)[0]

    for name, timings in collected_timings.items():
        print(f"{name}: {timings}")
