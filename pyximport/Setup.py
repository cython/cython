from distutils.core import setup
import sys, os
from StringIO import StringIO

if "sdist" in sys.argv:
    try:
        os.remove("MANIFEST")
    except (IOError, OSError):
        pass

    import html2text
    out = StringIO()
    html2text.convert_files(open("index.html"), out)
    out.write("\n\n")
    open("README", "w").write(out.getvalue())

setup(
    name = "pyximport",
    fullname = "Pyrex Import Hooks",
    version = "1.0",
    description = "Hooks to build and run Pyrex files as if they were simple Python files", 
    author = "Paul Prescod",
    author_email = "paul@prescod.net",
    url = "http://www.prescod.net/pyximport",
    license = "Python",
    keywords = "pyrex import hook",
#    scripts = ["pyxrun"],
#    data_files = [("examples/multi_file_extension", 
#         ["README", "ccode.c", "test.pyx", "test.pyxbld"]),
#       ("examples/dependencies",
#         ["README", "test.pyx", "test.pyxdep", "header.h",
#           "header2.h", "header3.h", "header4.h"])
#        ],
    py_modules = ["pyximport", "pyxbuild"])

