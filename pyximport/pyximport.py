"""
Import hooks; when installed with the install() function, these hooks
allow importing .pyx files as if they were Python modules.

If you want the hook installed every time you run Python
you can add it to your Python version by adding these lines to
sitecustomize.py (which you can create from scratch in site-packages
if it doesn't exist there or somewhere else on your python path)::

    import pyximport
    pyximport.install()

For instance on the Mac with a non-system Python 2.3, you could create
sitecustomize.py with only those two lines at
/usr/local/lib/python2.3/site-packages/sitecustomize.py .

A custom distutils.core.Extension instance and setup() args
(Distribution) for for the build can be defined by a <modulename>.pyxbld
file like:

# examplemod.pyxbld
def make_ext(modname, pyxfilename):
    from distutils.extension import Extension
    return Extension(name = modname,
                     sources=[pyxfilename, 'hello.c'],
                     include_dirs=['/myinclude'] )
def make_setup_args():
    return dict(script_args=["--compiler=mingw32"])

Extra dependencies can be defined by a <modulename>.pyxdep .
See README.

Since Cython 0.11, the :mod:`pyximport` module also has experimental
compilation support for normal Python modules.  This allows you to
automatically run Cython on every .pyx and .py module that Python
imports, including parts of the standard library and installed
packages.  Cython will still fail to compile a lot of Python modules,
in which case the import mechanism will fall back to loading the
Python source modules instead.  The .py import mechanism is installed
like this::

    pyximport.install(pyimport = True)

Running this module as a top-level script will run a test and then print
the documentation.
"""
import sys

from pyximport.common import initialize

if sys.version_info.major == 2:
    from pyximport._pyximport2 import PyxImporter, PyImporter
else:
    from pyximport._pyximport3 import PyxImportMetaFinder as PyxImporter, PyImportMetaFinder as PyImporter

mod_name = "pyximport"

def _have_importers():
    has_py_importer = False
    has_pyx_importer = False
    for importer in sys.meta_path:
        if isinstance(importer, PyxImporter):
            if isinstance(importer, PyImporter):
                has_py_importer = True
            else:
                has_pyx_importer = True

    return has_py_importer, has_pyx_importer


def install(pyximport=True, pyimport=False, build_dir=None, build_in_temp=True,
            setup_args=None, reload_support=False,
            load_py_module_on_import_failure=False, inplace=False,
            language_level=None):
    """ Main entry point for pyxinstall.

    Call this to install the ``.pyx`` import hook in
    your meta-path for a single Python process.  If you want it to be
    installed whenever you use Python, add it to your ``sitecustomize``
    (as described above).

    :param pyximport: If set to False, does not try to import ``.pyx`` files.

    :param pyimport: You can pass ``pyimport=True`` to also
        install the ``.py`` import hook
        in your meta-path.  Note, however, that it is rather experimental,
        will not work at all for some ``.py`` files and packages, and will
        heavily slow down your imports due to search and compilation.
        Use at your own risk.

    :param build_dir: By default, compiled modules will end up in a ``.pyxbld``
        directory in the user's home directory.  Passing a different path
        as ``build_dir`` will override this.

    :param build_in_temp: If ``False``, will produce the C files locally. Working
        with complex dependencies and debugging becomes more easy. This
        can principally interfere with existing files of the same name.

    :param setup_args: Dict of arguments for Distribution.
        See ``distutils.core.setup()``.

    :param reload_support: Enables support for dynamic
        ``reload(my_module)``, e.g. after a change in the Cython code.
        Additional files ``<so_path>.reloadNN`` may arise on that account, when
        the previously loaded module file cannot be overwritten.

    :param load_py_module_on_import_failure: If the compilation of a ``.py``
        file succeeds, but the subsequent import fails for some reason,
        retry the import with the normal ``.py`` module instead of the
        compiled module.  Note that this may lead to unpredictable results
        for modules that change the system state during their import, as
        the second import will rerun these modifications in whatever state
        the system was left after the import of the compiled module
        failed.

    :param inplace: Install the compiled module
        (``.so`` for Linux and Mac / ``.pyd`` for Windows)
        next to the source file.

    :param language_level: The source language level to use: 2 or 3.
        The default is to use the language level of the current Python
        runtime for .py files and Py2 for ``.pyx`` files.
    """

    initialize(build_dir, build_in_temp, setup_args, reload_support, load_py_module_on_import_failure)

    has_py_importer, has_pyx_importer = _have_importers()
    py_importer, pyx_importer = None, None

    if pyimport and not has_py_importer:
        py_importer = PyImporter(pyxbuild_dir=build_dir, inplace=inplace,
                                 language_level=language_level)
        # make sure we import Cython before we install the import hook
        import Cython.Compiler.Main, Cython.Compiler.Pipeline, Cython.Compiler.Optimize
        sys.meta_path.insert(0, py_importer)

    if pyximport and not has_pyx_importer:
        pyx_importer = PyxImporter(pyxbuild_dir=build_dir, inplace=inplace,
                                   language_level=language_level)
        sys.meta_path.append(pyx_importer)

    return py_importer, pyx_importer


def uninstall(py_importer, pyx_importer):
    """
    Uninstall an import hook.
    """
    try:
        sys.meta_path.remove(py_importer)
    except ValueError:
        pass

    try:
        sys.meta_path.remove(pyx_importer)
    except ValueError:
        pass


# MAIN

def show_docs():
    import __main__
    __main__.__name__ = mod_name
    for name in dir(__main__):
        item = getattr(__main__, name)
        try:
            setattr(item, "__module__", mod_name)
        except (AttributeError, TypeError):
            pass
    help(__main__)


if __name__ == '__main__':
    show_docs()
