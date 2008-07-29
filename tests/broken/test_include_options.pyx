import sys
from Pyrex.Compiler.Main import main

sys.argv[1:] = "-I spam -Ieggs --include-dir ham".split()
main(command_line = 1)
