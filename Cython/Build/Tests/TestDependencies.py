import contextlib
import os.path
import pathlib
import re
import tempfile
import unittest
from os.path import join as pjoin

from ...Utils import open_source_file
from ..Dependencies import extended_iglob, strip_string_literals


@contextlib.contextmanager
def writable_file(dir_path, filename):
    with open(pjoin(dir_path, filename), "w", encoding="utf8") as f:
        yield f


class TestGlobbing(unittest.TestCase):
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


class TestCodeProcessing(unittest.TestCase):
    maxDiff = None

    @staticmethod
    def _rebuild_string(stripped, literals):
        def lookup(match):
            return literals[match.group()]

        return re.sub("__Pyx_L[0-9]+_", lookup, stripped)

    def test_strip_string_literals(self):
        def strip_equals(s, expected):
            stripped, literals = strip_string_literals(s)
            self.assertEqual(expected, stripped)

            recovered = self._rebuild_string(stripped, literals)
            self.assertEqual(s, recovered)

        unchanged = [
            """abc""",
            """123""",
            """func(123)""",
            """ '' """,
            """ '''''''''''' """,
            """ '''''''''''''' """,
        ]

        tests = [(code, code) for code in unchanged] + [
            (""" '''' ''' """,
             """ '''__Pyx_L1_''' """),

            (''' """" """ ''',
             ''' """__Pyx_L1_""" '''),

            (""" func('xyz') + " " + "" '' # '' | "" "123" 'xyz' "' """,
             """ func('__Pyx_L1_') + "__Pyx_L2_" + "" '' # __Pyx_L3_"""),

            (""" f'f' """,
             """ f'__Pyx_L1_' """),

            (""" f'a{123}b' """,
             """ f'__Pyx_L1_{123}__Pyx_L2_' """),

            (""" f'{1}{f'xyz'}' """,
             """ f'{1}{f'__Pyx_L1_'}' """),

            (""" f'{f'''xyz{f\"""abc\"""}'''}' """,
             """ f'{f'''__Pyx_L1_{f\"""__Pyx_L2_\"""}'''}' """),

            (""" f'{{{{{"abc"}}}}}{{}}{{' == '{{abc}}{}{' """,
             """ f'__Pyx_L1_{"__Pyx_L2_"}__Pyx_L3_' == '__Pyx_L4_' """),
        ]

        for code, expected in tests:
            with self.subTest(code=code):
                strip_equals(code, expected)
            code = code.strip()
            expected = expected.strip()
            with self.subTest(code=code):
                strip_equals(code, expected)
            code += "\n"
            expected += "\n"
            with self.subTest(code=code):
                strip_equals(code, expected)

        # GH5977: unclosed string literal
        strip_equals(
            """ print("Say something: %s' % something) """,
            """ print("__Pyx_L1_"""
        )


    def _test_all_files(self, base_dir, file_paths):
        _find_leftover_string = re.compile(r"""[^_'"}](['"]+)[^_'"{]""").search
        for file_path in sorted(file_paths):
            with self.subTest(file=str(file_path.relative_to(base_dir))):
                with open_source_file(str(file_path)) as f:
                    code = f.read()
                stripped, literals = strip_string_literals(code)

                match = _find_leftover_string(stripped)
                if match and len(match.group(1)) != 2:
                    match_pos = match.start() + 1
                    self.fail(f"Leftover string found: {stripped[match_pos - 12 : match_pos + 12]!r}")

                recovered = self._rebuild_string(stripped, literals)
                self.assertEqual(code, recovered)


    def test_strip_string_literals_py_files(self):
        # process all .py files in the Cython package
        package_dir = pathlib.Path(__file__).absolute().parents[2]
        assert package_dir.name == 'Cython'
        base_dir = package_dir.parent
        self._test_all_files(base_dir, package_dir.rglob("*.py"))

    def test_strip_string_literals_test_files(self):
        # process all .py[x] files in the tests package
        base_dir = pathlib.Path(__file__).absolute().parents[3]
        tests_dir = base_dir / 'tests'
        test_files = []
        for test_subdir in tests_dir.iterdir():
            if test_subdir.is_dir() and test_subdir.name != 'errors':
                test_files.extend(test_subdir.rglob("*.py"))
                test_files.extend(test_subdir.rglob("*.pyx"))
        self._test_all_files(base_dir, test_files)
