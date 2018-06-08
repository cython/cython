"""
Inject Cython type declarations into a .py file using the Jedi static analysis tool.
"""

from __future__ import absolute_import

from io import open
from collections import defaultdict
from itertools import chain

import jedi
from jedi.parser.tree import Module, ImportName
from jedi.evaluate.representation import Function, Instance, Class
from jedi.evaluate.iterable import ArrayMixin, GeneratorComprehension

from Cython.Utils import open_source_file


default_type_map = {
    'float': 'double',
    'int': 'long',
}


def analyse(source_path=None, code=None):
    """
    Analyse a Python source code file with Jedi.
    Returns a mapping from (scope-name, (line, column)) pairs to a name-types mapping.
    """
    if not source_path and code is None:
        raise ValueError("Either 'source_path' or 'code' is required.")
    scoped_names = {}
    statement_iter = jedi.names(source=code, path=source_path, all_scopes=True)

    for statement in statement_iter:
        parent = statement.parent()
        scope = parent._definition
        evaluator = statement._evaluator

        # skip function/generator definitions, class definitions, and module imports
        if any(isinstance(statement._definition, t) for t in [Function, Class, ImportName]):
            continue
        key = (None if isinstance(scope, Module) else str(parent.name), scope.start_pos)
        try:
            names = scoped_names[key]
        except KeyError:
            names = scoped_names[key] = defaultdict(set)

        position = statement.start_pos if statement.name in names else None

        for name_type in evaluator.find_types(scope, statement.name, position=position ,search_global=True):
            if isinstance(name_type, Instance):
                if isinstance(name_type.base, Class):
                    type_name = 'object'
                else:
                    type_name = name_type.base.obj.__name__
            elif isinstance(name_type, ArrayMixin):
                type_name = name_type.type
            elif isinstance(name_type, GeneratorComprehension):
                type_name = None
            else:
                try:
                    type_name = type(name_type.obj).__name__
                except AttributeError as error:
                    type_name = None
            if type_name is not None:
                names[str(statement.name)].add(type_name)
    return scoped_names


def inject_types(source_path, types, type_map=default_type_map, mode='python'):
    """
    Hack type declarations into source code file.

    @param mode is currently 'python', which means that the generated type declarations use pure Python syntax.
    """
    col_and_types_by_line = dict(
        # {line: (column, scope_name or None, [(name, type)])}
        (k[-1][0], (k[-1][1], k[0], [(n, next(iter(t))) for (n, t) in v.items() if len(t) == 1]))
        for (k, v) in types.items())

    lines = [u'import cython\n']
    with open_source_file(source_path) as f:
        for line_no, line in enumerate(f, 1):
            if line_no in col_and_types_by_line:
                col, scope, types = col_and_types_by_line[line_no]
                if types:
                    types = ', '.join("%s='%s'" % (name, type_map.get(type_name, type_name))
                                    for name, type_name in types)
                    if scope is None:
                        type_decl = u'{indent}cython.declare({types})\n'
                    else:
                        type_decl = u'{indent}@cython.locals({types})\n'
                    lines.append(type_decl.format(indent=' '*col, types=types))
            lines.append(line)

    return lines


def main(file_paths=None, overwrite=False):
    """
    Main entry point to process a list of .py files and inject type inferred declarations.
    """
    if file_paths is None:
        import sys
        file_paths = sys.argv[1:]

    for source_path in file_paths:
        types = analyse(source_path)
        lines = inject_types(source_path, types)
        target_path = source_path + ('' if overwrite else '_typed.py')
        with open(target_path, 'w', encoding='utf8') as f:
            for line in lines:
                f.write(line)


if __name__ == '__main__':
    main()
