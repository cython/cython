"""
This code is based on the Py2.3+ import protocol as described in PEP 302.
"""

import imp
import os
import sys
from zipimport import zipimporter, ZipImportError
from pyximport.common import build_module, _debug, DEBUG_IMPORT, pyxargs, PYX_EXT, PY_EXT


# Performance problem: for every PYX file that is imported, we will
# invoke the whole distutils infrastructure even if the module is
# already built. It might be more efficient to only do it when the
# mod time of the .pyx is newer than the mod time of the .so but
# the question is how to get distutils to tell me the name of the .so
# before it builds it. Maybe it is easy...but maybe the performance
# issue isn't real.
def _load_pyrex(name, filename):
    "Load a pyrex file given a name and filename."


def load_module(name, pyxfilename, pyxbuild_dir=None, is_package=False,
                build_inplace=False, language_level=None, so_path=None):
    try:
        if so_path is None:
            if is_package:
                module_name = name + '.__init__'
            else:
                module_name = name
            so_path = build_module(module_name, pyxfilename, pyxbuild_dir,
                                   inplace=build_inplace, language_level=language_level)
        mod = imp.load_dynamic(name, so_path)
        if is_package and not hasattr(mod, '__path__'):
            mod.__path__ = [os.path.dirname(so_path)]
        assert mod.__file__ == so_path, (mod.__file__, so_path)
    except Exception as failure_exc:
        _debug("Failed to load extension module: %r" % failure_exc)
        if pyxargs.load_py_module_on_import_failure and pyxfilename.endswith(PY_EXT):
            # try to fall back to normal import
            mod = imp.load_source(name, pyxfilename)
            assert mod.__file__ in (pyxfilename, pyxfilename+'c', pyxfilename+'o'), (mod.__file__, pyxfilename)
        else:
            tb = sys.exc_info()[2]
            import traceback
            exc = ImportError("Building module %s failed: %s" % (
                name, traceback.format_exception_only(*sys.exc_info()[:2])))
            if sys.version_info[0] >= 3:
                raise exc.with_traceback(tb)
            else:
                exec("raise exc, None, tb", {'exc': exc, 'tb': tb})
    return mod


# import hooks

class PyxImporter(object):
    """A meta-path importer for .pyx files.
    """
    def __init__(self, extension=PYX_EXT, pyxbuild_dir=None, inplace=False,
                 language_level=None):
        self.extension = extension
        self.pyxbuild_dir = pyxbuild_dir
        self.inplace = inplace
        self.language_level = language_level

    def find_module(self, fullname, package_path=None):
        if fullname in sys.modules  and  not pyxargs.reload_support:
            return None  # only here when reload()

        # package_path might be a _NamespacePath. Convert that into a list...
        if package_path is not None and not isinstance(package_path, list):
            package_path = list(package_path)
        try:
            fp, pathname, (ext,mode,ty) = imp.find_module(fullname,package_path)
            if fp: fp.close()  # Python should offer a Default-Loader to avoid this double find/open!
            if pathname and ty == imp.PKG_DIRECTORY:
                pkg_file = os.path.join(pathname, '__init__'+self.extension)
                if os.path.isfile(pkg_file):
                    return PyxLoader(fullname, pathname,
                        init_path=pkg_file,
                        pyxbuild_dir=self.pyxbuild_dir,
                        inplace=self.inplace,
                        language_level=self.language_level)
            if pathname and pathname.endswith(self.extension):
                return PyxLoader(fullname, pathname,
                                 pyxbuild_dir=self.pyxbuild_dir,
                                 inplace=self.inplace,
                                 language_level=self.language_level)
            if ty != imp.C_EXTENSION:  # only when an extension, check if we have a .pyx next!
                return None

            # find .pyx fast, when .so/.pyd exist --inplace
            pyxpath = os.path.splitext(pathname)[0]+self.extension
            if os.path.isfile(pyxpath):
                return PyxLoader(fullname, pyxpath,
                                 pyxbuild_dir=self.pyxbuild_dir,
                                 inplace=self.inplace,
                                 language_level=self.language_level)

            # .so/.pyd's on PATH should not be remote from .pyx's
            # think no need to implement PyxArgs.importer_search_remote here?

        except ImportError:
            pass

        # searching sys.path ...

        #if DEBUG_IMPORT:  print "SEARCHING", fullname, package_path

        mod_parts = fullname.split('.')
        module_name = mod_parts[-1]
        pyx_module_name = module_name + self.extension

        # this may work, but it returns the file content, not its path
        #import pkgutil
        #pyx_source = pkgutil.get_data(package, pyx_module_name)

        paths = package_path or sys.path
        for path in paths:
            pyx_data = None
            if not path:
                path = os.getcwd()
            elif os.path.isfile(path):
                try:
                    zi = zipimporter(path)
                    pyx_data = zi.get_data(pyx_module_name)
                except (ZipImportError, IOError, OSError):
                    continue  # Module not found.
                # unzip the imported file into the build dir
                # FIXME: can interfere with later imports if build dir is in sys.path and comes before zip file
                path = self.pyxbuild_dir
            elif not os.path.isabs(path):
                path = os.path.abspath(path)

            pyx_module_path = os.path.join(path, pyx_module_name)
            if pyx_data is not None:
                if not os.path.exists(path):
                    try:
                        os.makedirs(path)
                    except OSError:
                        # concurrency issue?
                        if not os.path.exists(path):
                            raise
                with open(pyx_module_path, "wb") as f:
                    f.write(pyx_data)
            elif not os.path.isfile(pyx_module_path):
                continue  # Module not found.

            return PyxLoader(fullname, pyx_module_path,
                             pyxbuild_dir=self.pyxbuild_dir,
                             inplace=self.inplace,
                             language_level=self.language_level)

        # not found, normal package, not a .pyx file, none of our business
        _debug("%s not found" % fullname)
        return None


