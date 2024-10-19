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

import functools
import re
import os
import sys

# Make sure we import the right Cython
cythonpath, _ = os.path.split(os.path.realpath(__file__)) # bin directory
cythonpath, _ = os.path.split(cythonpath)
if os.path.exists(os.path.join(cythonpath, "Cython")):
    sys.path.insert(0, cythonpath)
    print("Found (and using) local cython directory")
# else we aren't in a development directory

from Cython.Compiler import Lexicon


def main():
    arg = '--overwrite'
    if len(sys.argv) == 2:
        arg = sys.argv[1]
    if len(sys.argv) > 2 or arg not in ['--overwrite','--here']:
        print("""Call the script with either:
  --overwrite    to update the existing Lexicon.py file (default)
  --here         to create an version of Lexicon.py in the current directory
""")
        return

    generated_code = (
        f"# Generated with 'cython-generate-lexicon.py' based on:\n"
        f"# {sys.implementation.name} {sys.version.splitlines()[0].strip()}\n"
        "\n"
        f"{generate_character_sets()}\n"
    )

    print("Reading file", Lexicon.__file__)
    with open(Lexicon.__file__, 'r') as f:
        parts = re.split(r"(# (?:BEGIN|END) GENERATED CODE\n?)", f.read())

    if len(parts) not in (4,5) or ' GENERATED CODE' not in parts[1] or ' GENERATED CODE' not in parts[3]:
        print("Warning: generated code section not found - code not inserted")
        return

    parts[2] = generated_code
    output = "".join(parts)

    if arg == "--here":
        outfile = "Lexicon.py"
    else:
        assert arg == "--overwrite"
        outfile = Lexicon.__file__

    print("Writing to file", outfile)
    with open(outfile, 'w') as f:
        f.write(output)


# The easiest way to generate an appropriate character set is just to use the str.isidentifier method
# An alternative approach for getting character sets is at https://stackoverflow.com/a/49332214/4657412
@functools.lru_cache()
def get_start_characters_as_number():
    return [ i for i in range(sys.maxunicode) if str.isidentifier(chr(i)) ]


def get_continue_characters_as_number():
    return [ i for i in range(sys.maxunicode) if str.isidentifier('a'+chr(i)) ]


def get_continue_not_start_as_number():
    start = get_start_characters_as_number()
    cont = get_continue_characters_as_number()
    assert set(start) <= set(cont), \
        "We assume that all identifier start characters are also continuation characters."
    return sorted(set(cont).difference(start))


def to_ranges(char_num_list):
    # Convert the large lists of character digits to
    #  list of characters
    #  a list pairs of characters representing closed ranges
    char_num_list = sorted(char_num_list)
    first_good_val = char_num_list[0]

    single_chars = []
    ranges = []
    for n in range(1, len(char_num_list)):
        if char_num_list[n]-1 != char_num_list[n-1]:
            # discontinuous
            if first_good_val == char_num_list[n-1]:
                single_chars.append(chr(char_num_list[n-1]))
            else:
                ranges.append(chr(first_good_val) + chr(char_num_list[n-1]))
            first_good_val = char_num_list[n]

    return ''.join(single_chars), ''.join(ranges)


def escape_chars(chars):
    escapes = []
    for char in chars:
        charval = ord(char)
        escape = f'\\U{charval:08x}' if charval > 65535 else f'\\u{charval:04x}'
        escapes.append(escape)
    return ''.join(escapes)


def make_split_strings(chars, splitby=113, indent="    "):
    splitby //= 10  # max length of "\U..." unicode escapes
    lines = [f'"{escape_chars(chars[i:i+splitby])}"' for i in range(0, len(chars), splitby)]
    return indent + f"\n{indent}".join(lines)


def generate_character_sets():
    declarations = []
    for char_type, char_generator in [
        ("unicode_start_ch", get_start_characters_as_number),
        ("unicode_continuation_ch", get_continue_not_start_as_number),
    ]:
        for set_type, chars in zip(("any", "range"), to_ranges(char_generator())):
            declarations.append(
                f"{char_type}_{set_type} = (\n"
                f"{make_split_strings(chars)}\n"
                f")\n"
            )

    return "".join(declarations)


if __name__ == "__main__":
    main()
