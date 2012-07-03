#################### GetTileSize ####################

DEF _DEBUG = False

DEF MIN_BLOCKSIZE = 256
DEF SIZE = 1600
DEF MAX_TRIES = 4
DEF N_SAMPLES = 10

import sys, types, time

cdef extern from "stdlib.h":
    void *malloc(size_t) nogil
    void free(void *) nogil

# cache tile size in this global, and in the module
cdef bint have_tile_size = False
cdef Py_ssize_t tile_size

cdef Py_ssize_t get_tile_size() except 0:
    if not have_tile_size:
        create_tile_size()
    return tile_size

cdef int create_tile_size() except -1:
    modname = '__pyx_array_expressions'
    mod = sys.modules.get(modname)
    if not mod:
        mod = types.ModuleType(modname)
        import time; t = time.time()
        mod.tile_size = compute_tile_size()
        if _DEBUG:
            print "total time:", time.time() - t, "tile size:", mod.tile_size
        sys.modules[modname] = mod

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

cdef inline tile(float *a, float *b, Py_ssize_t blocksize):
    cdef Py_ssize_t i, j, tiled_i, tiled_j, upper_i, upper_j

    for tiled_i in range(0, SIZE, blocksize):
        for tiled_j in range(0, SIZE, blocksize):
            upper_i = min(tiled_i + blocksize, SIZE)
            upper_j = min(tiled_j + blocksize, SIZE)
            for i in range(tiled_i, upper_i):
                for j in range(tiled_j, upper_j):
                    a[i * SIZE + j] += b[i + j * SIZE]

# print __pyx_get_tile_size()
