#################### GetTileSize ####################

DEF _DEBUG = False

DEF MIN_BLOCKSIZE = 128
DEF SIZE = 1600
DEF MAX_TRIES = 4
DEF N_SAMPLES = 10

import sys, types, time, math

cdef extern from "stdlib.h":
    void *malloc(size_t) nogil
    void free(void *) nogil

# cache tile size in this global, and in the module
cdef bint have_tile_size = False
cdef Py_ssize_t tile_size

cdef get_module():
    modname = '__pyx_array_expressions'
    mod = sys.modules.get(modname)
    if not mod:
        mod = types.ModuleType(modname)
        sys.modules[modname] = mod
    return mod

cdef Py_ssize_t get_tile_size(Py_ssize_t itemsize, int n_operands) except 0:
    if not have_tile_size:
        create_tile_size()

    result = tile_size / (itemsize * (float(n_operands) / 2))
    digits = int(round(math.log(result, 2)))
    return max(2 ** digits, MIN_BLOCKSIZE / itemsize)

cdef int create_tile_size() except -1:
    mod = get_module()
    if not hasattr(mod, 'tile_size'):
        mod.tile_size = compute_tile_size()

    # assigning to globals is broken in utility codes
    (&have_tile_size)[0] = True
    (&tile_size)[0] = mod.tile_size
    return 0

cdef Py_ssize_t compute_tile_size() except 0:
    cdef float *a = <float *> malloc(SIZE * SIZE * sizeof(float))
    cdef float *b = <float *> malloc(SIZE * SIZE * sizeof(float))

    if a == NULL or b == NULL:
        free(a)
        free(b)
        raise MemoryError

    cdef Py_ssize_t blocksize = MIN_BLOCKSIZE
    cdef Py_ssize_t best_blocksize = blocksize
    best_time = float('inf')

    cdef int i
    cdef int seen_worse_blocksizes = 0

    try:
        for i in range(MAX_TRIES):
            t = try_blocksize(a, b, blocksize)
            if t > best_time:
                seen_worse_blocksizes += 1
                if seen_worse_blocksizes > 1:
                    break
            else:
                best_blocksize = blocksize
                seen_worse_blocksizes = 0
                best_time = t

            blocksize *= 2
    finally:
        free(a)
        free(b)

    return best_blocksize

cdef try_blocksize(float *a, float *b, Py_ssize_t blocksize):
    cdef int i

    # warm up
    tile(a, b, blocksize / sizeof(float))

    # time the run
    t = time.time()
    for i in range(N_SAMPLES):
        tile(a, b, blocksize / sizeof(float))

    return time.time() - t

cdef void tile(float *a, float *b, Py_ssize_t blocksize):
    cdef Py_ssize_t i, j, tiled_i, tiled_j, upper_i, upper_j

    for tiled_i in range(0, SIZE, blocksize):
        for tiled_j in range(0, SIZE, blocksize):
            upper_i = min(tiled_i + blocksize, SIZE)
            upper_j = min(tiled_j + blocksize, SIZE)
            for i in range(tiled_i, upper_i):
                for j in range(tiled_j, upper_j):
                    a[i * SIZE + j] += b[i + j * SIZE]

# print __pyx_get_tile_size()

# cached minimum OpenMP size for the 'if' clause

DEF MIN_OMP_SIZE = 512
DEF N_OMP_SAMPLES = 10
DEF MAX_OMP_TRIES = 10

cdef extern from *:
    bint __pyx_compiled_with_openmp()
    void __pyx_test_sequential(double *a, int upper_limit)
    void __pyx_test_parallel(double *a, int upper_limit)


cdef bint have_omp_size = False
cdef Py_ssize_t omp_size

cdef Py_ssize_t get_omp_size(int n_operands) except -1:
    if not have_omp_size:
        if _DEBUG:
            t = time.time()
            create_omp_size()
            t = time.time() - t
            print "OMP_SIZE", omp_size, "took", t, "seconds"
        else:
            create_omp_size()

    return omp_size / n_operands

cdef int create_omp_size() except -1:
    mod = get_module()
    if not hasattr(mod, 'omp_size'):
        mod.omp_size = compute_omp_size()

    # assigning to globals is broken in utility codes
    (&have_omp_size)[0] = True
    (&omp_size)[0] = mod.omp_size
    return 0

cdef Py_ssize_t compute_omp_size() except 0:
    if not __pyx_compiled_with_openmp():
        if _DEBUG:
            print "Skipping omp tuning, not compiled with OpenMP"
        return 1

    cdef double *a = <double *> malloc(sizeof(double) * MIN_OMP_SIZE * 2 ** MAX_OMP_TRIES)
    cdef int i, j

    best_time = float('inf')
    cdef Py_ssize_t best_size = MIN_OMP_SIZE

    try:
        for i in range(MAX_OMP_TRIES):
            # warm up
            __pyx_test_sequential(a, best_size)
            sequential_time = time.time()
            for j in range(N_OMP_SAMPLES):
                __pyx_test_sequential(a, best_size)
            sequential_time = time.time() - sequential_time

            # multi-core warm up & potential OpenMP initialization
            __pyx_test_parallel(a, best_size)
            parallel_time = time.time()
            for j in range(N_OMP_SAMPLES):
                __pyx_test_parallel(a, best_size)
            parallel_time = time.time() - parallel_time

            if _DEBUG:
                print "size:", best_size, "time:", sequential_time, parallel_time

            if parallel_time < sequential_time:
                return best_size

            best_size *= 2
    finally:
        free(a)

    return best_size

