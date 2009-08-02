from distutils.errors import DistutilsFileError
from Cython.Distutils import build_ext as cy_build_ext
from numpy.distutils.command.build_ext import build_ext as np_build_ext
from numpy.distutils.extension import Extension as np_extension
from numpy.distutils.core import setup
import os


class FwrapExtension(np_extension):
    def __init__ (self, name, sources,
                  include_dirs=None,
                  define_macros=None,
                  undef_macros=None,
                  library_dirs=None,
                  libraries=None,
                  runtime_library_dirs=None,
                  extra_objects=None,
                  extra_compile_args=None,
                  extra_link_args=None,
                  export_symbols=None,
                  swig_opts=None,
                  depends=None,
                  language=None,
                  f2py_options=None,
                  module_dirs=None,
                  pyrex_include_dirs = None,
                  pyrex_create_listing = 0,
                  pyrex_cplus = 0,
                  pyrex_c_in_temp = 0,
                  pyrex_gen_pxi = 0,
                  fwrap_config_sources=None,
                  fwrap_cython_sources = None,
                  **kw):

        np_extension.__init__(self, name, sources,
                  include_dirs,
                  define_macros,
                  undef_macros,
                  library_dirs,
                  libraries,
                  runtime_library_dirs,
                  extra_objects,
                  extra_compile_args,
                  extra_link_args,
                  export_symbols,
                  swig_opts,
                  depends,
                  language,
                  f2py_options,
                  module_dirs,
                  )

        self.pyrex_include_dirs = pyrex_include_dirs or []
        self.pyrex_create_listing = pyrex_create_listing
        self.pyrex_cplus = pyrex_cplus
        self.pyrex_c_in_temp = pyrex_c_in_temp
        self.pyrex_gen_pxi = pyrex_gen_pxi

        self.fwrap_config_sources = fwrap_config_sources or []
        if len(fwrap_config_sources) != 1:
            raise DistutilsFileError("Only one fortran configuration file allowed.")
        self.fwrap_cython_sources = fwrap_cython_sources or []



class fwrap_build_ext(np_build_ext, cy_build_ext):

    def initialize_options(self):
        np_build_ext.initialize_options(self)
        self.pyrex_cplus = 0
        self.pyrex_create_listing = 0
        self.pyrex_include_dirs = None
        self.pyrex_c_in_temp = 0
        self.pyrex_gen_pxi = 0

    def finalize_options (self):
        np_build_ext.finalize_options(self)
        if self.pyrex_include_dirs is None:
            self.pyrex_include_dirs = []
        elif type(self.pyrex_include_dirs) is StringType:
            self.pyrex_include_dirs = \
                self.pyrex_include_dirs.split(os.pathsep)
 
    def init_compilers(self):

        from distutils.ccompiler import new_compiler
        from numpy.distutils.fcompiler import new_fcompiler

        compiler_type = self.compiler
        # Initialize C compiler:
        self.compiler = new_compiler(compiler=compiler_type,
                                     verbose=self.verbose,
                                     dry_run=self.dry_run,
                                     force=self.force)
        self.compiler.customize(self.distribution)
        self.compiler.customize_cmd(self)
        self.compiler.show_customization()

        # Initialize Fortran compiler:
        ctype = self.fcompiler
        self._f90_compiler = new_fcompiler(compiler=self.fcompiler,
                                           verbose=self.verbose,
                                           dry_run=self.dry_run,
                                           force=self.force,
                                           requiref90=True,
                                           c_compiler = self.compiler)
        fcompiler = self._f90_compiler
        if fcompiler:
            ctype = fcompiler.compiler_type
            fcompiler.customize(self.distribution)
        if fcompiler and fcompiler.get_version():
            fcompiler.customize_cmd(self)
            fcompiler.show_customization()
        else:
            self.warn('f90_compiler=%s is not available.' %
                      (ctype))
            self._f90_compiler = None

        # don't need cxx compiler.
        self._cxx_compiler = None

    def run(self):

        self.init_compilers()
        fcompiler = self._f90_compiler

        for ext in self.extensions:

            fullname = self.get_ext_fullname(ext.name)

            module_dirs = ext.module_dirs[:]
            module_build_dir = os.path.join(
                self.build_temp,os.path.dirname(
                    self.get_ext_filename(fullname)))

            extra_postargs = fcompiler.module_options(
                module_dirs,module_build_dir)

            # generate fortran config files.
            assert len(ext.fwrap_config_sources) == 1
            config_source, config_result = ext.fwrap_config_sources[0]
            exname = os.path.splitext(config_source)[0]

            onames = fcompiler.compile([config_source],
                            output_dir=self.build_temp,
                            extra_postargs=extra_postargs)
            print fcompiler.link_executable(onames,
                    exname,
                    output_dir=self.build_temp,
                    extra_postargs=extra_postargs)
            # TODO: untested on windows, may not work.
            fcompiler.spawn([os.path.join(self.build_temp,exname)])

            c_sources = cy_build_ext.cython_sources(self, ext.fwrap_cython_sources, ext)
            ext.sources = c_sources + [config_result] + ext.sources
            print ext.sources
            np_build_ext.build_extension(self, ext)
