import os
import shutil
import tempfile
import time

import Cython.Build.Dependencies
import Cython.Utils
from Cython.TestUtils import (CythonTest, clear_function_and_Dependencies_caches,
                              fresh_cythonize, write_file, write_newer_file)

SAME = "The result of cytonization is the same"
INCORRECT = "Incorrect cythonization"
LINE_BEFORE_IMPLEMENTATION = '  /* "{filename}":{at_line}\n'
VARS_LINE = '  /*--- Wrapped vars code ---*/\n'


class TestRecythonize(CythonTest):
    language_level = 3
    dep_tree = Cython.Build.Dependencies.create_dependency_tree()

    def setUp(self):
        CythonTest.setUp(self)
        clear_function_and_Dependencies_caches()
        self.temp_dir = (
            tempfile.mkdtemp(
                prefix='recythonize-test',
                dir='TEST_TMP' if os.path.isdir('TEST_TMP') else None
            )
        )
        self.src_dir = os.path.join(self.temp_dir, 'src')
        os.mkdir(self.src_dir)

    def tearDown(self):
        CythonTest.tearDown(self)
        clear_function_and_Dependencies_caches()
        shutil.rmtree(self.temp_dir)

    def fresh_cythonize(self, *args, **kwargs):
        kwargs.update(language_level=self.language_level)
        fresh_cythonize(*args, **kwargs)

    def refresh_dep_tree(self):
        Cython.Utils.clear_function_caches()
        Cython.Utils.clear_method_caches(self.dep_tree)
        self.dep_tree._transitive_cache.clear()

    def fresh_all_dependencies(self, *args, **kwargs):
        self.refresh_dep_tree()
        return self.dep_tree.all_dependencies(*args, **kwargs)

    def relative_lines_from_file(self, path, line, start, end):
        with open(path) as f:
            lines = f.readlines()

        try:
            ind = lines.index(line)
            return "".join(lines[ind+start: ind+end])
        except ValueError:
            # XXX: It is assumed that VARS_LINE is always present.
            ind = lines.index(VARS_LINE)
            raise ValueError(
                "{0!r} was not found, presumably in \n{1}".format(
                    line, "\n".join(map(repr, lines[ind-10: ind-1]))))

    def recythonize_on_pxd_change(self, ext, pxd_exists_for_first_check):
        module_filename = 'a' + ext

        pxd_to_be_modified = os.path.join(self.src_dir, 'a.pxd')
        module = os.path.join(self.src_dir, module_filename)
        module_c_file = os.path.join(self.src_dir, 'a.c')  # should change

        module_line_1 = LINE_BEFORE_IMPLEMENTATION.format(
            filename=module_filename, at_line=1)

        if pxd_exists_for_first_check:
            write_file(pxd_to_be_modified, 'cdef int x\n')

        write_file(module, 'x = 1\n')

        dependencies = self.fresh_all_dependencies(module)
        self.assertIn(module, dependencies)
        if pxd_exists_for_first_check:
            self.assertIn(pxd_to_be_modified, dependencies)
            self.assertEqual(2, len(dependencies))
        else:
            self.assertEqual(1, len(dependencies))

        # Create a.c
        self.fresh_cythonize(module)

        definition_before = self.relative_lines_from_file(
            module_c_file, module_line_1, 0, 7)

        if pxd_exists_for_first_check:
            self.assertIn("a_x = 1;", definition_before, INCORRECT)
        else:
            self.assertNotIn("a_x = 1;", definition_before, INCORRECT)

        # See https://github.com/cython/cython/issues/4245
        write_newer_file(pxd_to_be_modified, module_c_file, 'cdef float x\n')

        # otherwise nothing changes since there are no new files
        if not pxd_exists_for_first_check:
            dependencies = self.fresh_all_dependencies(module)
            self.assertIn(module, dependencies)
            self.assertIn(pxd_to_be_modified, dependencies)
            self.assertEqual(2, len(dependencies))

        # Change a.c
        self.fresh_cythonize(module)

        definition_after = self.relative_lines_from_file(
            module_c_file, module_line_1, 0, 7)

        self.assertNotIn("a_x = 1;", definition_after, SAME)
        self.assertIn("a_x = 1.0;", definition_after, INCORRECT)

    # pxd_exists_for_first_check is not used because cimport requires pxd
    # to import another script.
    def recythonize_on_dep_pxd_change(self, ext_a, ext_b):
        dep_filename, module_filename = "a" + ext_a, "b" + ext_b

        pxd_to_be_modified = os.path.join(self.src_dir, 'a.pxd')
        module_dependency = os.path.join(self.src_dir, dep_filename)
        dep_c_file = os.path.join(self.src_dir, 'a.c')  # should change
        pxd_for_cimport = os.path.join(self.src_dir, 'b.pxd')
        module = os.path.join(self.src_dir, module_filename)
        module_c_file = os.path.join(self.src_dir, 'b.c')  # should change

        dep_line_1 = LINE_BEFORE_IMPLEMENTATION.format(
            filename=dep_filename, at_line=1)
        module_line_1 = LINE_BEFORE_IMPLEMENTATION.format(
            filename=module_filename, at_line=1)

        write_file(pxd_to_be_modified, 'cdef int x\n')
        write_file(module_dependency, 'x = 1\n')
        write_file(pxd_for_cimport, 'cimport a\n')
        write_file(module, 'a.x = 2\n')

        dependencies = self.fresh_all_dependencies(module)
        self.assertIn(pxd_for_cimport, dependencies)
        self.assertIn(module, dependencies)
        self.assertIn(pxd_to_be_modified, dependencies)
        self.assertEqual(3, len(dependencies))

        # Create a.c and b.c
        self.fresh_cythonize([module_dependency, module])

        dep_definition_before = self.relative_lines_from_file(
            dep_c_file, dep_line_1, 0, 7)

        module_definition_before = self.relative_lines_from_file(
            module_c_file, module_line_1, 0, 7)

        self.assertIn("a_x = 1;", dep_definition_before, INCORRECT)
        self.assertIn("a_x = 2;", module_definition_before, INCORRECT)

        # See https://github.com/cython/cython/issues/4245
        write_newer_file(pxd_to_be_modified, module_c_file, 'cdef float x\n')

        # Change a.c and b.c
        self.fresh_cythonize([module_dependency, module])

        dep_definition_after = self.relative_lines_from_file(
            dep_c_file, dep_line_1, 0, 7)

        module_definition_after = self.relative_lines_from_file(
            module_c_file, module_line_1, 0, 7)

        self.assertNotIn("a_x = 1;", dep_definition_after, SAME)
        self.assertNotIn("a_x = 2;", module_definition_after, SAME)
        self.assertIn("a_x = 1.0;", dep_definition_after, INCORRECT)
        self.assertIn("a_x = 2.0;", module_definition_after, INCORRECT)

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
