#
#   Cython -- Main Program, generic
#

if __name__ == '__main__':

    from Cython.Compiler.Main import main
    main(command_line = 1)

else:
    # Void cython.* directives.
    from Cython.Shadow import *
