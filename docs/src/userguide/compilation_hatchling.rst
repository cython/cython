************************
Compiling with hatchling
************************

Hatchling is a Python build backend. It does not
appear to focus much of extension modules, however the
`hatch-cython plugin <https://github.com/joshua-auchincloss/hatch-cython>`_
does provide Cython support.

All of the details are contained within the :file:`pyproject.toml` file::

    [build-system]
    requires = ["hatchling", "hatch-cython", "Cython", "setuptools"]
    build-backend = "hatchling.build"

    [tool.hatch.build.targets.wheel.hooks.cython]
    dependencies = ["hatch-cython"]

    [project]
    name = "example"
    version = "1.0.0"

No source files are specified in this case because it automatically searches
under the "example" directory (or whatever your project name is) to find
suitable :file:`*.pyx` files to compile with Cython.  If you want to
customize this behaviour then use ``[build.targets.wheel.hooks.cython.options.files]``.

:mod:``hatch-cython`` also allows control of things like Cython compiler directives
and C compiler macros.  Additionally it can invoke the
:ref:`Tempita templating language <tempita>` for you if you want to programmatically
generate your Cython source code.
