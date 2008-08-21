"""
Import hooks; when installed (with the install()) function, these hooks 
allow importing .pyx files as if they were Python modules.

If you want the hook installed every time you run Python
you can add it to your Python version by adding these lines to
sitecustomize.py (which you can create from scratch in site-packages 
if it doesn't exist there are somewhere else on your python path)

import pyximport
pyximport.install()

For instance on  the Mac with Python 2.3 built from CVS, you could 
create sitecustomize.py with only those two lines at
/usr/local/lib/python2.3/site-packages/sitecustomize.py .

Running this module as a top-level script will run a test and then print
the documentation.

This code was modeled on Quixote's ptl_import.
"""
import sys, os, shutil
import imp, ihooks, glob, md5
import __builtin__
import pyxbuild
from distutils.dep_util import newer
from distutils.extension import Extension

mod_name = "pyximport"

assert sys.hexversion >= 0x20000b1, "need Python 2.0b1 or later"

PYX_FILE_TYPE = 1011
PYX_EXT = ".pyx"
PYXDEP_EXT = ".pyxdep"
PYXBLD_EXT = ".pyxbld"
_test_files = []

class PyxHooks (ihooks.Hooks):
    """Import hook that declares our suffixes. Let install() install it."""
    def get_suffixes (self):
        # add our suffixes
        return imp.get_suffixes() + [(PYX_EXT, "r", PYX_FILE_TYPE)]

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

    extra = "_" + md5.md5(open(pyxfilename).read()).hexdigest()  
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

class PyxLoader (ihooks.ModuleLoader):
    """Load a module. It checks whether a file is a .pyx and returns it.
    Otherwise it lets the ihooks base class handle it. Let install() 
    install it."""

    def load_module (self, name, stuff):
        # If it's a Pyrex file, load it specially.
        if stuff[2][2] == PYX_FILE_TYPE:
            file, pyxfilename, info = stuff
            (suff, mode, type) = info
            if file:
                file.close()
	    return load_module(name, pyxfilename)
        else:
            # Otherwise, use the default handler for loading
            return ihooks.ModuleLoader.load_module( self, name, stuff)

try:
    import cimport
except ImportError:
    cimport = None

class cModuleImporter(ihooks.ModuleImporter):
    """This was just left in from the Quixote implementation. I think
    it allows a performance enhancement if you have the cimport module
    from Quixote. Let install() install it."""
    def __init__(self, loader=None):
        self.loader = loader or ihooks.ModuleLoader()
        cimport.set_loader(self.find_import_module)

    def find_import_module(self, fullname, subname, path):
        stuff = self.loader.find_module(subname, path)
        if not stuff:
            return None
        return self.loader.load_module(fullname, stuff)

    def install(self):
        self.save_import_module = __builtin__.__import__
        self.save_reload = __builtin__.reload
        if not hasattr(__builtin__, 'unload'):
            __builtin__.unload = None
        self.save_unload = __builtin__.unload
        __builtin__.__import__ = cimport.import_module
        __builtin__.reload = cimport.reload_module
        __builtin__.unload = self.unload

_installed = 0

def install():
    """Main entry point. call this to install the import hook in your
    for a single Python process. If you want it to be installed whenever
    you use Python, add it to your sitecustomize (as described above).

    """
    global _installed
    if not _installed:
        hooks = PyxHooks()
        loader = PyxLoader(hooks)
        if cimport is not None:
            importer = cModuleImporter(loader)
        else:
            importer = ihooks.ModuleImporter(loader)
        ihooks.install(importer)
        _installed = 1

def on_remove_file_error(func, path, excinfo):
    print "Sorry! Could not remove a temp file:", path
    print "Extra information."
    print func, excinfo
    print "You may want to delete this yourself when you get a chance."

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