class PyImporter(PyxImporter):
    """A meta-path importer for normal .py files.
    """
    def __init__(self, pyxbuild_dir=None, inplace=False, language_level=None):
        if language_level is None:
            language_level = sys.version_info[0]
        self.super = super(PyImporter, self)
        self.super.__init__(extension=PY_EXT, pyxbuild_dir=pyxbuild_dir, inplace=inplace,
                            language_level=language_level)
        self.uncompilable_modules = {}
        self.blocked_modules = ['Cython', 'pyxbuild', 'pyximport.pyxbuild',
                                'distutils']
        self.blocked_packages = ['Cython.', 'distutils.']

    def find_module(self, fullname, package_path=None):
        if fullname in sys.modules:
            return None
        if any([fullname.startswith(pkg) for pkg in self.blocked_packages]):
            return None
        if fullname in self.blocked_modules:
            # prevent infinite recursion
            return None
        if _lib_loader.knows(fullname):
            return _lib_loader
        _debug("trying import of module '%s'", fullname)
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
                if importer.init_path:
                    path = importer.init_path
                    real_name = fullname + '.__init__'
                else:
                    path = importer.path
                    real_name = fullname
                _debug("importer found path %s for module %s", path, real_name)
                try:
                    so_path = build_module(
                        real_name, path,
                        pyxbuild_dir=self.pyxbuild_dir,
                        language_level=self.language_level,
                        inplace=self.inplace)
                    _lib_loader.add_lib(fullname, path, so_path,
                                        is_package=bool(importer.init_path))
                    return _lib_loader
                except Exception:
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


class LibLoader(object):
    def __init__(self):
        self._libs = {}

    def load_module(self, fullname):
        try:
            source_path, so_path, is_package = self._libs[fullname]
        except KeyError:
            raise ValueError("invalid module %s" % fullname)
        _debug("Loading shared library module '%s' from %s", fullname, so_path)
        return load_module(fullname, source_path, so_path=so_path, is_package=is_package)

    def add_lib(self, fullname, path, so_path, is_package):
        self._libs[fullname] = (path, so_path, is_package)

    def knows(self, fullname):
        return fullname in self._libs

_lib_loader = LibLoader()


class PyxLoader(object):
    def __init__(self, fullname, path, init_path=None, pyxbuild_dir=None,
                 inplace=False, language_level=None):
        _debug("PyxLoader created for loading %s from %s (init path: %s)",
               fullname, path, init_path)
        self.fullname = fullname
        self.path, self.init_path = path, init_path
        self.pyxbuild_dir = pyxbuild_dir
        self.inplace = inplace
        self.language_level = language_level

    def load_module(self, fullname):
        assert self.fullname == fullname, (
            "invalid module, expected %s, got %s" % (
            self.fullname, fullname))
        if self.init_path:
            # package
            #print "PACKAGE", fullname
            module = load_module(fullname, self.init_path,
                                 self.pyxbuild_dir, is_package=True,
                                 build_inplace=self.inplace,
                                 language_level=self.language_level)
            module.__path__ = [self.path]
        else:
            #print "MODULE", fullname
            module = load_module(fullname, self.path,
                                 self.pyxbuild_dir,
                                 build_inplace=self.inplace,
                                 language_level=self.language_level)
        return module
