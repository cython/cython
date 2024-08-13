# Note - setuptools imports are all lazy so that we can specify it as a dependency
from contextlib import contextmanager as _contextmanager
from functools import lru_cache
from pathlib import Path as _Path

def _prepare_ext_module(module_settings):
    from setuptools import Extension as _Extension
    name = module_settings['name']
    sources = module_settings['sources']
    
    # TODO - everything else:
    #  include_dirs, libraries, library_dirs, extra_*_args,
    #  py_limited_api, etc., etc.
    #  probably handle numpy/pythran/etc includes somehow?

    return _Extension(name, sources)

@lru_cache  # incase we go through multiple calls to this function
def _prepare_ext_modules() -> list:
    from setuptools.config.pyprojecttoml import load_file
    from Cython.Build.Dependencies import cythonize

    config_toml_path = (_Path.cwd().resolve() / 'pyproject.toml')
    config_toml = load_file(config_toml_path)
    print("AAAAA", config_toml)
    cython_settings = config_toml['tool']['cython']
    module_list = cython_settings['module_list']

    # either accept a string pattern, or a list
    if isinstance(module_list, str):
        pass  # pass straight to cythonize
    elif isinstance(module_list, list):
        module_list = [_prepare_ext_module(m) for m in module_list]
    else:
        raise TypeError("'module_list' must be a string or list")

    # TODO - extra arguments to cythonize:
    #  compiler_directives
    #  Cython.Options
    #  etc.

    return cythonize(
        module_list=module_list,
    )

@_contextmanager
def _patch_setup():
    import setuptools
    ext_modules = _prepare_ext_modules()
    old_setup = setuptools.setup
    def new_setup(**attrs):
        old_ext_modules = attrs.get("ext_modules", [])
        new_ext_modules = old_ext_modules + ext_modules
        attrs["ext_modules"] = new_ext_modules
        return old_setup(**attrs)
    setuptools.setup = new_setup
    try:
        yield
    finally:
        setuptools.setup = old_setup

def get_requires_for_build_wheel(config_settings=None):
    # specifying setuptools in the requires does mean we can't use setuptools to
    # get_requires.... That's more of an issue if the user provides a setup.py file
    # since setuptools can get requirements from that.
    return [
        "setuptools >= 38.2.5",
        "wheel"  # not really necessary for modern setuptools (>=70.0.1), 
                 # but I don't think I can specify that detail.
    ]

def get_requires_for_build_sdist(config_settings=None):
    return ["setuptools >= 38.2.5"]

def get_requires_for_build_editable(config_settings=None):
    return ["setuptools >= 63.0.0"]

def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    from setuptools.build_meta import prepare_metadata_for_build_wheel
    with _patch_setup():
        return prepare_metadata_for_build_wheel(
            metadata_directory,
            config_settings=config_settings
        )
    
def prepare_metadata_for_build_editable(metadata_directory, config_settings=None):
    from setuptools.build_meta import prepare_metadata_for_build_editable
    with _patch_setup():
        return prepare_metadata_for_build_editable(
            metadata_directory,
            config_settings=config_settings
        )

def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    from setuptools.build_meta import build_wheel
    with _patch_setup():
        return build_wheel(
            wheel_directory,
            config_settings=config_settings,
            metadata_directory=metadata_directory
        )
    
def build_sdist(sdist_directory, config_settings=None):
    from setuptools.build_meta import build_sdist
    with _patch_setup():
        return build_sdist(
            sdist_directory,
            config_settings=config_settings
        )

def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    from setuptools.build_meta import build_editable
    with _patch_setup():
        return build_editable(
            wheel_directory,
            config_settings=config_settings,
            metadata_directory=metadata_directory
        )
        
