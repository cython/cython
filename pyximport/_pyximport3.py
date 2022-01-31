from __future__ import absolute_import
import os.path
import sys
from importlib.abc import MetaPathFinder
from importlib.machinery import ExtensionFileLoader
from importlib.util import spec_from_file_location
from pyximport.common import build_module, PYX_EXT, PY_EXT


class PyxImportMetaFinder(MetaPathFinder):

    def __init__(self, extension=PYX_EXT, pyxbuild_dir=None, inplace=False, language_level=None):
        self.pyxbuild_dir = pyxbuild_dir
        self.inplace = inplace
        self.language_level = language_level
        self.extension = extension

    def find_spec(self, fullname, path, target=None):
        if path is None or path == "":
            path = [os.getcwd()]  # top level import --
        if "." in fullname:
            *parents, name = fullname.split(".")
        else:
            name = fullname
        for entry in path:
            if os.path.isdir(os.path.join(entry, name)):
                # this module has child modules
                filename = os.path.join(entry, name, "__init__.py")     # FIXME: __init__.pyx ?
                submodule_locations = [os.path.join(entry, name)]
            else:
                filename = os.path.join(entry, name + self.extension)
                submodule_locations = None
            if not os.path.exists(filename):
                continue

            return spec_from_file_location(
                fullname, filename,
                loader=PyxImportLoader(filename, self.pyxbuild_dir, self.inplace, self.language_level),
                submodule_search_locations=submodule_locations)

        return None  # we don't know how to import this


class PyImportMetaFinder(MetaPathFinder):

    def __init__(self, extension=PY_EXT, pyxbuild_dir=None, inplace=False, language_level=None):
        self.pyxbuild_dir = pyxbuild_dir
        self.inplace = inplace
        self.language_level = language_level
        self.extension = extension
        self.uncompilable_modules = {}
        self.blocked_modules = ['Cython', 'pyxbuild', 'pyximport.pyxbuild',
                                'distutils', 'cython']
        self.blocked_packages = ['Cython.', 'distutils.']

    def find_spec(self, fullname, path, target=None):
        if fullname in sys.modules:
            return None
        if any([fullname.startswith(pkg) for pkg in self.blocked_packages]):
            return None
        if fullname in self.blocked_modules:
            # prevent infinite recursion
            return None

        self.blocked_modules.append(fullname)
        name = fullname
        if path is None or path == "":
            path = [os.getcwd()]  # top level import --
        try:
            for entry in path:
                if os.path.isdir(os.path.join(entry, name)):
                    # this module has child modules
                    filename = os.path.join(entry, name, "__init__.py")
                    submodule_locations = [os.path.join(entry, name)]
                else:
                    filename = os.path.join(entry, name + PY_EXT)
                    submodule_locations = None
                if not os.path.exists(filename):
                    continue

                return spec_from_file_location(
                    fullname, filename,
                    loader=PyxImportLoader(filename, self.pyxbuild_dir, self.inplace, self.language_level),
                    submodule_search_locations=submodule_locations)
        finally:
            self.blocked_modules.pop()

        return None  # we don't know how to import this


class PyxImportLoader(ExtensionFileLoader):

    def __init__(self, filename, pyxbuild_dir, inplace, language_level):
        module_name = os.path.splitext(os.path.basename(filename))[0]
        super().__init__(module_name, filename)
        self._pyxbuild_dir = pyxbuild_dir
        self._inplace = inplace
        self._language_level = language_level

    def create_module(self, spec):
        so_path = build_module(spec.name, pyxfilename=spec.origin, pyxbuild_dir=self._pyxbuild_dir,
                               inplace=self._inplace, language_level=self._language_level)
        self.path = so_path
        spec.origin = so_path
        return super().create_module(spec)

    def exec_module(self, module):
        return super().exec_module(module)
