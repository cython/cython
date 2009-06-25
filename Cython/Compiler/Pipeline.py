#
# Really small pipeline stages
#
def dumptree(t):
    # For quick debugging in pipelines
    print t.dump()
    return t

def create_parse(context):
    def parse(compsrc):
        source_desc = compsrc.source_desc
        full_module_name = compsrc.full_module_name
        initial_pos = (source_desc, 1, 0)
        scope = context.find_module(full_module_name, pos = initial_pos, need_pxd = 0)
        tree = context.parse(source_desc, scope, pxd = 0, full_module_name = full_module_name)
        tree.compilation_source = compsrc
        tree.scope = scope
        tree.is_pxd = False
        return tree
    return parse

#
# Pipeline factories
#

def create_pipeline(context, pxd, py=False):
    from Visitor import PrintTree
    from ParseTreeTransforms import WithTransform, NormalizeTree, PostParse, PxdPostParse
    from ParseTreeTransforms import AnalyseDeclarationsTransform, AnalyseExpressionsTransform
    from ParseTreeTransforms import CreateClosureClasses, MarkClosureVisitor, DecoratorTransform
    from ParseTreeTransforms import InterpretCompilerDirectives, TransformBuiltinMethods
    from ParseTreeTransforms import AlignFunctionDefinitions, GilCheck
    from AutoDocTransforms import EmbedSignature
    from Optimize import FlattenInListTransform, SwitchTransform, IterationTransform
    from Optimize import OptimizeBuiltinCalls, ConstantFolding, FinalOptimizePhase
    from Buffer import IntroduceBufferAuxiliaryVars
    from ModuleNode import check_c_declarations


    # Temporary hack that can be used to ensure that all result_code's
    # are generated at code generation time.
    import Visitor
    class ClearResultCodes(Visitor.CythonTransform):
        def visit_ExprNode(self, node):
            self.visitchildren(node)
            node.result_code = "<cleared>"
            return node

    if pxd:
        _check_c_declarations = None
        _specific_post_parse = PxdPostParse(context)
    else:
        _check_c_declarations = check_c_declarations
        _specific_post_parse = None

    if py and not pxd:
        _align_function_definitions = AlignFunctionDefinitions(context)
    else:
        _align_function_definitions = None

    return [
        NormalizeTree(context),
        PostParse(context),
        _specific_post_parse,
        InterpretCompilerDirectives(context, context.pragma_overrides),
        _align_function_definitions,
        ConstantFolding(),
        FlattenInListTransform(),
        WithTransform(context),
        DecoratorTransform(context),
        AnalyseDeclarationsTransform(context),
        EmbedSignature(context),
        TransformBuiltinMethods(context),
        IntroduceBufferAuxiliaryVars(context),
        _check_c_declarations,
        AnalyseExpressionsTransform(context),
        OptimizeBuiltinCalls(),
        ConstantFolding(),
        IterationTransform(),
        SwitchTransform(),
        FinalOptimizePhase(context),
        GilCheck(),
    #            ClearResultCodes(context),
    #            SpecialFunctions(context),
        #        CreateClosureClasses(context),
        ]

def create_pyx_pipeline(context, options, result, py=False):
    def generate_pyx_code(module_node):
        module_node.process_implementation(options, result)
        result.compilation_source = module_node.compilation_source
        return result

    def inject_pxd_code(module_node):
        from textwrap import dedent
        stats = module_node.body.stats
        for name, (statlistnode, scope) in context.pxds.iteritems():
            # Copy over function nodes to the module
            # (this seems strange -- I believe the right concept is to split
            # ModuleNode into a ModuleNode and a CodeGenerator, and tell that
            # CodeGenerator to generate code both from the pyx and pxd ModuleNodes.
             stats.append(statlistnode)
             # Until utility code is moved to code generation phase everywhere,
             # we need to copy it over to the main scope
             module_node.scope.utility_code_list.extend(scope.utility_code_list)
        return module_node

    return ([
            create_parse(context),
        ] + create_pipeline(context, pxd=False, py=py) + [
            inject_pxd_code,
            generate_pyx_code,
        ])

def create_pxd_pipeline(context, scope, module_name):
    def parse_pxd(source_desc):
        tree = context.parse(source_desc, scope, pxd=True,
                          full_module_name=module_name)
        tree.scope = scope
        tree.is_pxd = True
        return tree

    from CodeGeneration import ExtractPxdCode

    # The pxd pipeline ends up with a CCodeWriter containing the
    # code of the pxd, as well as a pxd scope.
    return [parse_pxd] + create_pipeline(context, pxd=True) + [
        ExtractPxdCode(context),
        ]

def create_py_pipeline(context, options, result):
    return create_pyx_pipeline(context, options, result, py=True)

