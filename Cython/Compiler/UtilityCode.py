from TreeFragment import parse_from_strings, StringParseContext
from Scanning import StringSourceDescriptor
import Symtab
import Naming

class NonManglingModuleScope(Symtab.ModuleScope):
    def mangle(self, prefix, name=None):
        if name:
            if prefix in (Naming.typeobj_prefix, Naming.func_prefix):
                return name
            else:
                return "%s%s" % (prefix, name)
        else:
            return self.base.name

class CythonUtilityCodeContext(StringParseContext):
    def find_module(self, module_name, relative_to = None, pos = None, need_pxd = 1):
        if module_name != self.module_name:
            raise AssertionError("Not yet supporting any cimports/includes from string code snippets")
        return NonManglingModuleScope(module_name, parent_module = None, context = self)

class CythonUtilityCode:
    """
    Utility code written in the Cython language itself.
    """

    def __init__(self, pyx, name="<utility code>"):
        # 1) We need to delay the parsing/processing, so that all modules can be
        #    imported without import loops
        # 2) The same utility code object can be used for multiple source files;
        #    while the generated node trees can be altered in the compilation of a
        #    single file.
        # Hence, delay any processing until later.
        self.pyx = pyx
        self.name = name

    def inject_tree_and_scope_into(self, module_node):
        import Pipeline
        context = CythonUtilityCodeContext(self.name)
        tree = parse_from_strings(self.name, self.pyx, context=context)
        tree.scope.scope_prefix = 'dagss'
        pipeline = Pipeline.create_pipeline(context, 'pyx')
        (err, tree) = Pipeline.run_pipeline(pipeline, tree)
        assert not err
        module_node.merge_in(tree.body, tree.scope, merge_scope=True)

    def put_code(self, output):
        pass


        
