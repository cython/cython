.. highlight:: cython

.. _memoryviews:

*****************
Typed Memoryviews
*****************

Typed memoryviews allow efficient access to memory buffers, such as those
underlying NumPy arrays, without incurring any Python overhead.
Memoryviews are similar to the current NumPy array buffer support
(``np.ndarray[np.float64_t, ndim=2]``), but
they have more features and cleaner syntax.

Memoryviews are more general than the old NumPy array buffer support, because
they can handle a wider variety of sources of array data.  For example, they can
handle C arrays and the Cython array type (:ref:`view_cython_arrays`).

A memoryview can be used in any context (function parameters, module-level, cdef
class attribute, etc) and can be obtained from nearly any object that
exposes writable buffer through the `PEP 3118`_ buffer interface.

.. _view_quickstart:

Quickstart
==========

If you are used to working with NumPy, the following examples should get you
started with Cython memory views.

.. literalinclude:: ../../examples/userguide/memoryviews/quickstart.pyx

This code should give the following output::

    NumPy sum of the NumPy array before assignments: 351
    NumPy sum of NumPy array after assignments: 81
    Memoryview sum of NumPy array is 81
    Memoryview sum of C array is 451
    Memoryview sum of Cython array is 1351
    Memoryview sum of C memoryview is 451


Using memoryviews
=================

Syntax
------

Memory views use Python slicing syntax in a similar way as NumPy.

To create a complete view on a one-dimensional int buffer::

    cdef int[:] view1D = exporting_object

A complete 3D view::

    cdef int[:,:,:] view3D = exporting_object

A 2D view that restricts the first dimension of a buffer to 100 rows
starting at the second (index 1) and then skips every second (odd) row::

    cdef int[1:102:2,:] partial_view = exporting_object

This also works conveniently as function arguments:

.. code-block:: cython

    def process_3d_buffer(int[1:102:2,:] view not None):
        ...

The ``not None`` declaration for the argument automatically rejects
None values as input, which would otherwise be allowed.  The reason why
None is allowed by default is that it is conveniently used for return
arguments:

.. literalinclude:: ../../examples/userguide/memoryviews/not_none.pyx

Cython will reject incompatible buffers automatically, e.g. passing a
three dimensional buffer into a function that requires a two
dimensional buffer will raise a ``ValueError``.


Indexing
--------

In Cython, index access on memory views is automatically translated
into memory addresses.  The following code requests a two-dimensional
memory view of C ``int`` typed items and indexes into it::

   cdef int[:,:] buf = exporting_object

   print(buf[1,2])

Negative indices work as well, counting from the end of the respective
dimension::

   print(buf[-1,-2])

The following function loops over each dimension of a 2D array and
adds 1 to each item:

.. literalinclude:: ../../examples/userguide/memoryviews/add_one.pyx

Indexing and slicing can be done with or without the GIL.  It basically works
like NumPy.  If indices are specified for every dimension you will get an element
of the base type (e.g. `int`).  Otherwise, you will get a new view.  An Ellipsis
means you get consecutive slices for every unspecified dimension:

.. literalinclude:: ../../examples/userguide/memoryviews/slicing.pyx


Copying
-------

Memory views can be copied in place:

.. literalinclude:: ../../examples/userguide/memoryviews/copy.pyx

They can also be copied with the ``copy()`` and ``copy_fortran()`` methods; see
:ref:`view_copy_c_fortran`.

.. _view_transposing:

Transposing
-----------

In most cases (see below), the memoryview can be transposed in the same way that
NumPy slices can be transposed:

.. literalinclude:: ../../examples/userguide/memoryviews/transpose.pyx

This gives a new, transposed, view on the data.

Transposing requires that all dimensions of the memoryview have a
direct access memory layout (i.e., there are no indirections through pointers).
See :ref:`view_general_layouts` for details.

Newaxis
-------

As for NumPy, new axes can be introduced by indexing an array with ``None`` ::

    cdef double[:] myslice = np.linspace(0, 10, num=50)

    # 2D array with shape (1, 50)
    myslice[None] # or
    myslice[None, :]

    # 2D array with shape (50, 1)
    myslice[:, None]

    # 3D array with shape (1, 10, 1)
    myslice[None, 10:-20:2, None]

One may mix new axis indexing with all other forms of indexing and slicing.
See also an example_.

