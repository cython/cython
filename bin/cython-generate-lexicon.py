#!/usr/bin/env python3

#
#   Updates Cython's Lexicon.py with the unicode characters that are accepted as
#   identifiers. Should be run with the most recent version of Python possible
#   to ensure that Lexicon is as complete as possible.
#
#   Python3 only (it relies on str.isidentifier which is a Python 3 addition)
#
#   Run with either
#    --overwrite    to update the existing Lexicon.py file
#    --here         to create a copy of Lexicon.py in the current directory

import sys
from io import StringIO
import os

# Make sure we import the right Cython
cythonpath, _ = os.path.split(os.path.realpath(__file__)) # bin directory
cythonpath, _ = os.path.split(cythonpath)
if os.path.exists(os.path.join(cythonpath,"Cython")):
    sys.path.insert(0, cythonpath)
    print("Found (and using) local cython directory")
# else we aren't in a development directory

from Cython.Compiler import Lexicon

def main():
    if (len(sys.argv) != 2 or
        (sys.argv[1] not in ['--overwrite','--here'])):
        print("""Call the script with either:
  --overwrite    to update the existing Lexicon.py file
  --here         to create an version of Lexicon.py in the current directory
""")
        return

    generated_code = StringIO()
    print("# generated with:\n #",sys.implementation, file=generated_code)
    print(file=generated_code)
    print(start_expression(), file=generated_code)
    print(file=generated_code)
    print(cont_expression(),file=generated_code)
    print(file=generated_code)
    generated_code = generated_code.getvalue()

    output = StringIO()
    mode = 0 # 1 when found generated section, 2 afterwards
    print("Reading file", Lexicon.__file__)
    with open(Lexicon.__file__,'r') as f:
        for line in f:
            if mode != 1:
                output.write(line)
            else:
                if line.strip() == "# END GENERATED CODE":
                    mode = 2
                    output.write(line)
            if mode == 0:
                if line.strip() == "# BEGIN GENERATED CODE":
                    mode = 1
                    output.write(generated_code)

    if mode != 2:
        print("Warning: generated code section not found - code not inserted")
        return

    if sys.argv[1] == "--here":
        outfile = "Lexicon.py"
    elif sys.argv[1] == "--overwrite":
        outfile = Lexicon.__file__
    else:
        raise ValueError('argv: "{0}" not recognised', sys.argv[1])

    print("Writing to file", outfile)
    with open(outfile,'w') as f:
        f.write(output.getvalue())


# The easiest way to generate an appropriate character set is just to use the str.isidentifier method
# An alternative approach for getting character sets is at https://stackoverflow.com/a/49332214/4657412
def get_start_characters_as_number():
    return [ i for i in range(sys.maxunicode) if str.isidentifier(chr(i)) ]

def get_continue_characters_as_number():
    return [ i for i in range(sys.maxunicode) if str.isidentifier('a'+chr(i)) ]

def get_continue_not_start_as_number():
    start = get_start_characters_as_number()
    cont = get_continue_characters_as_number()
    return sorted(set(cont)-set(start))

def to_ranges(char_num_list):
    # Convert the large lists of character digits to
    #  list of characters
    #  a list pairs of characters representing closed ranges
    char_num_list = sorted(char_num_list)
    first_good_val = char_num_list[0]

    single_chars = []
    ranges = []
    for n in range(1,len(char_num_list)):
        if char_num_list[n]-1 != char_num_list[n-1]:
            # discontinuous
            if first_good_val==char_num_list[n-1]:
                single_chars.append(chr(char_num_list[n-1]))
            else:
                ranges.append(chr(first_good_val)+chr(char_num_list[n-1]))
            first_good_val = char_num_list[n]
    return single_chars, ranges

def make_split_strings(chars, splitby=60):
    out = []
    for i in range(0,len(chars), splitby):
        out.append('u"{}"'.format("".join(chars[i:i+splitby])))
    return "\n    ".join(out)

def start_expression():
    output = StringIO()
    print("unicode_start_ch_any = (\n    ", end='', file=output)

    single_chars, ranges = to_ranges(get_start_characters_as_number())
    single_chars = "".join(single_chars)
    ranges = "".join(ranges)

    print(make_split_strings(single_chars), end='', file=output)
    print(")", file=output)
    print("unicode_start_ch_range = (\n    ", end='', file=output)
    print(make_split_strings(ranges), end='', file=output)
    print(")", file=output)

    return output.getvalue()

def cont_expression():
    output = StringIO()
    print("unicode_continuation_ch_any = (\n    ", end='', file=output)

    single_chars, ranges = to_ranges(get_continue_not_start_as_number())
    single_chars = "".join(single_chars)
    ranges = "".join(ranges)

    print(make_split_strings(single_chars), end='', file=output)
    print(")", file=output)
    print("unicode_continuation_ch_range = (\n    ", end='', file=output)
    print(make_split_strings(ranges), end='', file=output)
    print(")", file=output)

    return output.getvalue()

if __name__ == "__main__":
    main()
