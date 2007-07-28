from distutils.core import setup
from distutils.sysconfig import get_python_lib
import os
from Cython.Compiler.Version import version

compiler_dir = os.path.join(get_python_lib(prefix=''), 'Cython/Compiler')

if os.name == "posix":
    scripts = ["bin/cython"]
else:
    scripts = ["cython.py"]

setup(
  name = 'Cython', 
  version = version,
  url = 'http://www.cython.org',
  author = 'Greg Ewing, William Stein, Robert Bradshaw, Stefan Behnel, et al.',
  author_email = 'wstein@gmail.com',
  scripts = scripts,
  packages=[
    'Cython',
    'Cython.Compiler',
    'Cython.Distutils',
    'Cython.Mac',
    'Cython.Plex'
    ],
  data_files=[
    (compiler_dir, ['Cython/Compiler/Lexicon.pickle'])
    ]
  )

