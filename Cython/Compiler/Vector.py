from Cython.Compiler import (ExprNodes, Nodes, PyrexTypes, Visitor,
                             Code, Naming)
from Cython.Compiler.Errors import error

from Cython.minivect import miniast
from Cython.minivect import minitypes
from Cython.minivect import miniutils
from Cython.minivect import minierror
from Cython.minivect import codegen
from Cython.minivect import specializers

debug = False

class TypeMapper(minitypes.TypeMapper):
    def map_type(self, type, wrap=False):
        if type.is_typedef:
            return minitypes.TypeWrapper(type)
        elif type.is_memoryviewslice:
            dtype = self.map_type(type.dtype, wrap=wrap)
            return minitypes.ArrayType(dtype, len(type.axes),
                                       is_c_contig=type.is_c_contig,
                                       is_f_contig=type.is_f_contig)
        elif type.is_float:
            if type == PyrexTypes.c_float_type:
                return minitypes.FloatType()
            elif type == PyrexTypes.c_double_type:
                return minitypes.DoubleType()
        elif type.is_int:
            if type == PyrexTypes.c_char_type:
                return minitypes.CharType()
            elif type == PyrexTypes.c_int_type:
                return minitypes.IntType()

        if wrap:
            return minitypes.TypeWrapper(type)
        else:
            raise minierror.UnmappableTypeError(type)

class CythonSpecializerMixin(object):
    def visit_NodeWrapper(self, node):
        for op in node.cython_ops:
            op.variable = self.visit(op.variable)
        return node

def create_hybrid_code(codegen, old_minicode):
    minicode = codegen.context.codewriter_cls(codegen.context)
    minicode.indent = old_minicode.indent
    code = CythonCCodeWriter(codegen.context, minicode)
    code.level = minicode.indent
    code.declaration_levels = list(old_minicode.declaration_levels)
    code.codegen = codegen.clone(codegen.context, code)
    return code

class CCodeGen(codegen.CCodeGen):

    def __init__(self, context, codewriter):
        super(CCodeGen, self).__init__(context, codewriter)
        self.error_handlers = []

    def visit_ErrorHandler(self, node):
        self.error_handlers.append(node)
        result = super(CCodeGen, self).visit_ErrorHandler(node)
        self.error_handlers.pop()
        return result

    def visit_FunctionNode(self, node):
        result = super(CCodeGen, self).visit_FunctionNode(node)
        self.code.function_declarations.putln("__Pyx_RefNannyDeclarations")
        self.code.before_loop.putln(
                '__Pyx_RefNannySetupContext("%s", 1);' % node.mangled_name)

    def visit_NodeWrapper(self, node):
        node = node.opaque_node
        code = create_hybrid_code(self, self.code)

        # create funcstate and evaluate the expression
        code.enter_cfunc_scope()
        node.generate_evaluation_code(code)
        if node.type.is_pyobject:
            code.put_incref(node.result(), node.type, nanny=True)
            code.put_giveref(node.result())

        # generate declarations for any temporaries
        declaration_code = CythonCCodeWriter(self.context, code.minicode)
        declaration_code.put_temp_declarations(code.funcstate)
        self.code.declaration_levels[0].putln(declaration_code.getvalue())
        self.code.putln(code.getvalue())

        return node.result()

class CCodeGenCleanup(codegen.CodeGenCleanup):
    error_handler_level = 0
    def visit_ErrorHandler(self, node):
        self.error_handler_level += 1
        super(CCodeGenCleanup, self).visit_ErrorHandler(node)
        self.error_handler_level -= 1
        if self.error_handler_level == 0:
            self.code.putln("__Pyx_RefNannyFinishContext();")
        return node

    def visit_NodeWrapper(self, node):
        code = create_hybrid_code(self, self.code)
        node.opaque_node.generate_disposal_code(code)
        self.code.putln(code.getvalue())

class Context(miniast.CContext):

    #codegen_cls = CCodeGen
    cleanup_codegen_cls = CCodeGenCleanup
    specializer_mixin_cls = CythonSpecializerMixin

    def __init__(self, astbuilder=None, typemapper=None):
        super(Context, self).__init__(astbuilder, typemapper)
        # [OperandNode]
        self.cython_operand_nodes = []

    def codegen_cls(self, _, codewriter):
        """
        Monkeypatch all OperandNodes to have a codegen attribute, so they
        can generate code for the miniast they wrap.
        """
        codegen = CCodeGen(self, codewriter)
        for node in self.cython_operand_nodes:
            node.codegen = codegen
        return codegen

    def getchildren(self, node):
        return node.child_attrs

    def declare_type(self, type):
        if type.is_typewrapper:
            return type.opaque_type.declaration_code("")

        return super(Context, self).declare_type(type)

    def may_error(self, node):
        return (node.type.resolve().is_pyobject or
                (node.type.is_memoryviewslice and node.type.dtype.is_pyobject))

