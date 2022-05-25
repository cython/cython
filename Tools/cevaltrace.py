#!/usr/bin/env python3

"""
Translate the byte code of a Python function into the corresponding
sequences of C code in CPython's "ceval.c".
"""

from __future__ import print_function, absolute_import

import re
import os.path

from dis import get_instructions  # requires Python 3.4+

# collapse some really boring byte codes
_COLLAPSE = {'NOP', 'LOAD_CONST', 'POP_TOP', 'JUMP_FORWARD'}
#_COLLAPSE.clear()

_is_start = re.compile(r"\s* switch \s* \( opcode \)", re.VERBOSE).match
# Py3: TARGET(XX), Py2: case XX
_match_target = re.compile(r"\s* (?: TARGET \s* \( | case \s* ) \s* (\w+) \s* [:)]", re.VERBOSE).match
_ignored = re.compile(r"\s* PREDICTED[A-Z_]*\(", re.VERBOSE).match
_is_end = re.compile(r"\s* } \s* /\* \s* switch \s* \*/", re.VERBOSE).match

_find_pyversion = re.compile(r'\#define \s+ PY_VERSION \s+ "([^"]+)"', re.VERBOSE).findall

class ParseError(Exception):
    def __init__(self, message="Failed to parse ceval.c"):
        super(ParseError, self).__init__(message)


def parse_ceval(file_path):
    snippets = {}
    with open(file_path) as f:
        lines = iter(f)

        for line in lines:
            if _is_start(line):
                break
        else:
            raise ParseError()

        targets = []
        code_lines = []
        for line in lines:
            target_match = _match_target(line)
            if target_match:
                if code_lines:
                    code = ''.join(code_lines).rstrip()
                    for target in targets:
                        snippets[target] = code
                    del code_lines[:], targets[:]
                targets.append(target_match.group(1))
            elif _ignored(line):
                pass
            elif _is_end(line):
                break
            else:
                code_lines.append(line)
        else:
            if not snippets:
                raise ParseError()
    return snippets


def translate(func, ceval_snippets):
    start_offset = 0
    code_obj = getattr(func, '__code__', None)
    if code_obj and os.path.exists(code_obj.co_filename):
        start_offset = code_obj.co_firstlineno
        with open(code_obj.co_filename) as f:
            code_line_at = {
                i: line.strip()
                for i, line in enumerate(f, 1)
                if line.strip()
            }.get
    else:
        code_line_at = lambda _: None

    for instr in get_instructions(func):
        code_line = code_line_at(instr.starts_line)
        line_no = (instr.starts_line or start_offset) - start_offset
        yield line_no, code_line, instr, ceval_snippets.get(instr.opname)


def main():
    import sys
    import importlib.util

    if len(sys.argv) < 3:
        print("Usage:  %s  path/to/Python/ceval.c  script.py ..." % sys.argv[0], file=sys.stderr)
        return

    ceval_source_file = sys.argv[1]
    version_header = os.path.join(os.path.dirname(ceval_source_file), '..', 'Include', 'patchlevel.h')
    if os.path.exists(version_header):
        with open(version_header) as f:
            py_version = _find_pyversion(f.read())
        if py_version:
            py_version = py_version[0]
            if not sys.version.startswith(py_version + ' '):
                print("Warning:  disassembling with Python %s, but ceval.c has version %s" % (
                    sys.version.split(None, 1)[0],
                    py_version,
                ), file=sys.stderr)

    snippets = parse_ceval(ceval_source_file)

    for code in _COLLAPSE:
        if code in snippets:
            snippets[code] = ''

    for file_path in sys.argv[2:]:
        module_name = os.path.basename(file_path)
        print("/*######## MODULE %s ########*/" % module_name)
        print('')

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for func_name, item in sorted(vars(module).items()):
            if not callable(item):
                continue
            print("/* FUNCTION %s */" % func_name)
            print("static void")  # assuming that it highlights in editors
            print("%s() {" % func_name)

            last_line = None
            for line_no, code_line, instr, snippet in translate(item, snippets):
                if last_line != line_no:
                    if code_line:
                        print('')
                        print('/*# %3d  %s */' % (line_no, code_line))
                        print('')
                    last_line = line_no

                print("  %s:%s {%s" % (
                    instr.opname,
                    ' /* %s */' % instr.argrepr if instr.arg is not None else '',
                    ' /* ??? */' if snippet is None else ' /* ... */ }' if snippet == '' else '',
                ))
                print(snippet or '')

            print("} /* FUNCTION %s */" % func_name)


if __name__ == '__main__':
    main()
