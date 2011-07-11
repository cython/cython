from TreeFragment import parse_from_strings, StringParseContext
from Scanning import StringSourceDescriptor
import Symtab
import Naming

class NonManglingModuleScope(Symtab.ModuleScope):
    def mangle(self, prefix, name=None):
        if name:
            if prefix in (Naming.typeobj_prefix, Naming.func_prefix):
                # Functions, classes etc. gets a manually defined prefix easily
                # manually callable instead (the one passed to CythonUtilityCode)
                prefix = self.prefix
            return "%s%s" % (prefix, name)
        else:
            return self.base.name

class CythonUtilityCodeContext(StringParseContext):
    scope = None
    
    def find_module(self, module_name, relative_to = None, pos = None, need_pxd = 1):
        if module_name != self.module_name:
            raise AssertionError("Not yet supporting any cimports/includes from string code snippets")
        if self.scope is None:
            self.scope = NonManglingModuleScope(module_name, parent_module = None, context = self)
            self.scope.prefix = self.prefix
        return self.scope

class CythonUtilityCode:
    """
    Utility code written in the Cython language itself.
    """

    def __init__(self, pyx, name="<utility code>", prefix=""):
        # 1) We need to delay the parsing/processing, so that all modules can be
        #    imported without import loops
        # 2) The same utility code object can be used for multiple source files;
        #    while the generated node trees can be altered in the compilation of a
        #    single file.
        # Hence, delay any processing until later.
        self.pyx = pyx
        self.name = name
        self.prefix = prefix

    def get_tree(self):
        from AnalysedTreeTransforms import AutoTestDictTransform
        excludes = [AutoTestDictTransform]
        
        import Pipeline
        context = CythonUtilityCodeContext(self.name)
        context.prefix = self.prefix
        tree = parse_from_strings(self.name, self.pyx, context=context)
        pipeline = Pipeline.create_pipeline(context, 'pyx', exclude_classes=excludes)
        (err, tree) = Pipeline.run_pipeline(pipeline, tree)
        assert not err
        return tree

    def put_code(self, output):
        pass


        
