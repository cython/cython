import shutil
import os
import tempfile

import Cython.Build.Dependencies
import Cython.Utils
from Cython.TestUtils import CythonTest



SAME = "The result of cytonization is the same"
INCORRECT = "Incorrect cythonization"
LINE_1 = '  /* "{name}{ext}":1\n'
VARS_LINE = '  /*--- Wrapped vars code ---*/\n'


class TestRecythonize(CythonTest):
    language_level = 3
    dep_tree = Cython.Build.Dependencies.create_dependency_tree()

    def сlear_function_and_Dependencies_caches(self):
        Cython.Utils.clear_function_caches()
        Cython.Build.Dependencies._dep_tree = None  # discard method caches

    def setUp(self):
        CythonTest.setUp(self)
        self.сlear_function_and_Dependencies_caches()
        self.temp_dir = (
            tempfile.mkdtemp(
                prefix='recythonize-test',
                dir='TEST_TMP' if os.path.isdir('TEST_TMP') else None
            )
        )
        self.src_dir = tempfile.mkdtemp(prefix='src', dir=self.temp_dir)

    def tearDown(self):
        CythonTest.tearDown(self)
        self.сlear_function_and_Dependencies_caches()
        shutil.rmtree(self.temp_dir)

    def fresh_cythonize(self, *args, **kwargs):
        self.сlear_function_and_Dependencies_caches()
        kwargs.update(language_level=self.language_level)
        Cython.Build.Dependencies.cythonize(*args, **kwargs)

    def refresh_dep_tree(self):
        Cython.Utils.clear_function_caches()
        Cython.Utils.clear_method_caches(self.dep_tree)
        self.dep_tree._transitive_cache.clear()

    def fresh_all_dependencies(self, *args, **kwargs):
        self.refresh_dep_tree()
        return self.dep_tree.all_dependencies(*args, **kwargs)

    def relative_lines(self, lines, line, start, end):
        try:
            ind = lines.index(line)
            return lines[ind+start: ind+end]
        except ValueError:
            # XXX: It is assumed that VARS_LINE is always present.
            ind = lines.index(VARS_LINE)
            raise ValueError(
                "{0!r} was not found, presumably in {1}".format(
                    line, lines[ind-10: ind-1]))
        except Exception as e:
            raise e

    def relative_lines_from_file(self, path, line, start, end):
        with open(path) as f:
            lines = f.readlines()

        return self.relative_lines(lines, line, start, end)

    def recythonize_on_pxd_change(self, ext, pxd_exists_for_first_check):
        a_pxd = os.path.join(self.src_dir, 'a.pxd')  # will be changed
        a_source = os.path.join(self.src_dir, 'a' + ext)
        a_c = os.path.join(self.src_dir, 'a.c')  # change check

        a_line_1 = LINE_1.format(name="a", ext=ext)

        if pxd_exists_for_first_check:
            with open(a_pxd, 'w') as f:
                f.write('cdef int x\n')

        with open(a_source, 'w') as f:
            f.write('x = 1\n')

        dependencies = self.fresh_all_dependencies(a_source)
        self.assertIn(a_source, dependencies)
        if pxd_exists_for_first_check:
            self.assertIn(a_pxd, dependencies)
            self.assertEqual(2, len(dependencies))
        else:
            self.assertEqual(1, len(dependencies))

        # Create a.c
        self.fresh_cythonize(a_source)

        definition_before = "".join(
            self.relative_lines_from_file(a_c, a_line_1, 0, 7))

        if pxd_exists_for_first_check:
            self.assertIn("a_x = 1;", definition_before, INCORRECT)
        else:
            self.assertNotIn("a_x = 1;", definition_before, INCORRECT)

        with open(a_pxd, 'w') as f:
            f.write('cdef float x\n')

        # otherwise nothing changes since there are no new files
        if not pxd_exists_for_first_check:
            dependencies = self.fresh_all_dependencies(a_source)
            self.assertIn(a_source, dependencies)
            self.assertIn(a_pxd, dependencies)
            self.assertEqual(2, len(dependencies))

        # Change a.c
        self.fresh_cythonize(a_source)

        definition_after = "".join(
            self.relative_lines_from_file(a_c, a_line_1, 0, 7))

        self.assertNotIn("a_x = 1;", definition_after, SAME)
        self.assertIn("a_x = 1.0;", definition_after, INCORRECT)

    # pxd_exists_for_first_check is not used because cimport requires pxd
    # to import another script.
    def recythonize_on_dep_pxd_change(self, ext_a, ext_b):
        a_pxd = os.path.join(self.src_dir, 'a.pxd')  # will be changed
        a_source = os.path.join(self.src_dir, 'a' + ext_a)  # dependency
        a_c = os.path.join(self.src_dir, 'a.c')  # change check
        b_pxd = os.path.join(self.src_dir, 'b.pxd')  # for cimport
        b_source = os.path.join(self.src_dir, 'b' + ext_b)  # reason for change
        b_c = os.path.join(self.src_dir, 'b.c')  # change check

        a_line_1 = LINE_1.format(name="a", ext=ext_a)
        b_line_1 = LINE_1.format(name="b", ext=ext_b)

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

        a_definition_before = "".join(
            self.relative_lines_from_file(a_c, a_line_1, 0, 7))

        b_definition_before = "".join(
            self.relative_lines_from_file(b_c, b_line_1, 0, 7))

        self.assertIn("a_x = 1;", a_definition_before, INCORRECT)
        self.assertIn("a_x = 2;", b_definition_before, INCORRECT)

        with open(a_pxd, 'w') as f:
            f.write('cdef float x\n')

        # Change a.c and b.c
        self.fresh_cythonize([a_source, b_source])

        a_definition_after = "".join(
            self.relative_lines_from_file(a_c, a_line_1, 0, 7))

        b_definition_after = "".join(
            self.relative_lines_from_file(b_c, b_line_1, 0, 7))

        self.assertNotIn("a_x = 1;", a_definition_after, SAME)
        self.assertNotIn("a_x = 2;", b_definition_after, SAME)
        self.assertIn("a_x = 1.0;", a_definition_after, INCORRECT)
        self.assertIn("a_x = 2.0;", b_definition_after, INCORRECT)

    def test_recythonize_py_on_pxd_change(self):
        self.recythonize_on_pxd_change(".py", pxd_exists_for_first_check=True)

    def test_recythonize_pyx_on_pxd_change(self):
        self.recythonize_on_pxd_change(".pyx", pxd_exists_for_first_check=True)

    def test_recythonize_py_on_pxd_creating(self):
        self.recythonize_on_pxd_change(".py", pxd_exists_for_first_check=False)

    def test_recythonize_pyx_on_pxd_creating(self):
        self.recythonize_on_pxd_change(".pyx", pxd_exists_for_first_check=False)

    def test_recythonize_py_py_on_dep_pxd_change(self):
        self.recythonize_on_dep_pxd_change(".py", ".py")

    def test_recythonize_py_pyx_on_dep_pxd_change(self):
        self.recythonize_on_dep_pxd_change(".py", ".pyx")

    def test_recythonize_pyx_py_on_dep_pxd_change(self):
        self.recythonize_on_dep_pxd_change(".pyx", ".py")

    def test_recythonize_pyx_pyx_on_dep_pxd_change(self):
        self.recythonize_on_dep_pxd_change(".pyx", ".pyx")