Read-only views
---------------

Since Cython 0.28, the memoryview item type can be declared as ``const`` to
support read-only buffers as input:

.. literalinclude:: ../../examples/userguide/memoryviews/np_flag_const.pyx

Using a non-const memoryview with a binary Python string produces a runtime error.
You can solve this issue with a ``const`` memoryview:

.. literalinclude:: ../../examples/userguide/memoryviews/view_string.pyx

Note that this does not *require* the input buffer to be read-only::

    a = np.linspace(0, 10, num=50)
    myslice = a   # read-only view of a writable buffer

Writable buffers are still accepted by ``const`` views, but read-only
buffers are not accepted for non-const, writable views::

    cdef double[:] myslice   # a normal read/write memory view

    a = np.linspace(0, 10, num=50)
    a.setflags(write=False)
    myslice = a   # ERROR: requesting writable memory view from read-only buffer!


Comparison to the old buffer support
====================================

You will probably prefer memoryviews to the older syntax because:

* The syntax is cleaner
* Memoryviews do not usually need the GIL (see :ref:`view_needs_gil`)
* Memoryviews are considerably faster

For example, this is the old syntax equivalent of the ``sum3d`` function above::

    cpdef int old_sum3d(object[int, ndim=3, mode='strided'] arr):
        cdef int I, J, K, total = 0
        I = arr.shape[0]
        J = arr.shape[1]
        K = arr.shape[2]
        for i in range(I):
            for j in range(J):
                for k in range(K):
                    total += arr[i, j, k]
        return total

Note that we can't use ``nogil`` for the buffer version of the function as we
could for the memoryview version of ``sum3d`` above, because buffer objects
are Python objects.  However, even if we don't use ``nogil`` with the
memoryview, it is significantly faster.  This is a output from an IPython
session after importing both versions::

    In [2]: import numpy as np

    In [3]: arr = np.zeros((40, 40, 40), dtype=int)

    In [4]: timeit -r15 old_sum3d(arr)
    1000 loops, best of 15: 298 us per loop

    In [5]: timeit -r15 sum3d(arr)
    1000 loops, best of 15: 219 us per loop

Python buffer support
=====================

Cython memoryviews support nearly all objects exporting the interface of Python
`new style buffers`_.  This is the buffer interface described in `PEP 3118`_.
NumPy arrays support this interface, as do :ref:`view_cython_arrays`.  The
"nearly all" is because the Python buffer interface allows the *elements* in the
data array to themselves be pointers; Cython memoryviews do not yet support
this.

.. _view_memory_layout:

Memory layout
=============

The buffer interface allows objects to identify the underlying memory in a
variety of ways.  With the exception of pointers for data elements, Cython
memoryviews support all Python new-type buffer layouts. It can be useful to know
or specify memory layout if the memory has to be in a particular format for an
external routine, or for code optimization.

Background
----------

The concepts are as follows: there is data access and data packing. Data access
means either direct (no pointer) or indirect (pointer).  Data packing means your
data may be contiguous or not contiguous in memory, and may use *strides* to
identify the jumps in memory consecutive indices need to take for each dimension.

NumPy arrays provide a good model of strided direct data access, so we'll use
them for a refresher on the concepts of C and Fortran contiguous arrays, and
data strides.

Brief recap on C, Fortran and strided memory layouts
----------------------------------------------------

The simplest data layout might be a C contiguous array.  This is the default
layout in NumPy and Cython arrays.  C contiguous means that the array data is
continuous in memory (see below) and that neighboring elements in the first
dimension of the array are furthest apart in memory, whereas neighboring
elements in the last dimension are closest together. For example, in NumPy::

    In [2]: arr = np.array([['0', '1', '2'], ['3', '4', '5']], dtype='S1')

Here, ``arr[0, 0]`` and ``arr[0, 1]`` are one byte apart in memory, whereas
``arr[0, 0]`` and ``arr[1, 0]`` are 3 bytes apart.  This leads us to the idea of
*strides*.  Each axis of the array has a stride length, which is the number of
bytes needed to go from one element on this axis to the next element.  In the
case above, the strides for axes 0 and 1 will obviously be::

    In [3]: arr.strides
    Out[4]: (3, 1)

For a 3D C contiguous array::

    In [5]: c_contig = np.arange(24, dtype=np.int8).reshape((2,3,4))
    In [6] c_contig.strides
    Out[6]: (12, 4, 1)

