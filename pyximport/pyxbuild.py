"""Build a Pyrex file from .pyx source to .so loadable module using
the installed distutils infrastructure. Call:

out_fname = pyx_to_dll("foo.pyx")
"""
import os
import sys

import distutils
from distutils.dist import Distribution
from distutils.errors import DistutilsArgError, DistutilsError, CCompilerError
from distutils.extension import Extension
from distutils.util import grok_environment_error
try:
    from Cython.Distutils import build_ext
    HAS_CYTHON = True
except ImportError:
    HAS_CYTHON = False
import shutil

DEBUG = 0
def pyx_to_dll(filename, ext = None, force_rebuild = 0,
               build_in_temp=False, pyxbuild_dir=None):
    """Compile a PYX file to a DLL and return the name of the generated .so 
       or .dll ."""
    assert os.path.exists(filename), "Could not find %s" % os.path.abspath(filename)

    path, name = os.path.split(filename)

    if not ext:
        modname, extension = os.path.splitext(name)
        assert extension in (".pyx", ".py"), extension
        if not HAS_CYTHON:
            filename = filename[:-len(extension)] + '.c'
        ext = Extension(name=modname, sources=[filename])

    if not pyxbuild_dir:
        pyxbuild_dir = os.path.join(path, "_pyxbld")

    if DEBUG:
        quiet = "--verbose"
    else:
        quiet = "--quiet"
    args = [quiet, "build_ext"]
    if force_rebuild:
        args.append("--force")
    if HAS_CYTHON and build_in_temp:
        args.append("--pyrex-c-in-temp")
    dist = Distribution({"script_name": None, "script_args": args})
    if not dist.ext_modules:
        dist.ext_modules = []
    dist.ext_modules.append(ext)
    if HAS_CYTHON:
        dist.cmdclass = {'build_ext': build_ext}
    build = dist.get_command_obj('build')
    build.build_base = pyxbuild_dir

    try:
        ok = dist.parse_command_line()
    except DistutilsArgError:
        raise

    if DEBUG:
        print("options (after parsing command line):")
        dist.dump_option_dicts()
    assert ok


    try:
        dist.run_commands()
        return dist.get_command_obj("build_ext").get_outputs()[0]
    except KeyboardInterrupt:
        sys.exit(1)
    except (IOError, os.error):
        exc = sys.exc_info()[1]
        error = grok_environment_error(exc)

        if DEBUG:
            sys.stderr.write(error + "\n")
            raise
        else:
            raise RuntimeError(error)

    except (DistutilsError, CCompilerError):
        if DEBUG:
            raise
        else:
            exc = sys.exc_info()[1]
            raise RuntimeError(repr(exc))

if __name__=="__main__":
    pyx_to_dll("dummy.pyx")
    import test

