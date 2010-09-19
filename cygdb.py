#!/usr/bin/env python

import sys
from Cython.Debugger import cygdb

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cygdb.main(path_to_debug_info=sys.argv[1])
    else:
        cygdb.main()