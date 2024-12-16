import argparse
import tempfile
import sys
import os
import shutil

from Cython.Compiler import Options
from Cython.Compiler import Pipeline
from Cython.Compiler import Errors
from Cython.Compiler import Main
from Cython.Compiler import Symtab
from Cython.Compiler.StringEncoding import EncodedString
from Cython.Compiler.Scanning import FileSourceDescriptor

def generate_shared_module(dest_dir):
    Errors.init_thread()
    Errors.open_listing_file(None)
    Options.use_shared_utility = True

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

        pipeline = Pipeline.create_shared_library_pipeline(context, scope, options, result)
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
