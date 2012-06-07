import copy

from Cython.Compiler import (ExprNodes, Nodes, PyrexTypes, Visitor,
                             Code, Naming, MemoryView, Errors)
from Cython.Compiler.Errors import error, CompileError

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
        for op in node.operands:
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
        for operand in node.operands:
            operand.codegen = self

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

    codegen_cls = CCodeGen
    cleanup_codegen_cls = CCodeGenCleanup
    specializer_mixin_cls = CythonSpecializerMixin

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
        specializer_transforms = [
            specializers.ContigSpecializer,
            specializers.StridedSpecializer,
        ]

        self.context.original_cython_code = code
        codes = self.context.run(self.function, specializer_transforms)

        self.temps = []

        code.begin_block()
        # Initialize a dest_shape and broadcasting variable
        ndim = self.function.ndim
        ones = ",".join("1" for i in range(ndim))
        shape_temp = "__pyx_shape_temp"
        broadcast_temp = "__pyx_broadcasting"
        code.putln("Py_ssize_t %s[%d] = { %s };" % (shape_temp, ndim, ones))
        code.putln("int %s = 0;" % broadcast_temp)

        # broadcast all array operands
        for idx, operand in enumerate(self.operands):
            if operand.type.is_memoryviewslice:
                self.broadcast(code, shape_temp, broadcast_temp, operand, ndim)

        if_guard = "if"
        for result in codes:
            specializer = iter(result).next()
            condition = self.condition(specializer, broadcast_temp)
            if condition:
                code.putln("%s (%s) {" % (if_guard, condition))
                if_guard = " elif"
            else:
                code.putln(" else {")

            self.put_specialized_call(code, shape_temp, broadcast_temp, *result)
            code.put("}")

        code.putln("")
        code.end_block()

        for temp in self.temps:
            code.funcstate.release_temp(temp)

    def broadcast(self, code, shape_temp, broadcast_temp, operand, ndim):
        strides_temp = code.funcstate.allocate_temp(PyrexTypes.CArrayType(
            PyrexTypes.c_py_ssize_t_type, operand.type.ndim), False)
        for i in range(operand.type.ndim):
            code.putln("%s[%d] = 0;" % (strides_temp, i))

        self.temps.append(strides_temp)
        # cdef void broadcast(Py_ssize_t *dst_shape, Py_ssize_t *dst_strides,
        #                     int max_ndim, int ndim,
        #                     Py_ssize_t *input_shape, Py_ssize_t *input_strides,
        #                     bint *p_broadcast) nogil:
        code.putln("__pyx_memoryview_broadcast(&%s[0], &%s[0], "
                   "%d, %d, "
                   "&%s.shape[0], &%s.strides[0],"
                   "&%s);" %
                   (shape_temp, strides_temp,
                    ndim, operand.type.ndim,
                    operand.result(), operand.result(),
                    broadcast_temp))

    def condition(self, specializer, broadcast_temp):
        if specializer.is_contig_specializer:
            if not self.all_contig:
                # todo: implement a memoryview flag to quickly check whether
                #       it is contig for each operand
                return "0"
            return "!%s" % broadcast_temp

    def put_specialized_call(self, code, shape_temp, broadcast_temp,
                             specializer, specialized_function,
                             codewriter, result_code):
        proto, impl = result_code

        function = self.function
        ndim = function.ndim

        utility = Code.UtilityCode(proto=proto, impl=impl)
        code.globalstate.use_utility_code(utility)

        if debug:
            marker =  '-' * 20
            print marker, 'proto', marker
            print proto
            print marker, 'impl', marker
            print impl

        # all function call arguments
        args = ["&%s[0]" % shape_temp, "&%s" % Naming.filename_cname,
                "&%s" % Naming.lineno_cname, "NULL"]

        # broadcast all array operands
        for idx, operand in enumerate(self.operands):
            result = operand.result()
            if operand.type.is_memoryviewslice:
                dtype_pointer_decl = operand.type.dtype.declaration_code("")
                args.append('(%s *) %s.data' % (dtype_pointer_decl, result))
                if not specializer.is_contig_specializer:
                    args.append("&%s.strides[0]" % result)
            else:
                args.append(result)

        call = "%s(%s)" % (specialized_function.mangled_name, ", ".join(args))
        lbl = code.funcstate.error_label
        code.funcstate.use_label(lbl)
        code.putln("if (unlikely(%s < 0)) { goto %s; }" % (call, lbl))


