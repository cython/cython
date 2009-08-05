from Errors import CompileError
from ExprNodes import IntNode, NoneNode, IntBinopNode, NameNode, AttributeNode
from Visitor import CythonTransform
import Options
import CythonScope
from Code import UtilityCode
from UtilityCode import CythonUtilityCode
from PyrexTypes import py_object_type, cython_memoryview_type

START_ERR = "there must be nothing or the value 0 (zero) in the start slot."
STOP_ERR = "Axis specification only allowed in the 'stop' slot."
STEP_ERR = "Only the value 1 (one) or valid axis specification allowed in the step slot."
ONE_ERR = "The value 1 (one) may appear in the first or last axis specification only."
BOTH_CF_ERR = "Cannot specify an array that is both C and Fortran contiguous."
NOT_AMP_ERR = "Invalid operator, only an ampersand '&' is allowed."
INVALID_ERR = "Invalid axis specification."
EXPR_ERR = "no expressions allowed in axis spec, only names (e.g. cython.view.contig)."
CF_ERR = "Invalid axis specification for a C/Fortran contiguous array."

memview_c_contiguous = "PyBUF_C_CONTIGUOUS"
memview_f_contiguous = "PyBUF_F_CONTIGUOUS"
memview_any_contiguous = "PyBUF_ANY_CONTIGUOUS"
memview_full_access = "PyBUF_FULL"
memview_strided_access = "PyBUF_STRIDED"

MEMVIEW_DIRECT = 1
MEMVIEW_PTR    = 2
MEMVIEW_FULL   = 4
MEMVIEW_CONTIG = 8
MEMVIEW_STRIDED= 16
MEMVIEW_FOLLOW = 32

_spec_to_const = {
        'contig' : MEMVIEW_CONTIG,
        'strided': MEMVIEW_STRIDED,
        'follow' : MEMVIEW_FOLLOW,
        'direct' : MEMVIEW_DIRECT,
        'ptr'    : MEMVIEW_PTR,
        'full'   : MEMVIEW_FULL
        }

def specs_to_code(specs):
    arr = []
    for access, packing in specs:
        arr.append("(%s | %s)" % (_spec_to_const[access], _spec_to_const[packing]))
    return arr

# XXX: add complex support below...
_typename_to_format = {
        'char' : 'c',
        'signed char' : 'b',
        'unsigned char' : 'B',
        'short' : 'h',
        'unsigned short' : 'H',
        'int' : 'i',
        'unsigned int' : 'I',
        'long' : 'l',
        'unsigned long' : 'L',
        'long long' : 'q',
        'unsigned long long' : 'Q',
        'float' : 'f',
        'double' : 'd',
        }

def format_from_type(base_type):
    return _typename_to_format[base_type.sign_and_name()]

def put_init_entry(mv_cname, code):
    code.putln("%s.data = NULL;" % mv_cname)
    code.put_init_to_py_none("%s.memview" % mv_cname, cython_memoryview_type)
    code.put_giveref("%s.memview" % mv_cname)

def put_assign_to_memview(lhs_cname, rhs_cname, memviewtype, pos, code):

    # XXX: add error checks!

    code.put_giveref("%s.memview" % (rhs_cname))
    code.put_incref("%s.memview" % (rhs_cname), py_object_type)
    code.put_gotref("%s.memview" % (lhs_cname))
    code.put_xdecref("%s.memview" % (lhs_cname), py_object_type)
    code.putln("%s.memview = %s.memview;" % (lhs_cname, rhs_cname))
    code.putln("%s.data = %s.data;" % (lhs_cname, rhs_cname))
    ndim = len(memviewtype.axes)
    for i in range(ndim):
        code.putln("%s.diminfo[%d] = %s.diminfo[%d];" % (lhs_cname, i, rhs_cname, i))

def get_buf_flag(specs):
    is_c_contig, is_f_contig = is_cf_contig(specs)

    if is_c_contig:
        return memview_c_contiguous
    elif is_f_contig:
        return memview_f_contiguous

    access, packing = zip(*specs)

    assert 'follow' not in packing

    if 'full' in access or 'ptr' in access:
        return memview_full_access
    else:
        return memview_strided_access

def use_cython_util_code(env, lu_name):
    import CythonScope
    cythonscope = env.global_scope().context.cython_scope
    viewscope = cythonscope.viewscope
    entry = viewscope.lookup_here(lu_name)
    entry.used = 1
    return entry

def use_memview_util_code(env):
    import CythonScope
    memview_entry = use_cython_util_code(env, CythonScope.memview_name)

def use_memview_cwrap(env):
    import CythonScope
    mv_cwrap_entry = use_cython_util_code(env, CythonScope.memview_cwrap_name)

