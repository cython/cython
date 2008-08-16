"""Build a Pyrex file from .pyx source to .so loadable module using
the installed distutils infrastructure. Call:

out_fname = pyx_to_dll("foo.pyx")
"""
import os, md5

import distutils
from distutils.dist import Distribution
from distutils.errors import DistutilsArgError, DistutilsError, CCompilerError
from distutils.extension import Extension
from distutils.util import grok_environment_error
from Cython.Distutils import build_ext
import shutil

DEBUG = 0
def pyx_to_dll(filename, ext = None, force_rebuild = 0):
    """Compile a PYX file to a DLL and return the name of the generated .so 
       or .dll ."""
    assert os.path.exists(filename)

    path, name = os.path.split(filename)

    if not ext:
        modname, extension = os.path.splitext(name)
	assert extension == ".pyx", extension
        ext = Extension(name=modname, sources=[filename])

    if DEBUG:
        quiet = "--verbose"
    else:
	quiet = "--quiet"
    args = [quiet, "build_ext"]
    if force_rebuild:
        args.append("--force")
    dist = Distribution({"script_name": None, "script_args": args})
    if not dist.ext_modules:
        dist.ext_modules = []
    dist.ext_modules.append(ext)
    dist.cmdclass = {'build_ext': build_ext}
    build = dist.get_command_obj('build')
    build.build_base = os.path.join(path, "_pyxbld")

    try:
        ok = dist.parse_command_line()
    except DistutilsArgError, msg:
        raise

    if DEBUG:
        print "options (after parsing command line):"
        dist.dump_option_dicts()
    assert ok


    try:
        dist.run_commands()
        return dist.get_command_obj("build_ext").get_outputs()[0]
    except KeyboardInterrupt:
        raise SystemExit, "interrupted"
    except (IOError, os.error), exc:
        error = grok_environment_error(exc)

        if DEBUG:
            sys.stderr.write(error + "\n")
            raise
        else:
            raise SystemExit, error

    except (DistutilsError,
        CCompilerError), msg:
        if DEBUG:
            raise
        else:
            raise SystemExit, "error: " + str(msg)

if __name__=="__main__":
    pyx_to_dll("dummy.pyx")
    import test