class CythonCCodeWriter(Code.CCodeWriter):

    def __init__(self, context, minicode):
        super(CythonCCodeWriter, self).__init__()
        self.minicode = minicode
        self.globalstate = context.original_cython_code.globalstate

    def mark_pos(self, pos):
        pass

    def set_error_info(self, pos):
        fn_var, lineno_var, col_var = [
            self.minicode.mangle(v.name)
                for v in self.codegen.function.posinfo.variables]

        filename_idx = self.lookup_filename(pos[0])
        return '*%s = %s[%d]; *%s = %s;' % (
            fn_var, Naming.filetable_cname, filename_idx,
            lineno_var, pos[1])

    def error_goto(self, pos):
        assert self.codegen.error_handlers

        label = self.codegen.error_handlers[-1].error_label
        return "{%s goto %s;}" % (self.set_error_info(pos), label.mangled_name)

    def mangle(self, name):
        "We are simultaneously a mini-CodeWriter and a Cython-CodeWriter"
        return self.minicode.mangle(name)

class OperandNode(ExprNodes.ExprNode):
    """
    The purpose of this node is to wrap a miniast variable and dispatch
    to the miniast code generator from within the Cython code generation
    process.

    This happens when certain operations are not supported natively in
    elementwise expressions, such as operations on complex numbers or
    objects. So the miniast has a NodeWrapper wrapping a Cython AST, of
    which an OperandNode is a leaf, which has to return back again to
    the miniast code generation process.

    Summary:

        miniast
            -> cython ast
                -> operand node
                    -> miniast
    """

    subexprs = []

    def analyse_types(self, env):
        "self.type is already set"

    def generate_result_code(self, code):
        pass

    def result(self):
        return self.codegen.visit(self.variable)

class ElementalNode(ExprNodes.ExprNode):
    """
    Wraps a mapped AST.

    context: Context attribute
    operands: all participating array views
    function: miniast function wrapping the array expression

    all_contig: whether all operands are contiguous
    """

    subexprs = ['operands']

    def result(self):
        return ""

    def generate_result_code(self, code):
        function = self.function

        if self.all_contig:
            specializer = specializers.ContigSpecializer
        else:
            specializer = specializers.StridedSpecializer

        self.context.original_cython_code = code
        codes = self.context.run(function, [specializer])
        (specialized_function, codewriter, (proto, impl)), = codes
        utility = Code.UtilityCode(proto=proto, impl=impl)
        code.globalstate.use_utility_code(utility)

        if debug:
            marker =  '-' * 20
            print marker, 'proto', marker
            print proto
            print marker, 'impl', marker
            print impl

        array_type = PyrexTypes.c_array_type(PyrexTypes.c_py_ssize_t_type,
                                             function.ndim)
        shape = code.funcstate.allocate_temp(array_type, manage_ref=False)
        for i in range(function.ndim):
            code.putln("%s[%d] = 0;" % (shape, i))

        args = ["&%s[0]" % shape, "&%s" % Naming.filename_cname,
                "&%s" % Naming.lineno_cname, "NULL"]
        for operand in self.operands:
            result = operand.result()
            if operand.type.is_memoryviewslice:
                for i in range(function.ndim):
                    code.putln("if (%s.shape[%d] > %s[%d]) {" % (result, i, shape, i))
                    code.putln(    "%s[%d] = %s.shape[%d];" % (shape, i, result, i))
                    code.putln("}")

                tp = operand.type.dtype.declaration_code("")
                args.append('(%s *) %s.data' % (tp, result))
                if not self.all_contig:
                    args.append("&%s.strides[0]" % result)
            else:
                args.append(result)

        call = "%s(%s)" % (specialized_function.mangled_name, ", ".join(args))
        lbl = code.funcstate.error_label
        code.funcstate.use_label(lbl)
        code.putln("if (unlikely(%s < 0)) { goto %s; }" % (call, lbl))

        code.funcstate.release_temp(shape)

def need_wrapper_node(type):
    while True:
        if type.is_ptr:
            type = type.base_type
        elif type.is_memoryviewslice:
            type = type.dtype
        else:
            break

    type = type.resolve()
    return type.is_pyobject or type.is_complex

