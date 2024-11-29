from Cython.Compiler import Options
from Cython.Compiler import Pipeline
from Cython.Compiler import Errors
from Cython.Compiler import Main
from Cython.Compiler import Symtab
from Cython.Compiler import MemoryView
from Cython.Compiler.StringEncoding import EncodedString
from Cython.Compiler.Scanning import StringSourceDescriptor, FileSourceDescriptor

Errors.init_thread()
Errors.open_listing_file(None)
Options.generate_cyshared = True

options = Options.CompilationOptions()
context = Main.Context.from_options(options)
scope = Symtab.ModuleScope('MemoryView', parent_module = None, context = context, is_package=False)

source = StringSourceDescriptor("MemoryView", '')
source.filename = 'MemoryView.pyx'
# source = FileSourceDescriptor('cyshared.pxd')
comp_src = Main.CompilationSource(source, EncodedString('MemoryView'), '.')
result = Main.create_default_resultobj(comp_src, options)

pipeline = Pipeline.create_dummy_pipeline(context, scope, options, result)
result = Pipeline.run_pipeline(pipeline, comp_src)
print(result)
