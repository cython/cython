import contextlib
import os
import tempfile
from os.path import join as pjoin

from ..Dependencies import extended_iglob, parse_dependencies
from ...TestUtils import TimedTest


@contextlib.contextmanager
def writable_file(dir_path, filename):
    with open(pjoin(dir_path, filename), "w", encoding="utf8") as f:
        yield f


class TestGlobbing(TimedTest):
    @classmethod
    def setUpClass(cls):
        cls._orig_dir = os.getcwd()
        cls._tmpdir = tempfile.TemporaryDirectory()
        temp_path = cls._tmpdir.name
        os.chdir(temp_path)

        for dir1 in "abcd":
            for dir1x in [dir1, dir1 + 'x']:
                for dir2 in "xyz":
                    dir_path = pjoin(dir1x, dir2)
                    os.makedirs(dir_path)
                    with writable_file(dir_path, "file2_pyx.pyx") as f:
                        f.write('""" PYX """')
                    with writable_file(dir_path, "file2_py.py") as f:
                        f.write('""" PY """')

                with writable_file(dir1x, "file1_pyx.pyx") as f:
                    f.write('""" PYX """')
                with writable_file(dir1x, "file1_py.py") as f:
                    f.write('""" PY """')

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls._orig_dir)
        cls._tmpdir.cleanup()

    def files_equal(self, pattern, expected_files):
        expected_files = sorted(expected_files)
        # It's the users's choice whether '/' will appear on Windows.
        matched_files = sorted(path.replace('/', os.sep) for path in extended_iglob(pattern))
        self.assertListEqual(matched_files, expected_files)  # /

        # Special case for Windows: also support '\' in patterns.
        if os.sep == '\\' and '/' in pattern:
            matched_files = sorted(extended_iglob(pattern.replace('/', '\\')))
            self.assertListEqual(matched_files, expected_files)  # \

    def test_extended_iglob_simple(self):
        ax_files = [pjoin("a", "x", "file2_pyx.pyx"), pjoin("a", "x", "file2_py.py")]
        self.files_equal("a/x/*", ax_files)
        self.files_equal("a/x/*.c12", [])
        self.files_equal("a/x/*.{py,pyx,c12}", ax_files)
        self.files_equal("a/x/*.{py,pyx}", ax_files)
        self.files_equal("a/x/*.{pyx}", ax_files[:1])
        self.files_equal("a/x/*.pyx", ax_files[:1])
        self.files_equal("a/x/*.{py}", ax_files[1:])
        self.files_equal("a/x/*.py", ax_files[1:])

    def test_extended_iglob_simple_star(self):
        for basedir in "ad":
            files = [
                pjoin(basedir, dirname, filename)
                for dirname in "xyz"
                for filename in ["file2_pyx.pyx", "file2_py.py"]
            ]
            self.files_equal(basedir + "/*/*", files)
            self.files_equal(basedir + "/*/*.c12", [])
            self.files_equal(basedir + "/*/*.{py,pyx,c12}", files)
            self.files_equal(basedir + "/*/*.{py,pyx}", files)
            self.files_equal(basedir + "/*/*.{pyx}", files[::2])
            self.files_equal(basedir + "/*/*.pyx", files[::2])
            self.files_equal(basedir + "/*/*.{py}", files[1::2])
            self.files_equal(basedir + "/*/*.py", files[1::2])

            for subdir in "xy*":
                files = [
                    pjoin(basedir, dirname, filename)
                    for dirname in "xyz"
                    if subdir in ('*', dirname)
                    for filename in ["file2_pyx.pyx", "file2_py.py"]
                ]
                path = basedir + '/' + subdir + '/'
                self.files_equal(path + "*", files)
                self.files_equal(path + "*.{py,pyx}", files)
                self.files_equal(path + "*.{pyx}", files[::2])
                self.files_equal(path + "*.pyx", files[::2])
                self.files_equal(path + "*.{py}", files[1::2])
                self.files_equal(path + "*.py", files[1::2])

    def test_extended_iglob_double_star(self):
        basedirs = os.listdir(".")
        files = [
            pjoin(basedir, dirname, filename)
            for basedir in basedirs
            for dirname in "xyz"
            for filename in ["file2_pyx.pyx", "file2_py.py"]
        ]
        all_files = [
            pjoin(basedir, filename)
            for basedir in basedirs
            for filename in ["file1_pyx.pyx", "file1_py.py"]
        ] + files
        self.files_equal("*/*/*", files)
        self.files_equal("*/*/**/*", files)
        self.files_equal("*/**/*.*", all_files)
        self.files_equal("**/*.*", all_files)
        self.files_equal("*/**/*.c12", [])
        self.files_equal("**/*.c12", [])
        self.files_equal("*/*/*.{py,pyx,c12}", files)
        self.files_equal("*/*/**/*.{py,pyx,c12}", files)
        self.files_equal("*/**/*/*.{py,pyx,c12}", files)
        self.files_equal("**/*/*/*.{py,pyx,c12}", files)
        self.files_equal("**/*.{py,pyx,c12}", all_files)
        self.files_equal("*/*/*.{py,pyx}", files)
        self.files_equal("**/*/*/*.{py,pyx}", files)
        self.files_equal("*/**/*/*.{py,pyx}", files)
        self.files_equal("**/*.{py,pyx}", all_files)
        self.files_equal("*/*/*.{pyx}", files[::2])
        self.files_equal("**/*.{pyx}", all_files[::2])
        self.files_equal("*/**/*/*.pyx", files[::2])
        self.files_equal("*/*/*.pyx", files[::2])
        self.files_equal("**/*.pyx", all_files[::2])
        self.files_equal("*/*/*.{py}", files[1::2])
        self.files_equal("**/*.{py}", all_files[1::2])
        self.files_equal("*/*/*.py", files[1::2])
        self.files_equal("**/*.py", all_files[1::2])


