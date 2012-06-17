import copy

from Cython import Utils
from Cython.Compiler import (ExprNodes, Nodes, PyrexTypes, Visitor,
                             Code, Naming, MemoryView, Errors, UtilNodes)
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

        elif type.is_pyobject:
            return minitypes.object_type

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


class MemoryAllocationNode(ExprNodes.ExprNode):
    subexprs = ['size']

    def analyse_types(self, env):
        self.is_temp = True
        self.type = PyrexTypes.CPtrType(self.dtype)
        self.size.analyse_types(env)

    def generate_result_code(self, code):
        code.putln("%s = (%s) malloc(%s);" % (self.result(),
                                              self.type.declaration_code(""),
                                              self.size.result()))
        code.putln("if (!%s) {" % self.result())
        if self.in_nogil_context:
            code.put_ensure_gil()
        code.putln(    "PyErr_NoMemory();")
        if self.in_nogil_context:
            code.put_release_ensure_gil()
        code.putln(code.error_goto(self.pos))
        code.putln("}")

    def generate_disposal_code(self, code):
        code.putln("free(%s);" % self.result())
        code.putln("%s = NULL;" % self.result())

class TempSliceMemory(ExprNodes.ExprNode):
    """
    Allocate a temporary memoryview slice with contiguous strides, in the
    order of Cython/Utilities/MemoryView.pyx:get_best_order(dst).

        target   The memoryview slice which we are creating a new contiguous
                 memory region for. Must be a temp.
    """

    subexprs = ['data']

    def analyse_types(self, env):
        self.type = self.target.type
        self.dtype = self.type.dtype
        self.memsize = UtilNodes.ResultRefNode(
                    pos=self.pos, type=PyrexTypes.c_py_ssize_t_type)
        self.data = MemoryAllocationNode(self.pos, dtype=self.dtype,
                                         size=self.memsize)
        self.data.analyse_types(env)

    def generate_evaluation_code(self, code):
        "set the size of memory to allocate before we evaluate subexpressions"
        sizes = ["sizeof(%s)" % self.dtype.declaration_code("")]
        for i in range(self.type.ndim):
            sizes.append("%s.shape[%d]" % (self.result(), i))

        self.memsize.result_code = " * ".join(sizes)
        super(TempSliceMemory, self).generate_evaluation_code(code)

    def generate_result_code(self, code):
        "Copy the slice struct and compute the contiguous strides"
        code.putln("%s.data = (char *) %s;" % (self.result(),
                                               self.data.result()))
        order = "__pyx_get_best_slice_order(%s, %d)" % (self.target.result(),
                                                         self.type.ndim)
        t = (self.result(), self.result(),
             self.dtype.declaration_code(""),
             self.type.ndim, order)
        code.putln("__pyx_fill_contig_strides_array("
                   "&%s.shape[0], &%s.strides[0], sizeof(%s), %d, %s);" % t)

    def result(self):
        return self.target.result()

class CheckOverlappingMemoryNode(ExprNodes.ExprNode):
    subexprs = ['dst']

    def analyse_types(self, env):
        self.type = PyrexTypes.c_bint_type
        self.dst.analyse_types(env)
        self.is_temp = True

    def generate_result_code(self, code):
        # Check for overlapping memory
        dst = self.dst.result()
        dst_ndim = self.dst.type.ndim

        def condition(op):
            f = "__pyx_slices_overlap"
            result = "%s(%s, %s, %d, %s)" % (f, dst, op.result(),
                                             dst_ndim, op.type.ndim)
            if op.type.ndim == dst_ndim:
                f = "__pyx_read_after_write"
                overlap = "%s(%s, %s, %d)" % (f, self.dst.result(),
                                              op.result(), dst_ndim)
                result = "(%s && %s)" % (result, overlap)

            return result

        code.putln("%s = %s;" % (
            self.result(), " || ".join(condition(op) for op in self.operands)))

