.. highlight:: cython

.. _device_offload:

********************************
Offloading to a Device
********************************

Basic Usage
===========

Cython supports offloading code blocks to a GPU device.
Currently only parallel blocks (see :ref:'Using Parallelism <parallel>')
can be offloaded to a target device. The current implementation is based
on the OpenMP 'target' directive.

.. NOTE:: The offload functionality is experimental.

.. NOTE:: Offloading to a device is only possible for code blocks which
          do not require the Python interpreter. There is no way to use
          Python objects on the device.

Let's consider a simple example for computing pairwise distances between vectors in ``parallel``::

    def pairwise_distance_host(double[:, ::1] X):
        cdef int M = X.shape[0]
        cdef int N = X.shape[1]
        cdef double tmp, d
        cdef double[:, ::1] D = np.empty((M, M), dtype=np.float64)
        cdef int i,j,k
        with nogil, parallel():
            for i in prange(M):
                for j in prange(M):
                    d = 0.0
                    for k in range(N):
                        tmp = X[i, k] - X[j, k]
                        d = d + tmp * tmp  # cython would interpret '+=' as a reduction variable!
                        D[i, j] = sqrt(d)
        return np.asarray(D)

Now all we need is a marker that the parallel region should be offloaded to a device::

    ...
        with nogil, parallel(device={}):
            for i in prange(M):
    ...

Cython should take care of a safe way to define data mappings: transferring the necessary data to the device and from
device to the host:

* By default arrays are sent from host to device when entering the parallel region and from the device to host
* TODO: read-only data will only be copied from host to device, not from device back to host
* TODO: write-only data will not be copied from host to device but only from device back to host
* TODO: data which is not used outside the device-block will not be copied at all, only allocated and deallocated

.. NOTE:: A parallel-device-block can also be implicitly defined by using the ``device`` argument to prange directly
          (like ``for i in prange(M, device={}):``)

.. NOTE:: ``device`` implicitly requires ``parallel`` (and ``nogil``).
          TODO: make implicit directives (parallel(), nogil) more consistent and document accordingly

Mapping variables
=================
Because complex indexing can make it impossible to correctly determine the best
mapping and because data-movement is often the biggest performance bottleneck, we also need a way for experts to
optimize the data movement. For that, device should accept a dictionary mapping variable names to a map-type
(as borrowed from OpenMP target map clauses):

* ``"to"`` means host to device
* ``"from"`` means device to host
* ``"tofrom"`` means host to device and device to host
* ``"alloc"`` means not data-transfer at all, only create an instance of the object

In the above example, the input array/memview is read-only on the device, so we could indicate it like this::

    ...
        with nogil, parallel(device={D:'to'}):
            for i in prange(M):
    ...

Map-values provided in device overwrite whatever Cython would automatically infer.

The following data-types can be implicitly mapped to/from a device:

* scalars like double, int etc.
* bitwise copy-able structs TODO: check bitwise copyability
* C-contiguous memoryviews on the above
* ``self`` of ``cdef``'ed classes

Additionally, pointers to scalars and bitwise-copy'able structs can be explicitly mapped. Since the number of elements
the pointer points to cannot be determined by cython this information needs to be provided in addition to the map-type.
This is done by providing a tuple like this:

    device={ptr:('tofrom', N})

where ``N`` can be a variable or a constant integer (use ``1`` for an object-pointer, e.g. pointing to a single object).

Keeping data on the device
==========================
Another common challenge in offloading is that computation might go back and forth between host and GPU.
In such cases it is often required to keep data on the GPU between different GPU regions even if a host-section
is in between. As an example, let's look at the above code and block the computation by only computing a single
row of the output array at once. Note that this will be needed anyway if the input array becomes large since the
output vector size increases with quadratically and might simply not fit on the GPU.::

    def pairwise_distance_row(double[:, ::1] X):
        cdef int M = X.shape[0]
        cdef int N = X.shape[1]
        cdef double tmp, d
        cdef double[:, ::1] D = np.empty((M, M), dtype=np.float64)
        cdef double[::1] Dslice
        cdef int i,j,k
        with nogil:
            for i in range(M):
                Dslice = D[i,:]
                with parallel(device={Dslice:'from'}):
                    for j in prange(M):
                        d = 0.0
                        for k in range(N):
                            tmp = X[i, k] - X[j, k]
                            d = d + tmp * tmp  # cython would interpret '+=' as a reduction variable!
                            Dslice[j] = sqrt(d)
        return np.asarray(D)