class TestParseDependencies(TimedTest):
    def cimports(self, source):
        # parse_dependencies() is cached by file name, so use a new directory for every call.
        with tempfile.TemporaryDirectory() as tmp:
            path = pjoin(tmp, "mod.pyx")
            with open(path, "w", encoding="utf8") as f:
                f.write(source)
            return parse_dependencies(path)[0]

    def test_from_cimport_submodule(self):
        expected = ["pkg", "pkg.submodule"]
        self.assertEqual(self.cimports("from pkg cimport submodule\n"), expected)
        self.assertEqual(self.cimports("from pkg cimport submodule"), expected)
        self.assertEqual(self.cimports("from pkg cimport submodule  # comment\n"), expected)

    def test_from_cimport_ignores_following_lines(self):
        self.assertEqual(
            self.cimports("from pkg cimport submodule\nif x:\n    pass\n"),
            ["pkg", "pkg.submodule"])

    def test_from_cimport_several_names(self):
        expected = ["pkg", "pkg.a", "pkg.b"]
        self.assertEqual(self.cimports("from pkg cimport a, b\n"), expected)
        self.assertEqual(self.cimports("from pkg cimport (a, b)\n"), expected)
        self.assertEqual(self.cimports("from pkg cimport a, \\\n    b\n"), expected)

    def test_from_cimport_multiline(self):
        expected = ["pkg", "pkg.a", "pkg.b"]
        self.assertEqual(self.cimports("from pkg cimport (\n    a,\n    b,\n)\n"), expected)
        self.assertEqual(self.cimports("from pkg cimport (\n    a,\n    b\n)\n"), expected)

    def test_from_cimport_alias(self):
        self.assertEqual(
            self.cimports("from pkg cimport a as x, b\n"), ["pkg", "pkg.a", "pkg.b"])

    def test_from_cython_cimports(self):
        self.assertEqual(
            self.cimports("from cython.cimports.pkg import submodule\n"),
            ["pkg", "pkg.submodule"])
