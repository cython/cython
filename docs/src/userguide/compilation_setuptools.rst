*************************
Compiling with Setuptools
*************************

Historically, :mod:`setuptools` and its predecessor :mod:`distutils`,
were the main ways of building a package that uses Cython modules.
Because of this, Cython ships with some convenience libraries to
help use it with :mod:`setuptools`.

Declarative syntax
==================

Since late 2024 setuptools has supported a declarative syntax for building
extension modules.  In this one does not ship a :file:`setup.py` file
but instead describe your extension modules in :file:`pyproject.toml`.
This is simpler than the more commonly used :file:`setup.py` version but
somewhat more limited in how you can customize it.

Most of the Cython documentation pre-dates this system (and thus is
described in terms of :file:`setup.py`) but we include an example
here for illustrative purposes::

    # pyproject.toml
    [build-system]
    requires = ["setuptools", "cython"]
    build-backend = "setuptools.build_meta"

    [project]
    name = "cython-example"  # as it would appear on PyPI
    version = "0.1"

    [tool.setuptools]
    ext-modules = [
        {name = "cython_example.example", sources = ["example.pyx"]}
    ]

.. _basic_setup.py:

Basic :file:`setup.py`
======================

The setuptools extension provided with Cython allows you to pass ``.pyx`` files
directly to the :class:`~setuptools.Extension` constructor in your setup file.

If you have a single Cython file that you want to turn into a compiled
extension, say with filename :file:`example.pyx` the associated :file:`setup.py`
would be:

.. code-block:: python
    :caption: setup.py

    from setuptools import setup
    from Cython.Build import cythonize

    setup(
        ext_modules = cythonize("example.pyx")
    )

If your build depends directly on Cython in this way,
then you may also want to inform pip that :mod:`Cython` is required for
:file:`setup.py` to execute, following :pep:`518`,
creating a :file:`pyproject.toml` file containing, at least:

.. code-block:: toml
    :caption: pyproject.toml

    [build-system]
    requires = ["setuptools", "Cython"]

To understand the :file:`setup.py` more fully look at the official
:external+setuptools:doc:`setuptools documentation <index>`.
To compile the extension for use in the current directory use:

.. code-block:: console

    $ python setup.py build_ext --inplace

