#!/usr/bin/env python

import sys

from Cython.Debugger import Cygdb as cygdb

if __name__ == '__main__':
    if len(sys.argv) > 1:
        path_to_debug_info = sys.argv[1]
        
        no_import = False
        if path_to_debug_info == '--':
            no_import = True
        
        cygdb.main(path_to_debug_info, 
                   gdb_argv=sys.argv[2:],
                   no_import=no_import)
    else:
        cygdb.main()