class ElementalMapper(specializers.ASTMapper):

    wrapping = 0

    def __init__(self, context, env):
        super(ElementalMapper, self).__init__(context)
        self.env = env
        # operands to the function in callee space
        self.operands = []
        # miniast function arguments to the function
        self.funcargs = []
        # All OperandNodes founds in the Cython AST held by a
        # miniast.NodeWrapper
        self.cython_ops = []
        self.error = False

    def map_type(self, node, **kwds):
        try:
            return super(ElementalMapper, self).map_type(node, **kwds)
        except minierror.UnmappableTypeError, e:
            error(node.pos, "Unsupported type in elementwise "
                            "operation: %s" % (node.type,))
            raise

    def get_dtype(self, type):
        if type.is_memoryviewslice:
            return type.dtype
        return type

    def register_operand(self, node):
        """
        Register a non-elemental subexpression, and pass it in to the function
        we are generating as an argument.
        """
        assert not node.is_elemental
        b = self.astbuilder

        node = node.coerce_to_simple(self.env)
        varname = '__pyx_op%d' % len(self.operands)
        self.operands.append(node)

        funcarg = b.funcarg(b.variable(self.map_type(node, wrap=True), varname))
        self.funcargs.append(funcarg)
        if self.wrapping:
            result = OperandNode(node.pos, type=self.get_dtype(node.type),
                                 variable=funcarg.variable)
            self.context.cython_operand_nodes.append(result)
            self.cython_ops.append(result)
            return result

        return funcarg.variable

    def register_wrapper_node(self, node):
        if not node.is_elemental:
            return self.register_operand(node)

        self.wrapping += 1
        self.visitchildren(node)
        self.wrapping -= 1

        if self.wrapping == 0:
            dtype = node.type
            if dtype.is_memoryviewslice:
                dtype = dtype.dtype

            node = type(node)(node.pos, type=dtype, operator=node.operator,
                              operand1=node.operand1, operand2=node.operand2)
            node.analyse_types(self.env)

            result = self.astbuilder.wrap(node, cython_ops=self.cython_ops)
            self.cython_ops = []
            return result
        else:
            return node

    def visit_ExprNode(self, node):
        return self.register_operand(node)

    def visit_SingleAssignmentNode(self, node):
        return self.astbuilder.assign(self.visit(node.lhs.dst),
                                      self.visit(node.rhs))

    def visit_BinopNode(self, node):
        minitype = self.map_type(node, wrap=True)
        if need_wrapper_node(node.type):
            return self.register_wrapper_node(node)

        op1 = self.visit(node.operand1)
        op2 = self.visit(node.operand2)
        return self.astbuilder.binop(minitype, node.operator, op1, op2)

class ElementWiseOperationsTransform(Visitor.EnvTransform):

    in_elemental = 0

    def visit_ModuleNode(self, node):
        self.minicontext = Context(typemapper=TypeMapper())
        self.funccount = 0
        self.visitchildren(node)
        return node

    def visit_elemental(self, node):
        self.in_elemental += 1
        self.visitchildren(node)
        self.in_elemental -= 1

        if not self.in_elemental:
            b = self.minicontext.astbuilder
            b.pos = node.pos
            astmapper = ElementalMapper(self.minicontext, self.current_env())
            shapevar = b.variable(minitypes.Py_ssize_t.pointer(),
                                  '__pyx_shape')
            try:
                body = astmapper.visit(node)
            except minierror.UnmappableTypeError:
                return None

            name = '__pyx_array_expression%d' % self.funccount
            self.funccount += 1

            pos_args = (
                b.variable(minitypes.c_string_type.pointer(), 'filename'),
                b.variable(minitypes.int_type.pointer(), 'lineno'),
                b.variable(minitypes.int_type.pointer(), 'column'))

            position_argument = b.funcarg(b.variable(None, 'position'),
                                          *pos_args)

            function = b.function(name, body, astmapper.funcargs, shapevar,
                                  position_argument)

            all_contig = miniutils.all(op.type.is_contig
                                           for op in astmapper.operands)
            node = ElementalNode(node.pos, operands=astmapper.operands,
                                 function=function, context=self.minicontext,
                                 all_contig=all_contig)
            node = Nodes.ExprStatNode(node.pos, expr=node)
        return node

    def visit_ExprNode(self, node):
        if node.is_elemental:
            node = self.visit_elemental(node)
        else:
            self.visitchildren(node)

        return node

    def visit_SingleAssignmentNode(self, node):
        if (isinstance(node.lhs, ExprNodes.MemoryCopySlice) and
                node.lhs.is_elemental):
            node.is_elemental = True
            return self.visit_elemental(node)

        self.visitchildren(node)
        return node