Even though we only transfer slices of D in Dslice from device to host, the entire input array X will be send from
host to device in every iteration of the outermost loop. The suggested solution adds a data-context (to be used with
with) defining the lifetime of variables on the device. Let's simply use the same keyword device and let it accept
the same mappings::

    ...
        with nogil, device({X:'to'}):
            for i in range(M):
    ...

Since this is an expert tool we might not want or need to infer any map-type and leave it to the programmer.

Calling functions in a device block
===================================
The OpenMP compiler will try to inline a function that appears in a target/device section/block and will usually
complain if that's not possible. For such cases Cython provides the decorate ``@cython.device`` to explicitly make
functions available on the device::

    @cython.device
    cdef double _dist(double[:] v1, double[:] v2) nogil:
        cdef double d = 0.0
        cdef double tmp
        for k in range(min(v1.shape[0], v1.shape[0])):
            tmp = v1[k] - v2[k]
            d += tmp * tmp  # cython would interpret '+=' as a reduction variable!
        return sqrt(d)

    def pairwise_distance_target_row_context_annotated_func(double[:, ::1] X):
        cdef int M = X.shape[0]
        cdef double tmp, d
        cdef double[:, ::1] D = np.empty((M, M), dtype=np.float64)
        cdef double[::1] Dslice
        cdef int i,j,k
        with device({X:'to'}):
            with nogil:
                for i in range(M):
                    Dslice = D[i,:]
                    with parallel(device={Dslice:'from'}):
                        for j in prange(M):
                            Dslice[j] = _dist(X[i], X[j])
        return np.asarray(D)

Compiling/Building
==================
The compiler in the Intel® oneAPI HPC Toolkit supports OpenMP target/offload out-of-the box. Please see
https://software.intel.com/en-us/articles/openmp-50-target-with-intel-compilers on how to get and use it.

Unfortunately gcc/clang in most binary packages of gcc and llvm/clang have their offload/target capabilities
disabled. Instructions to build compilers with the necessary support can be found here
* clang:  https://hpc-wiki.info/hpc/Building_LLVM/Clang_with_OpenMP_Offloading_to_NVIDIA_GPUs
* gcc: https://kristerw.blogspot.com/2017/04/building-gcc-with-support-for-nvidia.html
Note that CUDA v10 is not support yet by llvm, use CUDA v9.2.
Note that gcc currently cannot generate dynamic/shared libraries using offload. Hence gcc is most likely currently
not a usable alternative.

Examples for compile time flags:
* ``CC=icc CFLAGS="-qnextgen -fiopenmp -fopenmp-targets=spir64" LDSHARED="icc -shared" python setup.py build``
* ``CC=gcc CFLAGS="-fopenmp -foffload=nvptx-none" LDSHARED="gcc -shared" python setup.py build``
* ``CC=clang CFLAGS="-fopenmp -fopenmp-targets=nvptx64" LDSHARED="clang -shared"  python setup.py build``

Limitations, open questions etc
===============================
* In most cases the generated code does not work if ``@boundscheck`` and ``@wraparound`` are not set to False.
* OpenMP does not allow mapping overlapping memory regions. We need to at least check that 2 memviews do not overlap
* C-pointers are not properly checked
* Only C-contiguous memviews are supported
* need support for setup.py/distutils
* need tests
* need docu (syntax, semantics, and how to setup offload compiler)
* error reporting back to host is disabled, properly mapping related variables could allow a useful error reporting
* string support has not been looked at yet

