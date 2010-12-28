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

# examplemod.pyxbdl
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

This code is based on the Py2.3+ import protocol as described in PEP 302.
"""

import sys
import os
import glob
import imp

mod_name = "pyximport"

assert sys.hexversion >= 0x2030000, "need Python 2.3 or later"

PYX_EXT = ".pyx"
PYXDEP_EXT = ".pyxdep"
PYXBLD_EXT = ".pyxbld"

DEBUG_IMPORT = False

# Performance problem: for every PYX file that is imported, we will 
# invoke the whole distutils infrastructure even if the module is 
# already built. It might be more efficient to only do it when the 
# mod time of the .pyx is newer than the mod time of the .so but
# the question is how to get distutils to tell me the name of the .so
# before it builds it. Maybe it is easy...but maybe the peformance
# issue isn't real.
def _load_pyrex(name, filename):
    "Load a pyrex file given a name and filename."

def get_distutils_extension(modname, pyxfilename):
#    try:
#        import hashlib
#    except ImportError:
#        import md5 as hashlib
#    extra = "_" + hashlib.md5(open(pyxfilename).read()).hexdigest()  
#    modname = modname + extra
    extension_mod,setup_args = handle_special_build(modname, pyxfilename)
    if not extension_mod:
        from distutils.extension import Extension
        extension_mod = Extension(name = modname, sources=[pyxfilename])
    return extension_mod,setup_args

def handle_special_build(modname, pyxfilename):
    special_build = os.path.splitext(pyxfilename)[0] + PYXBLD_EXT
    ext = None
    setup_args={}
    if os.path.exists(special_build): 
        # globls = {}
        # locs = {}
        # execfile(special_build, globls, locs)
        # ext = locs["make_ext"](modname, pyxfilename)
        mod = imp.load_source("XXXX", special_build, open(special_build))
        make_ext = getattr(mod,'make_ext',None)
        if make_ext:
            ext = make_ext(modname, pyxfilename)
            assert ext and ext.sources, ("make_ext in %s did not return Extension" 
                                         % special_build)
        make_setup_args = getattr(mod,'make_setup_args',None)
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
                print("Rebuilding because of ", file)
                filetime = os.path.getmtime(file)
                os.utime(pyxfilename, (filetime, filetime))
                if testing:
                    _test_files.append(file)

def build_module(name, pyxfilename, pyxbuild_dir=None):
    assert os.path.exists(pyxfilename), (
        "Path does not exist: %s" % pyxfilename)
    handle_dependencies(pyxfilename)

    extension_mod,setup_args = get_distutils_extension(name, pyxfilename)
    build_in_temp=pyxargs.build_in_temp
    sargs=pyxargs.setup_args.copy()
    sargs.update(setup_args)
    build_in_temp=sargs.pop('build_in_temp',build_in_temp)

    import pyxbuild
    so_path = pyxbuild.pyx_to_dll(pyxfilename, extension_mod,
                                  build_in_temp=build_in_temp,
                                  pyxbuild_dir=pyxbuild_dir,
                                  setup_args=sargs,
                                  reload_support=pyxargs.reload_support)
    assert os.path.exists(so_path), "Cannot find: %s" % so_path
    
    junkpath = os.path.join(os.path.dirname(so_path), name+"_*") #very dangerous with --inplace ?
    junkstuff = glob.glob(junkpath)
    for path in junkstuff:
        if path!=so_path:
            try:
                os.remove(path)
            except IOError:
                print("Couldn't remove ", path)

    return so_path

def load_module(name, pyxfilename, pyxbuild_dir=None):
    try:
        so_path = build_module(name, pyxfilename, pyxbuild_dir)
        mod = imp.load_dynamic(name, so_path)
        assert mod.__file__ == so_path, (mod.__file__, so_path)
    except Exception, e:
        import traceback
        raise ImportError("Building module failed: %s" %
                          traceback.format_exception_only(*sys.exc_info()[:2])),None,sys.exc_info()[2]
    return mod


# import hooks

class PyxImporter(object):
    """A meta-path importer for .pyx files.
    """
    def __init__(self, extension=PYX_EXT, pyxbuild_dir=None):
        self.extension = extension
        self.pyxbuild_dir = pyxbuild_dir

    def find_module(self, fullname, package_path=None):
        if fullname in sys.modules  and  not pyxargs.reload_support:
            return None  # only here when reload() 
        try:
            fp, pathname, (ext,mode,ty) = imp.find_module(fullname,package_path)
            if fp: fp.close()  # Python should offer a Default-Loader to avoid this double find/open!
            if ty!=imp.C_EXTENSION: # only when an extension, check if we have a .pyx next!
                return None

            # find .pyx fast, when .so/.pyd exist --inplace
            pyxpath = os.path.splitext(pathname)[0]+self.extension
            if os.path.isfile(pyxpath):
                return PyxLoader(fullname, pyxpath,
                                 pyxbuild_dir=self.pyxbuild_dir)
            
            # .so/.pyd's on PATH should not be remote from .pyx's
            # think no need to implement PyxArgs.importer_search_remote here?
                
        except ImportError:
            pass

        # searching sys.path ...
                
        #if DEBUG_IMPORT:  print "SEARCHING", fullname, package_path
        if '.' in fullname: # only when package_path anyway?
            mod_parts = fullname.split('.')
            module_name = mod_parts[-1]
        else:
            module_name = fullname
        pyx_module_name = module_name + self.extension
        # this may work, but it returns the file content, not its path
        #import pkgutil
        #pyx_source = pkgutil.get_data(package, pyx_module_name)

        if package_path:
            paths = package_path
        else:
            paths = sys.path
        join_path = os.path.join
        is_file = os.path.isfile
        #is_dir = os.path.isdir
        sep = os.path.sep
        for path in paths:
            if not path:
                path = os.getcwd()
            if is_file(path+sep+pyx_module_name):
                return PyxLoader(fullname, join_path(path, pyx_module_name),
                                 pyxbuild_dir=self.pyxbuild_dir)
                
        # not found, normal package, not a .pyx file, none of our business
        return None

class PyImporter(PyxImporter):
    """A meta-path importer for normal .py files.
    """
    def __init__(self, pyxbuild_dir=None):
        self.super = super(PyImporter, self)
        self.super.__init__(extension='.py', pyxbuild_dir=pyxbuild_dir)
        self.uncompilable_modules = {}
        self.blocked_modules = ['Cython']

    def find_module(self, fullname, package_path=None):
        if fullname in sys.modules:
            return None
        if fullname.startswith('Cython.'):
            return None
        if fullname in self.blocked_modules:
            # prevent infinite recursion
            return None
        if DEBUG_IMPORT:
            print("trying import of module", fullname)
        if fullname in self.uncompilable_modules:
            path, last_modified = self.uncompilable_modules[fullname]
            try:
                new_last_modified = os.stat(path).st_mtime
                if new_last_modified > last_modified:
                    # import would fail again
                    return None
            except OSError:
                # module is no longer where we found it, retry the import
                pass

        self.blocked_modules.append(fullname)
        try:
            importer = self.super.find_module(fullname, package_path)
            if importer is not None:
                if DEBUG_IMPORT:
                    print("importer found")
                try:
                    if importer.init_path:
                        path = importer.init_path
                    else:
                        path = importer.path
                    build_module(fullname, path,
                                 pyxbuild_dir=self.pyxbuild_dir)
                except Exception, e:
                    if DEBUG_IMPORT:
                        import traceback
                        traceback.print_exc()
                    # build failed, not a compilable Python module
                    try:
                        last_modified = os.stat(path).st_mtime
                    except OSError:
                        last_modified = 0
                    self.uncompilable_modules[fullname] = (path, last_modified)
                    importer = None
        finally:
            self.blocked_modules.pop()
        return importer

class PyxLoader(object):
    def __init__(self, fullname, path, init_path=None, pyxbuild_dir=None):
        self.fullname = fullname
        self.path, self.init_path = path, init_path
        self.pyxbuild_dir = pyxbuild_dir

    def load_module(self, fullname):
        assert self.fullname == fullname, (
            "invalid module, expected %s, got %s" % (
            self.fullname, fullname))
        if self.init_path:
            # package
            #print "PACKAGE", fullname
            module = load_module(fullname, self.init_path,
                                 self.pyxbuild_dir)
            module.__path__ = [self.path]
        else:
            #print "MODULE", fullname
            module = load_module(fullname, self.path,
                                 self.pyxbuild_dir)
        return module


#install args
class PyxArgs(object):
    build_dir=True
    build_in_temp=True
    setup_args={}   #None

##pyxargs=None   
    
def install(pyximport=True, pyimport=False, build_dir=None, build_in_temp=True,
            setup_args={}, reload_support=False ):
    """Main entry point. Call this to install the .pyx import hook in
    your meta-path for a single Python process.  If you want it to be
    installed whenever you use Python, add it to your sitecustomize
    (as described above).

    You can pass ``pyimport=True`` to also install the .py import hook
    in your meta-path.  Note, however, that it is highly experimental,
    will not work for most .py files, and will therefore only slow
    down your imports.  Use at your own risk.

    By default, compiled modules will end up in a ``.pyxbld``
    directory in the user's home directory.  Passing a different path
    as ``build_dir`` will override this.

    ``build_in_temp=False`` will produce the C files locally. Working
    with complex dependencies and debugging becomes more easy. This
    can principally interfere with existing files of the same name.
    build_in_temp can be overriden by <modulename>.pyxbld/make_setup_args()
    by a dict item of 'build_in_temp'

    ``setup_args``: dict of arguments for Distribution - see
    distutils.core.setup() . They are extended/overriden by those of
    <modulename>.pyxbld/make_setup_args()

    ``reload_support``:  Enables support for dynamic
    reload(<pyxmodulename>), e.g. after a change in the Cython code.
    Additional files <so_path>.reloadNN may arise on that account, when
    the previously loaded module file cannot be overwritten.
    """
    if not build_dir:
        build_dir = os.path.expanduser('~/.pyxbld')
        
    global pyxargs
    pyxargs = PyxArgs()  #$pycheck_no
    pyxargs.build_dir = build_dir
    pyxargs.build_in_temp = build_in_temp
    pyxargs.setup_args = (setup_args or {}).copy()
    pyxargs.reload_support = reload_support

    has_py_importer = False
    has_pyx_importer = False
    for importer in sys.meta_path:
        if isinstance(importer, PyxImporter):
            if isinstance(importer, PyImporter):
                has_py_importer = True
            else:
                has_pyx_importer = True

    if pyimport and not has_py_importer:
        importer = PyImporter(pyxbuild_dir=build_dir)
        sys.meta_path.insert(0, importer)

    if pyximport and not has_pyx_importer:
        importer = PyxImporter(pyxbuild_dir=build_dir)
        sys.meta_path.append(importer)


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