class BroadcastNode(ExprNodes.ExprNode):
    """
    Broadcast the given operands.
        operands:
            All operands we are broadcasting, must be temps
        result():
            Whether the operation is braodcasting in some axis
        max_ndim:
            ndim of the broadcasted operands
    """

    subexprs = []
    init_shape = True

    def analyse_types(self, env):
        self.type = PyrexTypes.c_int_type
        self.is_temp = True

    def generate_result_code(self, code):
        broadcasting = miniutils.any(op.type.ndim != self.max_ndim
                                         for op in self.operands)
        code.putln("%s = %d;" % (self.result(), broadcasting))

        if self.init_shape:
            for i in range(self.dst_slice.type.ndim):
                code.putln("%s.shape[%d] = 1;" % (self.dst_slice.result(), i))

        for operand in self.operands:
            result = operand.result()
            format_tuple = (
                "__pyx_memoryview_broadcast", self.dst_slice.result(),
                result, result, self.max_ndim, operand.type.ndim,
                self.result())
            sig = "%s(&%s.shape[0], &%s.shape[0], &%s.strides[0], %d, %d, &%s)"
            code.putln(code.error_goto_if_neg(sig % format_tuple, self.pos))

class UnbroadcastDestNode(ExprNodes.ExprNode):
    subexprs = []
    def analyse_types(self, env):
        self.type = PyrexTypes.MemoryViewSliceType(
            self.lhs.type.dtype, self.lhs.type.axes[-self.rhs.type.ndim:])
        self.is_temp = True

    def generate_result_code(self, code):
        pass

class TempSliceStruct(ExprNodes.ExprNode):
    subexprs = []
    def analyse_types(self, env):
        self.type = PyrexTypes.MemoryViewSliceType(
            self.dtype, self.axes[-self.ndim:])
        self.is_temp = True

    def generate_result_code(self, code):
        pass

