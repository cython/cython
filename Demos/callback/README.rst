This example demonstrates how you can wrap a C API
that has a callback interface, so that you can
pass Python functions to it as callbacks.

The files ``cheesefinder.h`` and ``cheesefinder.c``
represent the C library to be wrapped.

The file ``cheese.pyx`` is the Cython module
which wraps it.

The file ``run_cheese.py`` demonstrates how to
call the wrapper.
