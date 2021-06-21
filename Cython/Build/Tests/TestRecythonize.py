import shutil
import os
import tempfile

import Cython.Build.Dependencies
import Cython.Utils
from Cython.TestUtils import CythonTest


SAME = "The result of cytonization is the same: "
INCOR = "Incorrect cythonization: "


# assertIn and assertNotIn are not used to validate the generated code
# as a failure causes an unreadable mess
class TestRecythonize(CythonTest):

    def setUp(self):
        CythonTest.setUp(self)
        self.temp_dir = (
            tempfile.mkdtemp(
                prefix='recythonize-test',
                dir='TEST_TMP' if os.path.isdir('TEST_TMP') else None
            )
        )
        self.src_dir = tempfile.mkdtemp(prefix='src', dir=self.temp_dir)
        self.dep_tree = Cython.Build.Dependencies.create_dependency_tree()
        self.language_level = 3

    def tearDown(self):
        CythonTest.tearDown(self)
        shutil.rmtree(self.temp_dir)

    def fresh_cythonize(self, *args, **kwargs):
        Cython.Utils.clear_function_caches()
        Cython.Build.Dependencies._dep_tree = None  # discard method caches
        kwargs.update(language_level=self.language_level)
        Cython.Build.Dependencies.cythonize(*args, **kwargs)

    def refresh_dep_tree(self):
        Cython.Utils.clear_function_caches()
        Cython.Utils.clear_method_caches(self.dep_tree)
        self.dep_tree._transitive_cache.clear()

    def fresh_all_dependencies(self, *args, **kwargs):
        self.refresh_dep_tree()
        return self.dep_tree.all_dependencies(*args, **kwargs)

    def recythonize_on_pxd_change(self, ext, creating_pxd):
        a_pxd = os.path.join(self.src_dir, 'a.pxd')  # will be changed
        a_source = os.path.join(self.src_dir, 'a' + ext)
        a_c = os.path.join(self.src_dir, 'a.c')  # change check

        if not creating_pxd:
            with open(a_pxd, 'w') as f:
                f.write('cdef int x\n')

        with open(a_source, 'w') as f:
            f.write('x = 1\n')

        dependencies = self.fresh_all_dependencies(a_source)
        self.assertIn(a_source, dependencies)
        if creating_pxd:
            self.assertEqual(1, len(dependencies))
        else:
            self.assertIn(a_pxd, dependencies)
            self.assertEqual(2, len(dependencies))

        # Create a.c
        self.fresh_cythonize(a_source)

        with open(a_c) as f:
            a_c_before = f.read()

        if creating_pxd:
            self.assertTrue("a_x = 1;" not in a_c_before, INCOR)
        else:
            self.assertTrue("a_x = 1;" in a_c_before, INCOR)

        with open(a_pxd, 'w') as f:
            f.write('cdef float x\n')

        if creating_pxd:
            dependencies = self.fresh_all_dependencies(a_source)
            self.assertIn(a_source, dependencies)
            self.assertIn(a_pxd, dependencies)
            self.assertEqual(2, len(dependencies))

        # Change a.c
        self.fresh_cythonize(a_source)

        with open(a_c) as f:
            a_c_after = f.read()

        self.assertTrue("a_x = 1;" not in a_c_after, SAME)
        self.assertTrue("a_x = 1.0;" in a_c_after, INCOR)

    # creating_pxd is not used because cimport requires pxd
    # to import another script.
    def recythonize_on_dep_pxd_change(self, ext_a, ext_b):
        a_pxd = os.path.join(self.src_dir, 'a.pxd')  # will be changed
        a_source = os.path.join(self.src_dir, 'a' + ext_a)  # dependency
        a_c = os.path.join(self.src_dir, 'a.c')  # change check
        b_pxd = os.path.join(self.src_dir, 'b.pxd')  # for cimport
        b_source = os.path.join(self.src_dir, 'b' + ext_b)  # reason for change
        b_c = os.path.join(self.src_dir, 'b.c')  # change check

        with open(a_pxd, 'w') as f:
            f.write('cdef int x\n')

        with open(a_source, 'w') as f:
            f.write('x = 1\n')

        with open(b_pxd, 'w') as f:
            f.write('cimport a\n')

        with open(b_source, 'w') as f:
            f.write('a.x = 2\n')

        dependencies = self.fresh_all_dependencies(b_source)
        self.assertIn(b_pxd, dependencies)
        self.assertIn(b_source, dependencies)
        self.assertIn(a_pxd, dependencies)
        self.assertEqual(3, len(dependencies))

        # Create a.c and b.c
        self.fresh_cythonize([a_source, b_source])

        with open(a_c) as f:
            a_c_before = f.read()

        with open(b_c) as f:
            b_c_before = f.read()

        self.assertTrue("a_x = 1;" in a_c_before, INCOR)
        self.assertTrue("a_x = 2;" in b_c_before, INCOR)

        with open(a_pxd, 'w') as f:
            f.write('cdef float x\n')

        # Change a.c and b.c
        self.fresh_cythonize([a_source, b_source])

        with open(a_c) as f:
            a_c_after = f.read()

        with open(b_c) as f:
            b_c_after = f.read()

        self.assertTrue("a_x = 1;" not in a_c_after, SAME)
        self.assertTrue("a_x = 2;" not in b_c_after, SAME)
        self.assertTrue("a_x = 1.0;" in a_c_after, INCOR)
        self.assertTrue("a_x = 2.0;" in b_c_after,INCOR)

    def test_recythonize_py_on_pxd_change(self):
        self.recythonize_on_pxd_change(".py", False)

    def test_recythonize_pyx_on_pxd_change(self):
        self.recythonize_on_pxd_change(".pyx", False)

    def test_recythonize_py_on_pxd_creating(self):
        self.recythonize_on_pxd_change(".py", True)

    def test_recythonize_pyx_on_pxd_creating(self):
        self.recythonize_on_pxd_change(".pyx", True)

    def test_recythonize_py_py_on_dep_pxd_change(self):
        self.recythonize_on_dep_pxd_change(".py", ".py")

    def test_recythonize_py_pyx_on_dep_pxd_change(self):
        self.recythonize_on_dep_pxd_change(".py", ".pyx")

    def test_recythonize_pyx_py_on_dep_pxd_change(self):
        self.recythonize_on_dep_pxd_change(".pyx", ".py")

    def test_recythonize_pyx_pyx_on_dep_pxd_change(self):
        self.recythonize_on_dep_pxd_change(".pyx", ".pyx")
