from Cython.Compiler import ExprNodes, Nodes, PyrexTypes, Visitor, Code
from Cython.Compiler.Errors import error

from Cython.minivect import miniast
from Cython.minivect import minitypes
from Cython.minivect import miniutils
from Cython.minivect import minierror
from Cython.minivect import specializers

debug = False

class Context(miniast.CContext):
    def getpos(self, node):
        return node.pos

    def getchildren(self, node):
        return node.child_attrs

class TypeMapper(minitypes.TypeMapper):
    def map_type(self, type):
        if type.is_memoryviewslice:
            return minitypes.ArrayType(self.map_type(type.dtype),
                                       len(type.axes),
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

        raise minierror.UnmappableTypeError(type)

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
            specializer = specializers.ContigSpecializer(self.context)
        else:
            specializer = specializers.StridedSpecializer(self.context)

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

        args = ["&%s[0]" % shape]
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
        code.putln(code.error_goto_if_neg(call, self.pos))

        code.funcstate.release_temp(shape)

class ElementalMapper(specializers.ASTMapper):

    def __init__(self, context, env):
        super(ElementalMapper, self).__init__(context)
        self.env = env
        self.operands = []
        self.funcargs = []
        self.error = False

    def map_type(self, node):
        try:
            return super(ElementalMapper, self).map_type(node)
        except minierror.UnmappableTypeError, e:
            error(node.pos, "Unsupported type in elementwise "
                            "operation: %s" % (node.type,))
            self.error = True
            return minitypes.error_type

    def visit_ExprNode(self, node):
        assert not node.is_elemental
        node = node.coerce_to_simple(self.env)
        varname = '__pyx_op%d' % len(self.operands)
        self.operands.append(node)
        funcarg = self.astbuilder.funcarg(
                self.astbuilder.variable(self.map_type(node), varname))
        self.funcargs.append(funcarg)
        return funcarg.variable

    def visit_SingleAssignmentNode(self, node):
        return self.astbuilder.assign(self.visit(node.lhs.dst),
                                      self.visit(node.rhs))

    def visit_BinopNode(self, node):
        minitype = self.map_type(node)
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
            astmapper = ElementalMapper(self.minicontext, self.current_env())
            shapevar = b.variable(minitypes.Py_ssize_t.pointer(),
                                  '__pyx_shape')
            body = astmapper.visit(node)
            if astmapper.error:
                return None

            name = '__pyx_array_expression%d' % self.funccount
            self.funccount += 1
            function = b.function(name, body, astmapper.funcargs, shapevar)

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