#!/usr/bin/env python

import sys

from Cython.Debugger import Cygdb as cygdb

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cygdb.main(path_to_debug_info=sys.argv[1], 
                   gdb_argv=sys.argv[2:])
    else:
        cygdb.main()
