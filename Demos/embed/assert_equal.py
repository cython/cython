from __future__ import absolute_import, print_function

import sys

f1 = open(sys.argv[1])
f2 = open(sys.argv[2])
try:
    if f1.read() != f2.read():
        print("Files differ")
        sys.exit(1)
    else:
        print("Files identical")
finally:
    f1.close()
    f2.close()
