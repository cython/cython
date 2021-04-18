import shutil
import os
import tempfile

import Cython.Build.Dependencies
import Cython.Utils
from Cython.TestUtils import CythonTest


def fresh_cythonize(*args, **kwargs):
    Cython.Utils.clear_function_caches()
    Cython.Build.Dependencies._dep_tree = None  # discard method caches
    Cython.Build.Dependencies.cythonize(*args, **kwargs)

class TestRecythonize(CythonTest):

    def setUp(self):
        CythonTest.setUp(self)

    def test_recythonize_pyx_on_pxd_change(self):
        temp_dir = (
            tempfile.mkdtemp(
                prefix='recythonize-test',
                dir='TEST_TMP' if os.path.isdir('TEST_TMP') else None
            )
        )
        try:
            src_dir = tempfile.mkdtemp(prefix='src', dir=temp_dir)

            content1 = 'value = 1\n'
            a_pxd = os.path.join(src_dir, 'a.pxd')
            a_pyx = os.path.join(src_dir, 'a.pyx')
            a_c = os.path.join(src_dir, 'a.c')
            dep_tree = Cython.Build.Dependencies.create_dependency_tree()

            with open(a_pxd, 'w') as f:
                f.write('cdef int value\n')

            with open(a_pyx, 'w') as f:
                f.write('value = 1\n')


            # The number of dependencies should be 2: "a.pxd" and "a.pyx"
            self.assertEqual(2, len(dep_tree.all_dependencies(a_pyx)))

            # Cythonize to create a.c
            fresh_cythonize(a_pyx)

            with open(a_c) as f:
                a_c_contents1 = f.read()

            with open(a_pxd, 'w') as f:
                f.write('cdef double value\n')

            fresh_cythonize(a_pyx)

            with open(a_c) as f:
                a_c_contents2 = f.read()


            self.assertNotEqual(a_c_contents1, a_c_contents2, 'C file not changed!')
        finally:
            shutil.rmtree(temp_dir)


    def test_recythonize_py_on_pxd_change(self):
        temp_dir = (
            tempfile.mkdtemp(
                prefix='recythonize-test',
                dir='TEST_TMP' if os.path.isdir('TEST_TMP') else None
            )
        )
        try:
            src_dir = tempfile.mkdtemp(prefix='src', dir=temp_dir)

            content1 = 'value = 1\n'
            a_pxd = os.path.join(src_dir, 'a.pxd')
            a_py = os.path.join(src_dir, 'a.py')
            a_c = os.path.join(src_dir, 'a.c')
            dep_tree = Cython.Build.Dependencies.create_dependency_tree()

            with open(a_pxd, 'w') as f:
                f.write('cdef int value\n')

            with open(a_py, 'w') as f:
                f.write('value = 1\n')


            # The number of dependencies should be 2: "a.pxd" and "a.pyx"
            self.assertEqual(2, len(dep_tree.all_dependencies(a_py)))

            # Cythonize to create a.c
            fresh_cythonize(a_py)

            with open(a_c) as f:
                a_c_contents1 = f.read()

            with open(a_pxd, 'w') as f:
                f.write('cdef double value\n')

            fresh_cythonize(a_py)

            with open(a_c) as f:
                a_c_contents2 = f.read()


            self.assertNotEqual(a_c_contents1, a_c_contents2, 'C file not changed!')
        finally:
            shutil.rmtree(temp_dir)