def need_wrapper_node(type):
    """
    Return whether a Cython node that needs to be mapped to a miniast Node,
    should be mapped or wrapped (i.e., should minivect or Cython generate
    the code to evaluate the expression?).
    """
    while True:
        if type.is_ptr:
            type = type.base_type
        elif type.is_memoryviewslice:
            type = type.dtype
        else:
            break

    type = type.resolve()
    return type.is_pyobject or type.is_complex

def get_dtype(type):
    if type.is_memoryviewslice:
        return type.dtype
    return type

class CythonASTInMiniastTransform(Visitor.VisitorTransform):

    def __init__(self, env):
        super(CythonASTInMiniastTransform, self).__init__()
        self.env = env
        self.operands = []

    def visit_BinopNode(self, node):
        dtype = get_dtype(node.type)
        node = type(node)(node.pos, type=dtype, operator=node.operator,
                          operand1=self.visit(node.operand1),
                          operand2=self.visit(node.operand2))
        node.analyse_types(self.env)
        return node

    def visit_ExprNode(self, node):
        node = OperandNode(node.pos, type=get_dtype(node.type), node=node)
        self.operands.append(node)
        return node

class ElementalMapper(specializers.ASTMapper):
    """
    When some elementwise expression is found in the Cython AST, convert that
    tree to a minivect AST.
    """

    wrapping = 0

    def __init__(self, context, env):
        super(ElementalMapper, self).__init__(context)
        self.env = env
        # operands to the function in callee space
        self.operands = []
        # miniast function arguments to the function
        self.funcargs = []
        self.error = False

    def map_type(self, node, **kwds):
        try:
            return super(ElementalMapper, self).map_type(node, **kwds)
        except minierror.UnmappableTypeError, e:
            error(node.pos, "Unsupported type in elementwise "
                            "operation: %s" % (node.type,))
            raise

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

        minitype = self.map_type(node, wrap=True)
        if node.type.is_memoryviewslice:
            funcarg = b.array_funcarg(b.variable(minitype, varname))
        else:
            funcarg = b.funcarg(b.variable(minitype, varname))

        self.funcargs.append(funcarg)
        return funcarg.variable

    def register_wrapper_node(self, node):
        """
        Create a miniast.NodeWrapper for functionality that Cython provides,
        but that we want to use inside miniast expressions.
        """
        assert node.is_elemental

        transform = CythonASTInMiniastTransform(self.env)
        try:

            node = transform.visit(node)
        except CompileError, e:
            error(e.position, e.message_only)
            return None

        for operand in transform.operands:
            operand.variable = self.register_operand(operand.node)

        def specialize_node(nodewrapper, memo):
            return copy.deepcopy(node, memo)

        return self.astbuilder.wrap(node, specialize_node,
                                    operands=transform.operands)

    def visit_ExprNode(self, node):
        """
        Some expression which cannot be converted to a miniast, but is passed
        in as an argument to the function generated from the miniast.
        """
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
    """
    Find elementwise expressions and run ElementalMapper to turn it into
    a minivect AST. Our Cython tree ends here in an ElementalNode, which
    responsibility is to call the function generated by minivect (as well
    as to perform broadcasting and selection of the right specialization).
    """

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
            load_utilities(self.current_env())

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

def load_utilities(env):
    from Cython.Compiler import CythonScope
    cython_scope = CythonScope.get_cython_scope(env)
    broadcast_utility.declare_in_scope(cython_scope.viewscope,
                                       cython_scope=cython_scope, used=True)

broadcast_utility = MemoryView.load_memview_cy_utility("Broadcasting")