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

Running this module as a top-level script will run a test and then print
the documentation.

This code is based on the Py2.3+ import protocol as described in PEP 302.
"""
import sys
import os
import glob
import imp
import pyxbuild
from distutils.dep_util import newer
from distutils.extension import Extension

try:
    import hashlib
except ImportError:
    import md5 as hashlib

mod_name = "pyximport"

assert sys.hexversion >= 0x2030000, "need Python 2.3 or later"

PYX_EXT = ".pyx"
PYXDEP_EXT = ".pyxdep"
PYXBLD_EXT = ".pyxbld"

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
    extra = "_" + hashlib.md5(open(pyxfilename).read()).hexdigest()  
#    modname = modname + extra
    extension_mod = handle_special_build(modname, pyxfilename)
    if not extension_mod:
        extension_mod = Extension(name = modname, sources=[pyxfilename])
    return extension_mod

def handle_special_build(modname, pyxfilename):
    special_build = os.path.splitext(pyxfilename)[0] + PYXBLD_EXT

    if not os.path.exists(special_build): 
        ext = None
    else:
        globls = {}
        locs = {}
        # execfile(special_build, globls, locs)
        # ext = locs["make_ext"](modname, pyxfilename)
        mod = imp.load_source("XXXX", special_build, open(special_build))
        ext = mod.make_ext(modname, pyxfilename)
        assert ext and ext.sources, ("make_ext in %s did not return Extension" 
                                     % special_build)
        ext.sources = [os.path.join(os.path.dirname(special_build), source) 
                       for source in ext.sources]
    return ext

def handle_dependencies(pyxfilename):
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
        _test_files[:] = []

        # if any file that the pyxfile depends upon is newer than
        # the pyx file, 'touch' the pyx file so that distutils will
        # be tricked into rebuilding it.
        for file in files:
            if newer(file, pyxfilename):
                print "Rebuilding because of ", file
                filetime = os.path.getmtime(file)
                os.utime(pyxfilename, (filetime, filetime))
                _test_files.append(file)

def build_module(name, pyxfilename):
    assert os.path.exists(pyxfilename), (
        "Path does not exist: %s" % pyxfilename)
    handle_dependencies(pyxfilename)

    extension_mod = get_distutils_extension(name, pyxfilename)

    so_path = pyxbuild.pyx_to_dll(pyxfilename, extension_mod)
    assert os.path.exists(so_path), "Cannot find: %s" % so_path

    junkpath = os.path.join(os.path.dirname(so_path), name+"_*")
    junkstuff = glob.glob(junkpath)
    for path in junkstuff:
        if path!=so_path:
            try:
                os.remove(path)
            except IOError:
                print "Couldn't remove ", path

    return so_path

def load_module(name, pyxfilename):
    so_path = build_module(name, pyxfilename)
    mod = imp.load_dynamic(name, so_path)
    assert mod.__file__ == so_path, (mod.__file__, so_path)
    return mod


# import hooks

class PyxImporter(object):
    def __init__(self):
        pass

    def find_module(self, fullname, package_path=None):
        #print "SEARCHING", fullname, package_path
        if '.' in fullname:
            mod_parts = fullname.split('.')
            package = '.'.join(mod_parts[:-1])
            module_name = mod_parts[-1]
        else:
            package = None
            module_name = fullname
        pyx_module_name = module_name + PYX_EXT
        # this may work, but it returns the file content, not its path
        #import pkgutil
        #pyx_source = pkgutil.get_data(package, pyx_module_name)

        if package_path:
            paths = package_path
        else:
            paths = sys.path
        join_path = os.path.join
        is_file = os.path.isfile
        for path in filter(os.path.isdir, paths):
            for filename in os.listdir(path):
                if filename == pyx_module_name:
                    return PyxLoader(fullname, join_path(path, filename))
                elif filename == module_name:
                    package_path = join_path(path, filename)
                    init_path = join_path(package_path, '__init__' + PYX_EXT)
                    if is_file(init_path):
                        return PyxLoader(fullname, package_path, init_path)
        # not found, normal package, not a .pyx file, none of our business
        return None

class PyxLoader(object):
    def __init__(self, fullname, path, init_path=None):
        self.fullname, self.path, self.init_path = fullname, path, init_path

    def load_module(self, fullname):
        assert self.fullname == fullname, (
            "invalid module, expected %s, got %s" % (
            self.fullname, fullname))
        if self.init_path:
            # package
            #print "PACKAGE", fullname
            module = load_module(fullname, self.init_path)
            module.__path__ = [self.path]
        else:
            #print "MODULE", fullname
            module = load_module(fullname, self.path)
        return module


def install():
    """Main entry point. call this to install the import hook in your
    for a single Python process. If you want it to be installed whenever
    you use Python, add it to your sitecustomize (as described above).

    """
    for importer in sys.meta_path:
        if isinstance(importer, PyxImporter):
            return
    importer = PyxImporter() # ('~/.pyxbuild')
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