.. note::

    setuptools 74.1.0 adds experimental support for extensions in :file:`pyproject.toml` (instead of :file:`setup.py`):

    .. code-block:: toml
        :caption: pyproject.toml

        [build-system]
        requires = ["setuptools", "cython"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "mylib-foo"
        version = "0.42"

        [tool.setuptools]
        ext-modules = [
          {name = "example", sources = ["example.pyx"]}
        ]

    In this case, you can use any build frontend - e.g. `build <https://pypi.org/project/build/>`_

    .. code-block:: console

        $ python -m build

Configuring the C-Build
------------------------

.. note::

   More details on building Cython modules that use cimport numpy can be found in the :ref:`Numpy section <numpy_compilation>` of the user guide.

If you have :ref:`Cython include files <include_statement>` or :ref:`Cython definition files <definition_file>` in non-standard places you can pass an
``include_path`` parameter to ``cythonize``::

    from setuptools import setup
    from Cython.Build import cythonize

    setup(
        name="My hello app",
        ext_modules=cythonize("src/*.pyx", include_path=[...]),
    )

If you need to specify compiler options, libraries to link with or other
linker options you will need to create :class:`~setuptools.Extension` instances manually
(note that glob syntax can still be used to specify multiple extensions
in one line)::

    from setuptools import Extension, setup
    from Cython.Build import cythonize

    extensions = [
        Extension("primes", ["primes.pyx"],
            include_dirs=[...],
            libraries=[...],
            library_dirs=[...]),
        # Everything but primes.pyx is included here.
        Extension("*", ["*.pyx"],
            include_dirs=[...],
            libraries=[...],
            library_dirs=[...]),
    ]
    setup(
        name="My hello app",
        ext_modules=cythonize(extensions),
    )

Some useful options to know about are

* ``include_dirs``- list of directories to search for C/C++ header files (in Unix form for portability),
* ``libraries`` - list of library names (not filenames or paths) to link against,
* ``library_dirs`` - list of directories to search for C/C++ libraries at link time.

Note that when using setuptools, you should import it before Cython, otherwise,
both might disagree about the class to use here.

Often, Python packages that offer a C-level API provide a way to find
the necessary C header files::

    from setuptools import Extension, setup
    from Cython.Build import cythonize

    extensions = [
        Extension("*", ["*.pyx"],
            include_dirs=["/usr/local/include"]),
    ]
    setup(
        name="My hello app",
        ext_modules=cythonize(extensions),
    )

If your options are static (for example you do not need to call a tool like
``pkg-config`` to determine them) you can also provide them directly in your
``.pyx`` or ``.pxd`` source file using a special comment block at the start of the file::

    # distutils: libraries = spam eggs
    # distutils: include_dirs = /opt/food/include

If you cimport multiple .pxd files defining libraries, then Cython
merges the list of libraries, so this works as expected (similarly
with other options, like ``include_dirs`` above).

If you have some C files that have been wrapped with Cython and you want to
compile them into your extension, you can define the setuptools ``sources``
parameter::

    # distutils: sources = [helper.c, another_helper.c]

Note that these sources are added to the list of sources of the current
extension module.  Spelling this out in the :file:`setup.py` file looks
as follows::

    from setuptools import Extension, setup
    from Cython.Build import cythonize

    sourcefiles = ['example.pyx', 'helper.c', 'another_helper.c']

    extensions = [Extension("example", sourcefiles)]

    setup(
        ext_modules=cythonize(extensions)
    )

The :class:`~setuptools.Extension` class takes many options, and a fuller explanation can
be found in the :external+setuptools:doc:`setuptools documentation <index>`.

Sometimes this is not enough and you need finer customization of the
setuptools :class:`~setuptools.Extension`.
To do this, you can provide a custom function ``create_extension``
to create the final :class:`~setuptools.Extension` object after Cython has processed
the sources, dependencies and ``# distutils`` directives but before the
file is actually Cythonized.
This function takes 2 arguments ``template`` and ``kwds``, where
``template`` is the :class:`~setuptools.Extension` object given as input to Cython
and ``kwds`` is a :class:`dict` with all keywords which should be used
to create the :class:`~setuptools.Extension`.
The function ``create_extension`` must return a 2-tuple
``(extension, metadata)``, where ``extension`` is the created
:class:`~setuptools.Extension` and ``metadata`` is metadata which will be written
as JSON at the top of the generated C files. This metadata is only used
for debugging purposes, so you can put whatever you want in there
(as long as it can be converted to JSON).
The default function (defined in ``Cython.Build.Dependencies``) is::

    def default_create_extension(template, kwds):
        if 'depends' in kwds:
            include_dirs = kwds.get('include_dirs', []) + ["."]
            depends = resolve_depends(kwds['depends'], include_dirs)
            kwds['depends'] = sorted(set(depends + template.depends))

        t = template.__class__
        ext = t(**kwds)
        if hasattr(template, "py_limited_api"):
            ext.py_limited_api = template.py_limited_api
        metadata = dict(distutils=kwds, module_name=kwds['name'])
        return ext, metadata

In case that you pass a string instead of an :class:`~setuptools.Extension` to
``cythonize()``, the ``template`` will be an :class:`~setuptools.Extension` without
sources. For example, if you do ``cythonize("*.pyx")``,
the ``template`` will be ``Extension(name="*.pyx", sources=[])``.

Just as an example, this adds ``mylib`` as library to every extension::

    from Cython.Build.Dependencies import default_create_extension

    def my_create_extension(template, kwds):
        libs = kwds.get('libraries', []) + ["mylib"]
        kwds['libraries'] = libs
        return default_create_extension(template, kwds)

    ext_modules = cythonize(..., create_extension=my_create_extension)

.. note::

    If you Cythonize in parallel (using the ``nthreads`` argument),
    then the argument to ``create_extension`` must be pickleable.
    In particular, it cannot be a lambda function.


.. _cythonize_arguments:

Cythonize arguments
-------------------

The function :func:`cythonize` can take extra arguments which will allow you to
customize your build.

.. autofunction:: Cython.Build.cythonize

Multiple Cython Files in a Package
===================================

To automatically compile multiple Cython files without listing all of them
explicitly, you can use glob patterns::

    setup(
        ext_modules = cythonize("package/*.pyx")
    )

You can also use glob patterns in :class:`~setuptools.Extension` objects if you pass
them through :func:`cythonize`::

    extensions = [Extension("*", ["*.pyx"])]

    setup(
        ext_modules = cythonize(extensions)
    )


.. _distributing_cython_modules:

Distributing Cython modules
----------------------------

Following recent improvements in the distribution toolchain, it is
not recommended to include generated files in source distributions.
Instead, `require` Cython at build-time to generate the C/C++ files,
as defined in :pep:`518` and :pep:`621`. See :ref:`basic_setup.py`.

It is, however, possible to distribute the generated ``.c`` files together with
your Cython sources, so that users can install your module without needing
to have Cython available.

Doing so allows you to make Cython compilation optional in the
version you distribute. Even if the user has Cython installed, they may not
want to use it just to install your module. Also, the installed version
may not be the same one you used, and may not compile your sources correctly.

This simply means that the :file:`setup.py` file that you ship with will just
be a normal setuptools file on the generated `.c` files, for the basic example
we would have instead::

    from setuptools import Extension, setup

    setup(
        ext_modules = [Extension("example", ["example.c"])]
    )

This is easy to combine with :func:`cythonize` by changing the file extension
of the extension module sources::

    from setuptools import Extension, setup

    USE_CYTHON = ...   # command line option, try-import, ...

    ext = '.pyx' if USE_CYTHON else '.c'

    extensions = [Extension("example", ["example"+ext])]

    if USE_CYTHON:
        from Cython.Build import cythonize
        extensions = cythonize(extensions)

    setup(
        ext_modules = extensions
    )

If you have many extensions and want to avoid the additional complexity in the
declarations, you can declare them with their normal Cython sources and then
call the following function instead of ``cythonize()`` to adapt the sources
list in the :class:`~setuptools.Extension`\ s when not using Cython::

    import os.path

    def no_cythonize(extensions, **_ignore):
        for extension in extensions:
            sources = []
            for sfile in extension.sources:
                path, ext = os.path.splitext(sfile)
                if ext in ('.pyx', '.py'):
                    if extension.language == 'c++':
                        ext = '.cpp'
                    else:
                        ext = '.c'
                    sfile = path + ext
                sources.append(sfile)
            extension.sources[:] = sources
        return extensions

If you want to expose the C-level interface of your library for other
libraries to cimport from, use package_data to install the ``.pxd`` files,
e.g.::

    setup(
        package_data = {
            'my_package': ['*.pxd'],
            'my_package/sub_package': ['*.pxd'],
        },
        ...
    )

These ``.pxd`` files need not have corresponding ``.pyx``
modules if they contain purely declarations of external libraries.