A Fortran contiguous array has the opposite memory ordering, with the elements
on the first axis closest together in memory::

    In [7]: f_contig = np.array(c_contig, order='F')
    In [8]: np.all(f_contig == c_contig)
    Out[8]: True
    In [9]: f_contig.strides
    Out[9]: (1, 2, 6)

A contiguous array is one for which a single continuous block of memory contains
all the data for the elements of the array, and therefore the memory block
length is the product of number of elements in the array and the size of the
elements in bytes. In the example above, the memory block is 2 * 3 * 4 * 1 bytes
long, where 1 is the length of an int8.

An array can be contiguous without being C or Fortran order::

    In [10]: c_contig.transpose((1, 0, 2)).strides
    Out[10]: (4, 12, 1)

Slicing an NumPy array can easily make it not contiguous::

    In [11]: sliced = c_contig[:,1,:]
    In [12]: sliced.strides
    Out[12]: (12, 1)
    In [13]: sliced.flags
    Out[13]:
    C_CONTIGUOUS : False
    F_CONTIGUOUS : False
    OWNDATA : False
    WRITEABLE : True
    ALIGNED : True
    UPDATEIFCOPY : False

Default behavior for memoryview layouts
---------------------------------------

As you'll see in :ref:`view_general_layouts`, you can specify memory layout for
any dimension of an memoryview.  For any dimension for which you don't specify a
layout, then the data access is assumed to be direct, and the data packing
assumed to be strided.  For example, that will be the assumption for memoryviews
like::

    int [:, :, :] my_memoryview = obj

.. _c_and_fortran_contiguous_memoryviews:

C and Fortran contiguous memoryviews
------------------------------------

You can specify C and Fortran contiguous layouts for the memoryview by using the
``::1`` step syntax at definition.  For example, if you know for sure your
memoryview will be on top of a 3D C contiguous layout, you could write::

    cdef int[:, :, ::1] c_contiguous = c_contig

where ``c_contig`` could be a C contiguous NumPy array.  The ``::1`` at the 3rd
position means that the elements in this 3rd dimension will be one element apart
in memory.  If you know you will have a 3D Fortran contiguous array::

    cdef int[::1, :, :] f_contiguous = f_contig

If you pass a non-contiguous buffer, for example

::

    # This array is C contiguous
    c_contig = np.arange(24).reshape((2,3,4))
    cdef int[:, :, ::1] c_contiguous = c_contig

    # But this isn't
    c_contiguous = np.array(c_contig, order='F')

you will get a ``ValueError`` at runtime::

    /Users/mb312/dev_trees/minimal-cython/mincy.pyx in init mincy (mincy.c:17267)()
        69
        70 # But this isn't
    ---> 71 c_contiguous = np.array(c_contig, order='F')
        72
        73 # Show the sum of all the arrays before altering it

    /Users/mb312/dev_trees/minimal-cython/stringsource in View.MemoryView.memoryview_cwrapper (mincy.c:9995)()

    /Users/mb312/dev_trees/minimal-cython/stringsource in View.MemoryView.memoryview.__cinit__ (mincy.c:6799)()

    ValueError: ndarray is not C-contiguous

Thus the `::1` in the slice type specification indicates in which dimension the
data is contiguous.  It can only be used to specify full C or Fortran
contiguity.

.. _view_copy_c_fortran:

C and Fortran contiguous copies
-------------------------------

.. Mark : I could not make this work - should it?

    # This slice is C contiguous
    c_contig = np.arange(24).reshape((2,3,4))
    f_contig = np.array(c_contig, order='F')
    cdef int [:, :, ::1] c_contig_view = c_contig
    cdef int [::1, :, :] f_contig_view = f_contig

    cdef int[:, :, ::1] f2c = f_contig_view.copy()
    cdef int[::1, :, :] c2f = c_contig_view.copy_fortran()

Copies can be made C or Fortran contiguous using the ``.copy()`` and
``.copy_fortran()`` methods::

    # This view is C contiguous
    cdef int[:, :, ::1] c_contiguous = myview.copy()

    # This view is Fortran contiguous
    cdef int[::1, :] f_contiguous_slice = myview.copy_fortran()

.. _view_general_layouts:

Specifying more general memory layouts
--------------------------------------

