from TreeFragment import parse_from_strings, StringParseContext
from Scanning import StringSourceDescriptor
import Symtab
import Naming
from Cython.Compiler import Visitor


class CythonUtilityCode(object):
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
        # The AutoTestDictTransform creates the statement "__test__ = {}",
        # which when copied into the main ModuleNode overwrites
        # any __test__ in user code; not desired
        excludes = [AutoTestDictTransform]
        
        import Pipeline, ParseTreeTransforms
        #context = CythonUtilityCodeContext(self.name)
        #context.prefix = self.prefix
        context = StringParseContext(self.name)
        tree = parse_from_strings(self.name, self.pyx, context=context)
        pipeline = Pipeline.create_pipeline(context, 'pyx', exclude_classes=excludes)

        transform = ParseTreeTransforms.CnameDirectivesTransform(context)
        # InterpretCompilerDirectives already does a cdef declarator check
        #before = ParseTreeTransforms.DecoratorTransform
        before = ParseTreeTransforms.InterpretCompilerDirectives
        pipeline = Pipeline.insert_into_pipeline(pipeline, transform,
                                                 before=before)

        (err, tree) = Pipeline.run_pipeline(pipeline, tree)
        assert not err
        return tree

    def put_code(self, output):
        pass