class SpecializationCaller(ExprNodes.ExprNode):
    """
    Wraps a mapped AST.

    context: Context attribute
    operands: all participating array views
    function: miniast function wrapping the array expression

    During code generation:
        broadcasting: result code indicating whether the operation is
                      broadcasting
    """

    subexprs = []

    target = None

    def analyse_types(self, env):
        self.all_contig = miniutils.all(
            op.type.is_contig for op in self.operands)
        if not self.target:
            self.target = TempSliceStruct(self.pos, ndim=self.function.ndim,
                                          dtype=self.dst.type.dtype,
                                          axes=self.dst.type.axes)
            self.target.analyse_types(env)
        self.type = self.target.type

    def result(self):
        return self.target.result()

    def generate_result_code(self, code):
        specializer_transforms = [
            specializers.ContigSpecializer,
            specializers.StridedSpecializer,
        ]

        self.context.original_cython_code = code
        codes = self.context.run(self.function, specializer_transforms)

        # select specializations
        if_guard = "if"
        for result in codes:
            specializer = iter(result).next()
            condition = self.condition(specializer)
            if condition:
                code.putln("%s (%s) {" % (if_guard, condition))
                if_guard = " elif"
            else:
                code.putln(" else {")

            self.put_specialized_call(code, *result)
            code.put("}")

        code.putln("")

    def condition(self, specializer):
        if specializer.is_contig_specializer:
            if not self.all_contig:
                # todo: implement a memoryview flag to quickly check whether
                #       it is contig for each operand
                return "0"
            return "!%s" % self.broadcasting

    def put_specialized_call(self, code, specializer, specialized_function,
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
        offset = max(self.target.type.ndim - self.function.ndim, 0)
        args = ["&%s.shape[%d]" % (self.result(), offset)]

        if specialized_function.posinfo:
            args.extend(["&%s" % Naming.filename_cname,
                         "&%s" % Naming.lineno_cname,
                         "NULL"])

        for operand in [self] + self.operands:
            result = operand.result()
            if operand.type.is_memoryviewslice:
                dtype_pointer_decl = operand.type.dtype.declaration_code("")
                args.append('(%s *) %s.data' % (dtype_pointer_decl, result))
                if not specializer.is_contig_specializer:
                    offset = max(operand.type.ndim - self.function.ndim, 0)
                    args.append("&%s.strides[%d]" % (result, offset))
            else:
                args.append(result)

        call = "%s(%s)" % (specialized_function.mangled_name, ", ".join(args))

        if self.may_error:
            lbl = code.funcstate.error_label
            code.funcstate.use_label(lbl)
            code.putln("if (unlikely(%s < 0)) { goto %s; }" % (call, lbl))
        else:
            code.putln("(void) %s;" % call)

class ElementalNode(Nodes.StatNode):
    """
    Evaluate the expression on the right hand side before assigning to the
    expression on the left hand side. This is needed in two situations:

        1) The rhs has overlapping memory with the lhs, and executing the
           expression would write to memory of the lhs before it would be
           read
        2) Some error may occur while evaluating the rhs

    rhs: entire RHS expression node
    sources: list of broadcastable array operands, excluding the LHS
    may_error: indicates whether the expression may raise a sudden error
    """

    child_attrs = ['operands', 'temp_nodes', 'lhs', 'check_overlap', 'rhs',
                   'final_assignment_node', 'broadcast', 'final_broadcast',
                   'temp_dst']

    check_overlap = None
    may_error = None
    rhs = None
    rhs_target = None
    assignment_counter = 0

    def analyse_expressions(self, env):
        self.temp_nodes = []
        self.max_ndim = max(op.type.ndim for op in self.operands)

        # self.lhs is an UnbroadcastDestNode
        self.lhs = self.lhs.lhs
        self.lhs.analyse_types(env)
        self.lhs = self.lhs.coerce_to_simple(env)

        self.rhs = SpecializationCaller(
            self.operands[0].pos, context=self.minicontext,
            dst=self.lhs, operands=self.operands, function=self.rhs_function,
            may_error=self.may_error)
        self.rhs.analyse_types(env)
        self.temp_nodes.append(self.rhs.target)

        for i, operand in enumerate(self.operands):
            operand.analyse_types(env)

        self.check_overlap = CheckOverlappingMemoryNode(
                    self.pos, dst=self.lhs.wrap_in_clone_node(),
                    operands=self.operands)
        self.check_overlap.analyse_types(env)

        self.temp_dst = TempSliceMemory(self.rhs.pos, target=self.rhs)
        self.temp_dst.analyse_types(env)

        self.broadcast = BroadcastNode(self.pos,
                                       operands=self.operands,
                                       max_ndim=self.max_ndim,
                                       dst_slice=self.rhs)
        self.broadcast.analyse_types(env)

        self.final_assignment_node = self.final_assignment()
        self.final_assignment_node.analyse_types(env)
        self.temp_nodes.append(self.final_assignment_node.target)

        self.final_broadcast = BroadcastNode(
                self.pos, operands=[self.rhs], max_ndim=self.lhs.type.ndim,
                dst_slice=self.lhs, init_shape=False)
        self.final_broadcast.analyse_types(env)

    def final_assignment(self):
        b = self.minicontext.astbuilder
        typemapper = self.minicontext.typemapper

        lhs_offset, rhs_offset = self.offsets()
        self.rhs_type = PyrexTypes.MemoryViewSliceType(
            self.rhs.type.dtype, self.rhs.type.axes[rhs_offset:])

        lhs_var = b.variable(typemapper.map_type(self.lhs.type, wrap=True), 'lhs')
        rhs_var = b.variable(typemapper.map_type(self.rhs_type, wrap=True), 'rhs')

        if self.lhs.type.dtype.is_pyobject:
            body = b.assign(b.decref(lhs_var), b.incref(rhs_var))
        else:
            body = b.assign(lhs_var, rhs_var)

        args = [b.array_funcarg(lhs_var), b.array_funcarg(rhs_var)]
        func = b.function('final_assignment%d' % self.assignment_counter,
                          body, args)
        ElementalNode.assignment_counter += 1
        return SpecializationCaller(self.pos, context=self.minicontext,
                                    operands=[self.rhs], function=func,
                                    dst=self.lhs, may_error=False,
                                    target=self.lhs.wrap_in_clone_node())

    def overlap(self):
        if self.may_error:
            return "1"
        return "unlikely(%s)" % self.check_overlap.result()

    def offsets(self):
        lhs_ndim = self.lhs.type.ndim
        rhs_ndim = self.rhs.type.ndim
        lhs_offset = max(lhs_ndim - rhs_ndim, 0)
        rhs_offset = max(rhs_ndim - lhs_ndim, 0)
        return lhs_offset, rhs_offset

    def verify_final_shape(self, code):
        call = "__pyx_verify_shapes(%s, %s, %d, %d)" % (
                            self.lhs.result(), self.rhs.result(),
                            self.lhs.type.ndim, self.rhs.type.ndim)
        code.putln(code.error_goto_if_neg(call, self.pos))

    def init_rhs_temp(self, code):
        """
        In case of no overlapping memory, assign directly to the LHS.
        """
        code.putln("%s.data = %s.data;" % (self.rhs.result(), self.lhs.result()))

        lhs_offset, rhs_offset = self.offsets()
        for i in range(rhs_offset):
            code.putln("%s.strides[%d] = 0;" % (self.rhs.result(), i))

        for i in range(self.rhs.type.ndim):
            code.putln("%s.strides[%d] = %s.strides[%d];" % (
                self.rhs.result(), i + rhs_offset,
                self.lhs.result(), i + lhs_offset))

    def advance_lhs_data_ptr(self, code):
        """
        If we performed a direct assignment to the LHS, but the RHS was
        broadcasting, perform the final broadcasting assignment by advancing
        the data pointer of LHS. E.g.

            m3[:, :] = m1[:] * m2[:]

        m3[0, :] contains the data, which we need to broadcast over m3[1:, :]
        """
        lhs_offset, rhs_offset = self.offsets()
        lhs_r, rhs_r = self.lhs.result(), self.rhs.result()

        def advance(i):
            code.putln("%s.data += %s.strides[%d];" % (lhs_r, lhs_r, i))
            code.putln("%s.shape[%d] -= 1;" % (lhs_r, i))

        for i in range(lhs_offset):
            advance(i)

        for i in range(self.rhs.type.ndim):
            code.putln("if (%s.shape[%d] > 1 && %s.shape[%d] == 1) {" %
                       (lhs_r, i + lhs_offset, rhs_r, i))
            advance(i + lhs_offset)
            code.putln("}")

    def remove_rhs_offset(self, code):
        lhs_offset, rhs_offset = self.offsets()
        if rhs_offset:
            rhs_result = self.rhs.result()
            bound = self.rhs.type.ndim - rhs_offset
            i = code.funcstate.allocate_temp(PyrexTypes.c_int_type)
            t = rhs_result, i, rhs_result, i, rhs_offset
            code.putln("for (%s = 0; %s < %d; %s++) {" % (i, i, bound, i))
            code.putln(    "%s.shape[%s] = %s.shape[%s + %d];" % t)
            code.putln(    "%s.strides[%s] = %s.strides[%s + %d];" % t)
            code.putln("}")
            code.funcstate.release_temp(i)

    def generate_execution_code(self, code):
        code.mark_pos(self.pos)

        code.putln("/* LHS */")
        self.lhs.generate_evaluation_code(code)
        self.rhs.target.generate_evaluation_code(code)

        code.putln("/* Evaluate operands */")
        for op in self.operands:
            op.generate_evaluation_code(code)

        code.putln("/* Check overlapping memory */")
        self.check_overlap.generate_evaluation_code(code)

        code.putln("/* Broadcast all operands in RHS expression */")
        self.broadcast.generate_evaluation_code(code)
        self.verify_final_shape(code)

        # Set rhs.data and rhs.strides
        code.putln("/* Allocate scratch space if needed */")
        code.putln("if (%s) {" % self.overlap())
        self.temp_dst.generate_evaluation_code(code)
        code.putln("} else {")
        # shut up compiler warnings
        code.putln("%s = NULL;" % self.temp_dst.data.result())
        self.init_rhs_temp(code)
        code.putln("}")

        code.putln("/* Evaluate expression */")
        self.rhs.broadcasting = self.broadcast.result()
        self.rhs.generate_evaluation_code(code)

        code.putln("if (!%s) {" % self.overlap())
        self.advance_lhs_data_ptr(code)
        code.putln("}")

        code.putln("/* Broadcast final RHS and LHS */")
        self.final_assignment_node.target.generate_evaluation_code(code)
        self.final_broadcast.generate_evaluation_code(code)

        code.putln("/* Final broadcasting assignment */")
        if self.lhs.type.ndim == self.rhs.type.ndim:
            code.putln("if (%s) {" % self.final_broadcast.result())
        self.remove_rhs_offset(code)
        self.final_assignment_node.broadcasting = self.final_broadcast.result()
        self.final_assignment_node.generate_evaluation_code(code)
        if self.lhs.type.ndim == self.rhs.type.ndim:
            code.putln("}")

        code.putln("/* Cleanup */")
        code.putln("if (%s) {" % self.overlap())
        self.temp_dst.generate_disposal_code(code)
        self.temp_dst.free_temps(code)
        code.putln("}")

        self.dispose(code)

    def dispose(self, code):
        for child_attr in self.child_attrs:
            if child_attr == 'temp_dst':
                continue

            value_list = getattr(self, child_attr)
            if not isinstance(value_list, list):
                value_list = [value_list]

            for node in value_list:
                node.generate_disposal_code(code)
                node.free_temps(code)

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
        self.may_error = False

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

        node = node.coerce_to_temp(self.env)
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
            self.may_error = True
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
    may_error = False

    def visit_ModuleNode(self, node):
        self.minicontext = Context(typemapper=TypeMapper())
        self.funccount = 0
        self.visitchildren(node)
        return node

    def visit_elemental(self, node, lhs=None):
        self.in_elemental += 1
        self.visitchildren(node)
        self.in_elemental -= 1

        if not self.in_elemental:
            load_utilities(self.current_env())

            b = self.minicontext.astbuilder
            b.pos = node.pos
            astmapper = ElementalMapper(self.minicontext, self.current_env())

            try:
                body = astmapper.visit(node)
            except minierror.UnmappableTypeError:
                return None

            name = '__pyx_array_expression%d' % self.funccount
            self.funccount += 1

            if astmapper.may_error:
                pos_args = (
                    b.variable(minitypes.c_string_type.pointer(), 'filename'),
                    b.variable(minitypes.int_type.pointer(), 'lineno'),
                    b.variable(minitypes.int_type.pointer(), 'column'))
                posinfo = b.funcarg(b.variable(None, 'position'), *pos_args)
                self.may_error = False
            else:
                posinfo = None

            function = b.function(name, body, astmapper.funcargs,
                                  posinfo=posinfo)

            astmapper.operands.remove(lhs)
            node = ElementalNode(node.pos, operands=astmapper.operands,
                                 rhs_function=function,
                                 minicontext=self.minicontext,
                                 lhs=lhs)
            node.analyse_expressions(self.current_env())
            #node = Nodes.ExprStatNode(node.pos, expr=node)
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

            assert not self.in_elemental
            node.is_elemental = True

            node.lhs.dst = UnbroadcastDestNode(
                node.pos, lhs=node.lhs.dst.coerce_to_temp(self.current_env()),
                rhs=node.rhs)
            node.lhs.dst.analyse_types(self.current_env())
            return self.visit_elemental(node, node.lhs.dst)

        self.visitchildren(node)
        return node

def load_utilities(env):
    from Cython.Compiler import CythonScope
    cython_scope = CythonScope.get_cython_scope(env)
    broadcast_utility.declare_in_scope(cython_scope.viewscope,
                                       cython_scope=cython_scope, used=True)

    env.use_utility_code(overlap_utility)

broadcast_utility = MemoryView.load_memview_cy_utility(
                "Broadcasting", context=MemoryView.context)
MemoryView.view_utility_code.requires.append(broadcast_utility)
overlap_utility = MemoryView.load_memview_c_utility(
        "ReadAfterWrite", context=MemoryView.context)
        #proto_block='utility_code_proto_before_types')