Data layout can be specified using the previously seen ``::1`` slice syntax, or
by using any of the constants in ``cython.view``. If no specifier is given in
any dimension, then the data access is assumed to be direct, and the data
packing assumed to be strided.  If you don't know whether a dimension will be
direct or indirect (because you're getting an object with a buffer interface
from some library perhaps), then you can specify the `generic` flag, in which
case it will be determined at runtime.

The flags are as follows:

* generic - strided and direct or indirect
* strided - strided and direct (this is the default)
* indirect - strided and indirect
* contiguous - contiguous and direct
* indirect_contiguous - the list of pointers is contiguous

and they can be used like this:

.. literalinclude:: ../../examples/userguide/memoryviews/memory_layout.pyx

Only the first, last or the dimension following an indirect dimension may be
specified contiguous:

.. literalinclude:: ../../examples/userguide/memoryviews/memory_layout_2.pyx

::

    # INVALID
    cdef int[::view.contiguous, ::view.indirect, :] d
    cdef int[::1, ::view.indirect, :] e


The difference between the `contiguous` flag and the `::1` specifier is that the
former specifies contiguity for only one dimension, whereas the latter specifies
contiguity for all following (Fortran) or preceding (C) dimensions::

    cdef int[:, ::1] c_contig = ...

    # VALID
    cdef int[:, ::view.contiguous] myslice = c_contig[::2]

    # INVALID
    cdef int[:, ::1] myslice = c_contig[::2]

The former case is valid because the last dimension remains contiguous, but the
first dimension does not "follow" the last one anymore (meaning, it was strided
already, but it is not C or Fortran contiguous any longer), since it was sliced.

.. _view_needs_gil:

Memoryviews and the GIL
=======================

As you will see from the :ref:`view_quickstart` section, memoryviews often do
not need the GIL::

    cpdef int sum3d(int[:, :, :] arr) nogil:
        ...

In particular, you do not need the GIL for memoryview indexing, slicing or
transposing. Memoryviews require the GIL for the copy methods
(:ref:`view_copy_c_fortran`), or when the dtype is object and an object
element is read or written.

Memoryview Objects and Cython Arrays
====================================

These typed memoryviews can be converted to Python memoryview objects
(`cython.view.memoryview`).  These Python objects are indexable, slicable and
transposable in the same way that the original memoryviews are. They can also be
converted back to Cython-space memoryviews at any time.

They have the following attributes:

    * ``shape``: size in each dimension, as a tuple.
    * ``strides``: stride along each dimension, in bytes.
    * ``suboffsets``
    * ``ndim``: number of dimensions.
    * ``size``: total number of items in the view (product of the shape).
    * ``itemsize``: size, in bytes, of the items in the view.
    * ``nbytes``: equal to ``size`` times ``itemsize``.
    * ``base``

And of course the aforementioned ``T`` attribute (:ref:`view_transposing`).
These attributes have the same semantics as in NumPy_.  For instance, to
retrieve the original object::

    import numpy
    cimport numpy as cnp

    cdef cnp.int32_t[:] a = numpy.arange(10, dtype=numpy.int32)
    a = a[::2]

    print(a)
    print(numpy.asarray(a))
    print(a.base)

    # this prints:
    #    <MemoryView of 'ndarray' object>
    #    [0 2 4 6 8]
    #    [0 1 2 3 4 5 6 7 8 9]

Note that this example returns the original object from which the view was
obtained, and that the view was resliced in the meantime.

.. _view_cython_arrays:

Cython arrays
=============

Whenever a Cython memoryview is copied (using any of the `copy` or
`copy_fortran` methods), you get a new memoryview slice of a newly created
``cython.view.array`` object. This array can also be used manually, and will
automatically allocate a block of data. It can later be assigned to a C or
Fortran contiguous slice (or a strided slice). It can be used like::

    from cython cimport view

    my_array = view.array(shape=(10, 2), itemsize=sizeof(int), format="i")
    cdef int[:, :] my_slice = my_array

It also takes an optional argument `mode` ('c' or 'fortran') and a boolean
`allocate_buffer`, that indicates whether a buffer should be allocated and freed
when it goes out of scope::

    cdef view.array my_array = view.array(..., mode="fortran", allocate_buffer=False)
    my_array.data = <char *> my_data_pointer

    # define a function that can deallocate the data (if needed)
    my_array.callback_free_data = free

