import argparse
import tempfile
import sys
import os
import shutil

from Cython.Compiler import (
    MemoryView, Code, Options, Pipeline, Errors, Main, Symtab
)
from Cython.Compiler.StringEncoding import EncodedString
from Cython.Compiler.Scanning import FileSourceDescriptor

def create_shared_library_pipeline(context, scope, options, result):

    def generate_tree_factory(context):
        def generate_tree(compsrc):

            # Force to generate __Pyx_ExportFunction
            Options.cimport_from_pyx = True

            source_desc = compsrc.source_desc
            full_module_name = compsrc.full_module_name

            initial_pos = (source_desc, 1, 0)
            scope = context.find_module(full_module_name, pos = initial_pos, need_pxd = 0)

            tree = context.parse(source_desc, scope, pxd = 0, full_module_name = full_module_name)

            tree.is_pxd = False
            tree.compilation_source = compsrc
            tree.scope = scope

            scope.use_utility_code(MemoryView._get_memoryview_utility_code()[0])

            scope.use_utility_code(MemoryView._get_memoryview_utility_code()[1])
            scope.use_utility_code(MemoryView.typeinfo_to_format_code)
            context.include_directories.append(Code.get_utility_dir())
            return tree

        return generate_tree

    return [
        generate_tree_factory(context),
        *Pipeline.create_pipeline(context, 'pyx', exclude_classes=()),
        Pipeline.inject_pxd_code_stage_factory(context),
        Pipeline.inject_utility_code_stage_factory(context),
        Pipeline.inject_utility_pxd_code_stage_factory(context),
        Pipeline.abort_on_errors,
        Pipeline.generate_pyx_code_stage_factory(options, result),
    ]

def generate_shared_module(dest_dir):
    Errors.init_thread()
    Errors.open_listing_file(None)

    options = Options.CompilationOptions(language_level = 3)
    context = Main.Context.from_options(options)
    scope = Symtab.ModuleScope('MemoryView', parent_module = None, context = context, is_package=False)

    with tempfile.TemporaryDirectory() as tmpdirname:
        pyx_file = os.path.join(tmpdirname, 'MemoryView.pyx')
        c_file = os.path.join(tmpdirname, 'MemoryView.c')
        with open(pyx_file, 'w'):
            pass
        source_desc = FileSourceDescriptor(pyx_file)
        comp_src = Main.CompilationSource(source_desc, EncodedString('MemoryView'), os.getcwd())
        result = Main.create_default_resultobj(comp_src, options)

        pipeline = create_shared_library_pipeline(context, scope, options, result)
        err, enddata = Pipeline.run_pipeline(pipeline, comp_src)
        if err is None:
            shutil.copy(c_file, dest_dir)
            sys.exit(0)
        else:
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('DIR', nargs='?', default='.')
    args = parser.parse_args()
    if not os.path.isdir(args.DIR):
        print(f"{args.DIR} must be an existing directory.", file=sys.stderr)
        sys.exit(1)
    generate_shared_module(args.DIR)

if __name__ == '__main__':
    main()
