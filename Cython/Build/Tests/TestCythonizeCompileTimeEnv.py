import os
import shutil
import tempfile

import Cython.Build.Dependencies
import Cython.Utils
from Cython.TestUtils import CythonTest


def fresh_cythonize(*args, **kwargs):
    Cython.Utils.clear_function_caches()
    Cython.Build.Dependencies._dep_tree = None  # discard method caches
    return Cython.Build.Dependencies.cythonize(*args, **kwargs)


class TestCythonizeCompileTimeEnv(CythonTest):
    # Regression tests for https://github.com/cython/cython/issues/1572
    # Setting "cython_compile_time_env" on an Extension used to be ignored
    # when cythonize() was called directly (it only worked through the
    # distutils build_ext, which passes the value in as a global option).

    def setUp(self):
        CythonTest.setUp(self)
        self.temp_dir = tempfile.mkdtemp(prefix='cythonize-env-test')
        self.addCleanup(shutil.rmtree, self.temp_dir, True)

    def write_module(self, name):
        pyx_path = os.path.join(self.temp_dir, name + '.pyx')
        with open(pyx_path, 'w') as f:
            f.write('DEF RESULT = TEST_ENV * 2\n')
            f.write('value = RESULT\n')
        return pyx_path

    def compiled_value(self, name):
        with open(os.path.join(self.temp_dir, name + '.c')) as f:
            return f.read()

    def make_extension(self, name, pyx_path, env=None):
        from Cython.Distutils import Extension
        return Extension(name, sources=[pyx_path], cython_compile_time_env=env)

    def test_per_extension_env_is_used(self):
        pyx_path = self.write_module('mod_a')
        ext = self.make_extension('mod_a', pyx_path, env={'TEST_ENV': 123})

        fresh_cythonize([ext], quiet=True, force=True)

        # TEST_ENV * 2 == 246 ends up as a constant in the generated code.
        self.assertIn('__pyx_int_246', self.compiled_value('mod_a'))

    def test_per_extension_env_overrides_global(self):
        # Two modules in one cythonize() call: the first has its own env,
        # the second falls back to the global one.
        pyx_a = self.write_module('mod_a')
        pyx_b = self.write_module('mod_b')
        ext_a = self.make_extension('mod_a', pyx_a, env={'TEST_ENV': 123})
        ext_b = self.make_extension('mod_b', pyx_b)

        fresh_cythonize(
            [ext_a, ext_b],
            compile_time_env={'TEST_ENV': 1000},
            quiet=True,
            force=True,
        )

        self.assertIn('__pyx_int_246', self.compiled_value('mod_a'))
        self.assertIn('__pyx_int_2000', self.compiled_value('mod_b'))