def src_conforms_to_dst(src, dst):
    '''
    returns True if src conforms to dst, False otherwise.

    If conformable, the types are the same, the ndims are equal, and each axis spec is conformable.

    Any packing/access spec is conformable to itself.

    'contig' and 'follow' are conformable to 'strided'.

    'direct' and 'ptr' are conformable to 'full'.

    Any other combo is not conformable.
    '''

    if src.dtype != dst.dtype:
        return False
    if len(src.axes) != len(dst.axes):
        return False

    for src_spec, dst_spec in zip(src.axes, dst.axes):
        src_access, src_packing = src_spec
        dst_access, dst_packing = dst_spec
        if src_access != dst_access and dst_access != 'strided':
            return False
        if src_packing != dst_packing and dst_packing != 'full':
            return False

    return True


def get_axes_specs(env, axes):
    '''
    get_axes_specs(env, axes) -> list of (access, packing) specs for each axis.

    access is one of 'full', 'ptr' or 'direct'
    packing is one of 'contig', 'strided' or 'follow'
    '''

    cythonscope = env.global_scope().context.cython_scope
    viewscope = cythonscope.viewscope

    access_specs = tuple([viewscope.lookup(name)
                    for name in ('full', 'direct', 'ptr')])
    packing_specs = tuple([viewscope.lookup(name)
                    for name in ('contig', 'strided', 'follow')])

    is_f_contig, is_c_contig = False, False
    default_access, default_packing = 'direct', 'strided'
    cf_access, cf_packing = default_access, 'follow'

    # set the is_{c,f}_contig flag.
    for idx, axis in ((0,axes[0]), (-1,axes[-1])):
        if isinstance(axis.step, IntNode):
            if axis.step.compile_time_value(env) != 1:
                raise CompileError(axis.step.pos, STEP_ERR)
            if len(axes) > 1 and (is_c_contig or is_f_contig):
                raise CompileError(axis.step.pos, BOTH_CF_ERR)
            if not idx:
                is_f_contig = True
            else:
                is_c_contig = True
            if len(axes) == 1:
                break

    assert not (is_c_contig and is_f_contig)

    axes_specs = []
    # analyse all axes.
    for idx, axis in enumerate(axes):

        # start slot can be either a literal '0' or None.
        if isinstance(axis.start, IntNode):
            if axis.start.compile_time_value(env):
                raise CompileError(axis.start.pos,  START_ERR)
        elif not isinstance(axis.start, NoneNode):
            raise CompileError(axis.start.pos,  START_ERR)

        # stop slot must be None.
        if not isinstance(axis.stop, NoneNode):
            raise CompileError(axis.stop.pos, STOP_ERR)

        # step slot can be None, the value 1, 
        # a single axis spec, or an IntBinopNode.
        if isinstance(axis.step, NoneNode):
            if is_c_contig or is_f_contig:
                axes_specs.append((cf_access, cf_packing))
            else:
                axes_specs.append((default_access, default_packing))

        elif isinstance(axis.step, IntNode):
            if idx not in (0, len(axes)-1):
                raise CompileError(axis.step.pos, ONE_ERR)
            # the packing for the ::1 axis is contiguous, 
            # all others are cf_packing.
            axes_specs.append((cf_access, 'contig'))

        elif isinstance(axis.step, IntBinopNode):
            if is_c_contig or is_f_contig:
                raise CompileError(axis.step.pos, CF_ERR)
            if axis.step.operator != u'&':
                raise CompileError(axis.step.pos, NOT_AMP_ERR)
            operand1, operand2 = axis.step.operand1, axis.step.operand2
            spec1, spec2 = [_get_resolved_spec(env, op)
                    for op in (operand1, operand2)]
            if spec1 in access_specs and spec2 in packing_specs:
                axes_specs.append((spec1.name, spec2.name))
            elif spec2 in access_specs and spec1 in packing_specs:
                axes_specs.append((spec2.name, spec1.name))
            else:
                raise CompileError(axis.step.pos, INVALID_ERR)
        
        elif isinstance(axis.step, (NameNode, AttributeNode)):
            if is_c_contig or is_f_contig:
                raise CompileError(axis.step.pos, CF_ERR)
            resolved_spec = _get_resolved_spec(env, axis.step)
            if resolved_spec in access_specs:
                axes_specs.append((resolved_spec.name, default_packing))
            elif resolved_spec in packing_specs:
                axes_specs.append((default_access, resolved_spec.name))
            else:
                raise CompileError(axis.step.pos, INVALID_ERR)

        else:
            raise CompileError(axis.step.pos, INVALID_ERR)


    validate_axes_specs(axes[0].start.pos, axes_specs)

    return axes_specs

