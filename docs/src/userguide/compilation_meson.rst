********************
Compiling with Meson
********************

Meson is a build system mainly focused on building compiled languages
such as C and C++. The `meson-python` package
allows it to work as a build backend to build Python wheels.

Some relevant links to official and unofficial documentation that
may be worth reading are:

* `The meson-python docs <https://mesonbuild.com/meson-python/>`_ which
  describe how to use Meson as a build backend. 
* `The section on their built-in Cython support <https://mesonbuild.com/Cython.html>`_
  provides examples of how to build a Cython module.
* `A complete simple example <https://github.com/oscarbenjamin/meson_simple>`_.

You need two files (plus your Cython source).
First is :file:`pyproject.toml` which specifies the build
backend and dependencies, and contains the your project-level metadata::

    [build-system]
    build-backend = 'mesonpy'
    requires = ['meson-python', 'cython']

    [project]
    name = 'example'
    version = '1.0.0'

Secondly you need a :file:`meson.build`, which describes how your module will be
built::

    project('my project', 'cython', 'c')

    py = import('python').find_installation(pure: false)

    py.extension_module(
       'foo',
       'foo.pyx',
       install: true
    )

Additional Cython arguments can be passed to ``py.extension_module`` e.g.::

    cython_args : ['-Xboundscheck=False'],

(these are essentially command-line arguments to the ``cython`` executable).
Arguments to the C compiler are passed as::

    c_args: ['-DCYTHON_USE_TYPE_SPECS=1'],

To use C++ as an intermediate language instead of C, change the ``"c"`` in
the ``project`` line at the start of the file to ``"cpp"``.