You can also cast pointers to array, or C arrays to arrays::

    cdef view.array my_array = <int[:10, :2]> my_data_pointer
    cdef view.array my_array = <int[:, :]> my_c_array

Of course, you can also immediately assign a cython.view.array to a typed memoryview slice. A C array
may be assigned directly to a memoryview slice::

    cdef int[:, ::1] myslice = my_2d_c_array

The arrays are indexable and slicable from Python space just like memoryview objects, and have the same
attributes as memoryview objects.

CPython array module
====================

An alternative to ``cython.view.array`` is the ``array`` module in the
Python standard library.  In Python 3, the ``array.array`` type supports
the buffer interface natively, so memoryviews work on top of it without
additional setup.

Starting with Cython 0.17, however, it is possible to use these arrays
as buffer providers also in Python 2.  This is done through explicitly
cimporting the ``cpython.array`` module as follows::

    cimport cpython.array

    def sum_array(int[:] view):
        """
        >>> from array import array
        >>> sum_array( array('i', [1,2,3]) )
        6
        """
        cdef int total
        for i in range(view.shape[0]):
            total += view[i]
        return total

Note that the cimport also enables the old buffer syntax for the array
type.  Therefore, the following also works::

    from cpython cimport array

    def sum_array(array.array[int] arr):  # using old buffer syntax
        ...

Coercion to NumPy
=================

Memoryview (and array) objects can be coerced to a NumPy ndarray, without having
to copy the data. You can e.g. do::

    cimport numpy as np
    import numpy as np

    numpy_array = np.asarray(<np.int32_t[:10, :10]> my_pointer)

Of course, you are not restricted to using NumPy's type (such as ``np.int32_t``
here), you can use any usable type.

None Slices
===========

Although memoryview slices are not objects they can be set to None and they can
be checked for being None as well::

    def func(double[:] myarray = None):
        print(myarray is None)

If the function requires real memory views as input, it is therefore best to
reject None input straight away in the signature, which is supported in Cython
0.17 and later as follows::

    def func(double[:] myarray not None):
        ...

Unlike object attributes of extension classes, memoryview slices are not
initialized to None.


Pass data from a C function via pointer
=======================================

Since use of pointers in C is ubiquitous, here we give a quick example of how
to call C functions whose arguments contain pointers. Let's suppose you want to
manage an array (allocate and deallocate) with NumPy (it can also be Python arrays, or
anything that supports the buffer interface), but you want to perform computation on this
array with an external C function implemented in :file:`C_func_file.c`:

.. literalinclude:: ../../examples/userguide/memoryviews/C_func_file.c
    :linenos:

This file comes with a header file called :file:`C_func_file.h` containing:

.. literalinclude:: ../../examples/userguide/memoryviews/C_func_file.h
    :linenos:

where ``arr`` points to the array and ``n`` is its size.

You can call the function in a Cython file in the following way:

.. literalinclude:: ../../examples/userguide/memoryviews/memview_to_c.pyx
    :linenos:

Several things to note:
 - ``::1`` requests a C contiguous view, and fails if the buffer is not C contiguous.
   See :ref:`c_and_fortran_contiguous_memoryviews`.
 - ``&arr_memview[0]`` can be understood as 'the address of the first element of the
   memoryview'. For contiguous arrays, this is equivalent to the
   start address of the flat memory buffer.
 - ``arr_memview.shape[0]`` could have been replaced by ``arr_memview.size``,
   ``arr.shape[0]`` or ``arr.size``. But ``arr_memview.shape[0]`` is more efficient
   because it doesn't require any Python interaction.
 - ``multiply_by_10`` will perform computation in-place if the array passed is contiguous,
   and will return a new numpy array if ``arr`` is not contiguous.
 - If you are using Python arrays instead of numpy arrays, you don't need to check
   if the data is stored contiguously as this is always the case. See :ref:`array-array`.

This way, you can call the C function similar to a normal Python function,
and leave all the memory management and cleanup to NumPy arrays and Python's
object handling. For the details of how to compile and
call functions in C files, see :ref:`using_c_libraries`.


.. _GIL: http://docs.python.org/dev/glossary.html#term-global-interpreter-lock
.. _NumPy: https://docs.scipy.org/doc/numpy/reference/arrays.ndarray.html#memory-layout
.. _example: https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html