def is_cf_contig(specs):
    is_c_contig = is_f_contig = False

    packing_idx = 1

    if (specs[-1][packing_idx] == 'contig' and 
          all(axis[packing_idx] == 'follow' for axis in specs[:-1])):
        # c_contiguous: 'follow', 'follow', ..., 'follow', 'contig'
        is_c_contig = True

    elif (len(specs) > 1 and 
        specs[0][packing_idx] == 'contig' and 
        all(axis[packing_idx] == 'follow' for axis in specs[1:])):
        # f_contiguous: 'contig', 'follow', 'follow', ..., 'follow'
        is_f_contig = True

    return is_c_contig, is_f_contig

def validate_axes_specs(pos, specs):

    packing_specs = ('contig', 'strided', 'follow')
    access_specs = ('direct', 'ptr', 'full')

    is_c_contig, is_f_contig = is_cf_contig(specs)
    
    has_contig = has_follow = has_strided = False

    for access, packing in specs:

        if not (access in access_specs and
                packing in packing_specs):
            raise CompileError(pos, "Invalid axes specification.")

        if packing == 'strided':
            has_strided = True
        elif packing == 'contig':
            if has_contig:
                raise CompileError(pos, "Only one contiguous axis may be specified.")
            has_contig = True
        elif packing == 'follow':
            if has_strided:
                raise CompileError(pos, "A memoryview cannot have both follow and strided axis specifiers.")
            if not (is_c_contig or is_f_contig):
                raise CompileError(pos, "Invalid use of the follow specifier.")


def _get_resolved_spec(env, spec):
    # spec must be a NameNode or an AttributeNode
    if isinstance(spec, NameNode):
        return _resolve_NameNode(env, spec)
    elif isinstance(spec, AttributeNode):
        return _resolve_AttributeNode(env, spec)
    else:
        raise CompileError(spec.pos, INVALID_ERR)

def _resolve_NameNode(env, node):
    try:
        resolved_name = env.lookup(node.name).name
    except AttributeError:
        raise CompileError(node.pos, INVALID_ERR)
    viewscope = env.context.cython_scope.viewscope
    return viewscope.lookup(resolved_name)

def _resolve_AttributeNode(env, node):
    path = []
    while isinstance(node, AttributeNode):
        path.insert(0, node.attribute)
        node = node.obj
    if isinstance(node, NameNode):
        path.insert(0, node.name)
    else:
        raise CompileError(node.pos, EXPR_ERR)
    modnames = path[:-1]
    # must be at least 1 module name, o/w not an AttributeNode.
    assert modnames
    scope = env.lookup(modnames[0]).as_module
    for modname in modnames[1:]:
        scope = scope.lookup(modname).as_module
    return scope.lookup(path[-1])

class MemoryViewTransform(CythonTransform):

    memviews_exist = False

    def __call__(self, node):
        return super(MemoryViewTransform, self).__call__(node)

    def inspect_scope(self, node, scope):

        memviewvars = [entry for name, entry
                in scope.entries.iteritems()
                if entry.type.is_memoryview]
        if memviewvars:
            self.memviews_exist = True

    def visit_FuncDefNode(self, node):
        # check for the existence of memview entries here.
        self.inspect_scope(node, node.local_scope)
        self.visitchildren(node)
        return node

    def visit_ModuleNode(self, node):
        # check for memviews here.
        self.inspect_scope(node, node.scope)
        self.visitchildren(node)
        return node

    def visit_ClassDefNode(self, node):
        # check for memviews in the class scope
        if hasattr(node, 'scope'):
            scope = node.scope
        else:
            scope = node.entry.type.scope
        self.inspect_scope(node, scope)
        self.visitchildren(node)
        return node

    def visit_SingleAssignmentNode(self, node):
        return node

spec_constants_code = UtilityCode(proto="""
#define __Pyx_MEMVIEW_DIRECT  1
#define __Pyx_MEMVIEW_PTR     2
#define __Pyx_MEMVIEW_FULL    4
#define __Pyx_MEMVIEW_CONTIG  8
#define __Pyx_MEMVIEW_STRIDED 16
#define __Pyx_MEMVIEW_FOLLOW  32
"""
)

memviewslice_cname = u'__Pyx_memviewslice'
memviewslice_declare_code = UtilityCode(proto="""

/* memoryview slice struct */

typedef struct {
  Py_ssize_t shape, strides, suboffsets;
} __Pyx_mv_DimInfo;

typedef struct {
  struct %s *memview;
  char *data;
  __Pyx_mv_DimInfo diminfo[%d];
} %s;

""" % (CythonScope.memview_objstruct_cname,
       Options.buffer_max_dims,
       memviewslice_cname)
)
