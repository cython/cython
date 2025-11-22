Embedding Cython Modules in C/C++
=================================

Cython provides a convenient way to embed Python modules into C or C++ applications.
This allows you to create standalone binaries that contain a Python interpreter and your compiled modules.

Using the ``--embed`` flag
--------------------------

The easiest way to embed a Cython module is using the ``--embed`` command-line flag.
This generates a C file that includes a ``main()`` entry point, which initializes the Python interpreter
and imports your module.

.. code-block:: bash

    # Generate the C source with a main() function
    cython --embed -o myprogram.c mymodule.pyx

    # Compile (example for Linux/GCC)
    gcc -Os -I /usr/include/python3.8 -o myprogram myprogram.c -lpython3.8 -lpthread -lm -lutil -ldl

Manual Embedding
----------------

If you are integrating into an existing C++ application, you may not want Cython to generate ``main()``.
Instead, you should initialize Python explicitly and import your module.

.. code-block:: c

    #include <Python.h>
    #include "mymodule.h"

    int main(int argc, char *argv[]) {
        // Initialize Python
        Py_Initialize();

        // Initialize your Cython module
        PyInit_mymodule();

        // Run your application logic...

        // Clean up
        Py_Finalize();
        return 0;
    }