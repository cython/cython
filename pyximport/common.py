import glob
import os.path
import sys

DEBUG_IMPORT = False
PYX_EXT = ".pyx"
PY_EXT = ".py"
PYXBLD_EXT = ".pyxbld"
PYXDEP_EXT = ".pyxdep"
pyxargs = None


class PyxArgs(object):
    build_dir = True
    build_in_temp = True
    setup_args = {}


def _print(message, args):
    if args:
        message = message % args
    print(message)


def _debug(message, *args):
    if DEBUG_IMPORT:
        _print(message, args)


def _info(message, *args):
    _print(message, args)


if sys.version_info.major == 2:
    def load_source(file_path):
        import imp
        return imp.load_source("XXXX", file_path, open(file_path))
else:
    def load_source(file_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("XXXX", file_path)
        return importlib.util.module_from_spec(spec)

def get_distutils_extension(modname, pyxfilename, language_level=None):
    extension_mod,setup_args = handle_special_build(modname, pyxfilename)
    if not extension_mod:
        if not isinstance(pyxfilename, str):
            # distutils is stupid in Py2 and requires exactly 'str'
            # => encode accidentally coerced unicode strings back to str
            pyxfilename = pyxfilename.encode(sys.getfilesystemencoding())
        from distutils.extension import Extension
        extension_mod = Extension(name=modname, sources=[pyxfilename])
        if language_level is not None:
            extension_mod.cython_directives = {'language_level': language_level}
    return extension_mod,setup_args


def handle_special_build(modname, pyxfilename):
    special_build = os.path.splitext(pyxfilename)[0] + PYXBLD_EXT
    ext = None
    setup_args={}
    if os.path.exists(special_build):
        # python3:
        # spec = importlib.util.spec_from_file_location(module_name, file_path)
        # module = importlib.util.module_from_spec(spec)
        mod = load_source(special_build)
        make_ext = getattr(mod,'make_ext',None)
        if make_ext:
            ext = make_ext(modname, pyxfilename)
            assert ext and ext.sources, "make_ext in %s did not return Extension" % special_build
        make_setup_args = getattr(mod, 'make_setup_args',None)
        if make_setup_args:
            setup_args = make_setup_args()
            assert isinstance(setup_args,dict), ("make_setup_args in %s did not return a dict"
                                         % special_build)
        assert set or setup_args, ("neither make_ext nor make_setup_args %s"
                                         % special_build)
        ext.sources = [os.path.join(os.path.dirname(special_build), source)
                       for source in ext.sources]
    return ext, setup_args


def handle_dependencies(pyxfilename):
    testing = '_test_files' in globals()
    dependfile = os.path.splitext(pyxfilename)[0] + PYXDEP_EXT

    # by default let distutils decide whether to rebuild on its own
    # (it has a better idea of what the output file will be)

    # but we know more about dependencies so force a rebuild if
    # some of the dependencies are newer than the pyxfile.
    if os.path.exists(dependfile):
        depends = open(dependfile).readlines()
        depends = [depend.strip() for depend in depends]

        # gather dependencies in the "files" variable
        # the dependency file is itself a dependency
        files = [dependfile]
        for depend in depends:
            fullpath = os.path.join(os.path.dirname(dependfile),
                                    depend)
            files.extend(glob.glob(fullpath))

        # only for unit testing to see we did the right thing
        if testing:
            _test_files[:] = []  #$pycheck_no

        # if any file that the pyxfile depends upon is newer than
        # the pyx file, 'touch' the pyx file so that distutils will
        # be tricked into rebuilding it.
        for file in files:
            from distutils.dep_util import newer
            if newer(file, pyxfilename):
                _debug("Rebuilding %s because of %s", pyxfilename, file)
                filetime = os.path.getmtime(file)
                os.utime(pyxfilename, (filetime, filetime))
                if testing:
                    _test_files.append(file)


def build_module(name, pyxfilename, pyxbuild_dir=None, inplace=False, language_level=None):
    assert os.path.exists(pyxfilename), "Path does not exist: %s" % pyxfilename
    handle_dependencies(pyxfilename)

    extension_mod, setup_args = get_distutils_extension(name, pyxfilename, language_level)
    build_in_temp = pyxargs.build_in_temp
    sargs = pyxargs.setup_args.copy()
    sargs.update(setup_args)
    build_in_temp = sargs.pop('build_in_temp',build_in_temp)

    from . import pyxbuild
    so_path = pyxbuild.pyx_to_dll(pyxfilename, extension_mod,
                                  build_in_temp=build_in_temp,
                                  pyxbuild_dir=pyxbuild_dir,
                                  setup_args=sargs,
                                  inplace=inplace,
                                  reload_support=pyxargs.reload_support)
    assert os.path.exists(so_path), "Cannot find: %s" % so_path

    junkpath = os.path.join(os.path.dirname(so_path), name+"_*")  #very dangerous with --inplace ? yes, indeed, trying to eat my files ;)
    junkstuff = glob.glob(junkpath)
    for path in junkstuff:
        if path != so_path:
            try:
                os.remove(path)
            except IOError:
                _info("Couldn't remove %s", path)

    return so_path


def initialize(build_dir=None, build_in_temp=True,
            setup_args=None, reload_support=False,
            load_py_module_on_import_failure=False):
    if setup_args is None:
        setup_args = {}
    if not build_dir:
        build_dir = os.path.join(os.path.expanduser('~'), PYXBLD_EXT)

    global pyxargs
    pyxargs = PyxArgs()
    pyxargs.build_dir = build_dir
    pyxargs.build_in_temp = build_in_temp
    pyxargs.setup_args = (setup_args or {}).copy()
    pyxargs.reload_support = reload_support
    pyxargs.load_py_module_on_import_failure = load_py_module_on_import_failure
