from Errors import CompileError
from ExprNodes import IntNode, NoneNode, IntBinopNode, NameNode, AttributeNode
from Visitor import CythonTransform
import Options
import CythonScope
from Code import UtilityCode
from UtilityCode import CythonUtilityCode
from PyrexTypes import py_object_type, cython_memoryview_ptr_type

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

def put_init_entry(mv_cname, code):
    code.putln("%s.data = NULL;" % mv_cname)
    code.putln("%s.memview = NULL;" % mv_cname)

def mangle_dtype_name(dtype):
    # a dumb wrapper for now; move Buffer.mangle_dtype_name in here later?
    import Buffer
    return Buffer.mangle_dtype_name(dtype)

def axes_to_str(axes):
    return "".join([access[0].upper()+packing[0] for (access, packing) in axes])

def gen_acquire_memoryviewslice(rhs, lhs_type, lhs_is_cglobal, lhs_result, lhs_pos, code):
    # import MemoryView
    assert rhs.type.is_memoryviewslice

    pretty_rhs = isinstance(rhs, NameNode) or rhs.result_in_temp()
    if pretty_rhs:
        rhstmp = rhs.result()
    else:
        rhstmp = code.funcstate.allocate_temp(lhs_type, manage_ref=False)
        code.putln("%s = %s;" % (rhstmp, rhs.result_as(lhs_type)))
        code.putln(code.error_goto_if_null("%s.memview" % rhstmp, lhs_pos))

    if not rhs.result_in_temp():
        code.put_incref("%s.memview" % rhstmp, cython_memoryview_ptr_type)

    if lhs_is_cglobal:
        code.put_gotref("%s.memview" % lhs_result)

    #XXX: this is here because self.lhs_of_first_assignment is not set correctly,
    #     once that is working this should take that flag into account.
    #     See NameNode.generate_assignment_code
    code.put_xdecref("%s.memview" % lhs_result, cython_memoryview_ptr_type)

    if lhs_is_cglobal:
        code.put_giveref("%s.memview" % rhstmp)

    put_assign_to_memviewslice(lhs_result, rhstmp, lhs_type,
                                     lhs_pos, code=code)

    if rhs.result_in_temp() or not pretty_rhs:
        code.putln("%s.memview = 0;" % rhstmp)

    if not pretty_rhs:
        code.funcstate.release_temp(rhstmp)

def put_assign_to_memviewslice(lhs_cname, rhs_cname, memviewslicetype, pos, code):

    code.putln("%s.memview = %s.memview;" % (lhs_cname, rhs_cname))
    code.putln("%s.data = %s.data;" % (lhs_cname, rhs_cname))
    ndim = len(memviewslicetype.axes)
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

def use_cython_view_util_code(env, lu_name):
    import CythonScope
    cythonscope = env.global_scope().context.cython_scope
    viewscope = cythonscope.viewscope
    entry = viewscope.lookup_here(lu_name)
    entry.used = 1
    return entry

def use_cython_util_code(env, lu_name):
    import CythonScope
    cythonscope = env.global_scope().context.cython_scope
    entry = cythonscope.lookup_here(lu_name)
    entry.used = 1
    return entry

def use_memview_util_code(env):
    import CythonScope
    return use_cython_view_util_code(env, CythonScope.memview_name)

def use_memview_cwrap(env):
    import CythonScope
    return use_cython_view_util_code(env, CythonScope.memview_cwrap_name)

def use_cython_array(env):
    return use_cython_util_code(env, 'array')

def src_conforms_to_dst(src, dst):
    '''
    returns True if src conforms to dst, False otherwise.

    If conformable, the types are the same, the ndims are equal, and each axis spec is conformable.

    Any packing/access spec is conformable to itself.

    'direct' and 'ptr' are conformable to 'full'.
    'contig' and 'follow' are conformable to 'strided'.
    Any other combo is not conformable.
    '''

    if src.dtype != dst.dtype:
        return False
    if len(src.axes) != len(dst.axes):
        return False

    for src_spec, dst_spec in zip(src.axes, dst.axes):
        src_access, src_packing = src_spec
        dst_access, dst_packing = dst_spec
        if src_access != dst_access and dst_access != 'full':
            return False
        if src_packing != dst_packing and dst_packing != 'strided':
            return False

    return True

def get_copy_contents_name(from_mvs, to_mvs):
    dtype = from_mvs.dtype
    assert dtype == to_mvs.dtype
    return ('__Pyx_BufferCopyContents_%s_%s_%s' %
            (axes_to_str(from_mvs.axes),
             axes_to_str(to_mvs.axes),
             mangle_dtype_name(dtype)))


copy_template = '''
static __Pyx_memviewslice %(copy_name)s(const __Pyx_memviewslice from_mvs) {

    int i;
    __Pyx_memviewslice new_mvs = {0, 0};
    struct __pyx_obj_memoryview *from_memview = from_mvs.memview;
    Py_buffer *buf = &from_memview->view;
    PyObject *shape_tuple = 0;
    PyObject *temp_int = 0;
    struct __pyx_obj_array *array_obj = 0;
    struct __pyx_obj_memoryview *memview_obj = 0;
    char mode[] = "%(mode)s";

    __Pyx_SetupRefcountContext("%(copy_name)s");

    shape_tuple = PyTuple_New((Py_ssize_t)(buf->ndim));
    if(unlikely(!shape_tuple)) {
        goto fail;
    }
    __Pyx_GOTREF(shape_tuple);


    for(i=0; i<buf->ndim; i++) {
        temp_int = PyInt_FromLong(buf->shape[i]);
        if(unlikely(!temp_int)) {
            goto fail;
        } else {
            PyTuple_SET_ITEM(shape_tuple, i, temp_int);
        }
    }

    array_obj = __pyx_cythonarray_array_cwrapper(shape_tuple, %(sizeof_dtype)s, buf->format, mode);
    if (unlikely(!array_obj)) {
        goto fail;
    }
    __Pyx_GOTREF(array_obj);

    memview_obj = __pyx_viewaxis_memoryview_cwrapper((PyObject *)array_obj, %(contig_flag)s);
    if (unlikely(!memview_obj)) {
        goto fail;
    }

    /* initialize new_mvs */
    if (unlikely(-1 == __Pyx_init_memviewslice(memview_obj, buf->ndim, &new_mvs))) {
        PyErr_SetString(PyExc_RuntimeError,
            "Could not initialize new memoryviewslice object.");
        goto fail;
    }

    if (unlikely(-1 == %(copy_contents_name)s(&from_mvs, &new_mvs))) {
        /* PyErr_SetString(PyExc_RuntimeError,
            "Could not copy contents of memoryview slice."); */
        goto fail;
    }

    goto no_fail;

fail:
    __Pyx_XDECREF(new_mvs.memview); new_mvs.memview = 0;
    new_mvs.data = 0;
no_fail:
    __Pyx_XDECREF(shape_tuple); shape_tuple = 0;
    __Pyx_GOTREF(temp_int);
    __Pyx_XDECREF(temp_int); temp_int = 0;
    __Pyx_XDECREF(array_obj); array_obj = 0;
    __Pyx_FinishRefcountContext();
    return new_mvs;

}
'''

def get_copy_contents_code(from_mvs, to_mvs, cfunc_name):
    assert from_mvs.dtype == to_mvs.dtype
    assert len(from_mvs.axes) == len(to_mvs.axes)

    ndim = len(from_mvs.axes)

    # XXX: we only support direct access for now.
    for (access, packing) in from_mvs.axes:
        if access != 'direct':
            raise NotImplementedError("only direct access supported currently.")

    code = '''

static int %(cfunc_name)s(const __Pyx_memviewslice *from_mvs, __Pyx_memviewslice *to_mvs) {

    char *to_buf = (char *)to_mvs->data;
    char *from_buf = (char *)from_mvs->data;
    struct __pyx_obj_memoryview *temp_memview = 0;
    char *temp_data = 0;

''' % {'cfunc_name' : cfunc_name}

    if to_mvs.is_c_contig:
        start, stop, step = 0, ndim, 1
    elif to_mvs.is_f_contig:
        start, stop, step = ndim-1, -1, -1
    else:
        assert False

    INDENT = "    "

    for i, idx in enumerate(range(start, stop, step)):
        # the crazy indexing is to account for the fortran indexing.
        # 'i' always goes up from zero to ndim-1.
        # 'idx' is the same as 'i' for c_contig, and goes from ndim-1 to 0 for f_contig.
        # this makes the loop code below identical in both cases.
        code += INDENT+"Py_ssize_t i%d = 0, idx%d = 0;\n" % (i,i)
        code += INDENT+"Py_ssize_t stride%(i)d = from_mvs->diminfo[%(idx)d].strides;\n" % {'i':i, 'idx':idx}
        code += INDENT+"Py_ssize_t shape%(i)d = from_mvs->diminfo[%(idx)d].shape;\n" % {'i':i, 'idx':idx}

    code += "\n"

    # put down the nested for-loop.
    for k in range(ndim):

        code += INDENT*(k+1) + "for(i%(k)d=0; i%(k)d<shape%(k)d; i%(k)d++) {\n" % {'k' : k}
        if k >= 1:
            code += INDENT*(k+2) + "idx%(k)d = i%(k)d * stride%(k)d + idx%(km1)d;\n" % {'k' : k, 'km1' : k-1}
        else:
            code += INDENT*(k+2) + "idx%(k)d = i%(k)d * stride%(k)d;\n" % {'k' : k}

    # the inner part of the loop.
    dtype_decl = from_mvs.dtype.declaration_code("")
    last_idx = ndim-1
    code += INDENT*ndim+"memcpy(to_buf, from_buf+idx%(last_idx)d, sizeof(%(dtype_decl)s));\n" % locals()
    code += INDENT*ndim+"to_buf += sizeof(%(dtype_decl)s);\n" % locals()

    # for-loop closing braces
    for k in range(ndim-1, -1, -1):
        code += INDENT*(k+1)+"}\n"

    # init to_mvs->data and to_mvs->diminfo.
    code += INDENT+"temp_memview = to_mvs->memview;\n"
    code += INDENT+"temp_data = to_mvs->data;\n"
    code += INDENT+"to_mvs->memview = 0; to_mvs->data = 0;\n"
    code += INDENT+"if(unlikely(-1 == __Pyx_init_memviewslice(temp_memview, %d, to_mvs))) {\n" % (ndim,)
    code += INDENT*2+"return -1;\n"
    code +=   INDENT+"}\n"

    code += INDENT + "return 0;\n"

    code += '}\n'

    return code

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

    if (len(specs) == 1 and specs == [('direct', 'contig')]):
        is_c_contig = True

    elif (specs[-1] == ('direct','contig') and 
          all(axis == ('direct','follow') for axis in specs[:-1])):
        # c_contiguous: 'follow', 'follow', ..., 'follow', 'contig'
        is_c_contig = True

    elif (len(specs) > 1 and 
        specs[0] == ('direct','contig') and 
        all(axis == ('direct','follow') for axis in specs[1:])):
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
    viewscope = env.global_scope().context.cython_scope.viewscope
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

class MemoryViewSliceTransform(CythonTransform):

    memviews_exist = False

    def __call__(self, node):
        return super(MemoryViewSliceTransform, self).__call__(node)

    def inspect_scope(self, node, scope):

        memviewvars = [entry for name, entry
                in scope.entries.iteritems()
                if entry.type.is_memoryviewslice]
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

memviewslice_init_code = UtilityCode(proto="""\

#define __Pyx_BUF_MAX_NDIMS %(BUF_MAX_NDIMS)d

#define __Pyx_MEMVIEW_DIRECT   1
#define __Pyx_MEMVIEW_PTR      2
#define __Pyx_MEMVIEW_FULL     4
#define __Pyx_MEMVIEW_CONTIG   8
#define __Pyx_MEMVIEW_STRIDED  16
#define __Pyx_MEMVIEW_FOLLOW   32

#define __Pyx_IS_C_CONTIG 1
#define __Pyx_IS_F_CONTIG 2

static int __Pyx_ValidateAndInit_memviewslice(struct __pyx_obj_memoryview *memview, 
                                int *axes_specs, int c_or_f_flag,  int ndim, __Pyx_TypeInfo *dtype,
                                __Pyx_BufFmt_StackElem stack[], __Pyx_memviewslice *memviewslice);

static int __Pyx_init_memviewslice(
                struct __pyx_obj_memoryview *memview,
                int ndim,
                __Pyx_memviewslice *memviewslice);
""" % {'BUF_MAX_NDIMS' :Options.buffer_max_dims},
impl = """\
static int __Pyx_ValidateAndInit_memviewslice(
                struct __pyx_obj_memoryview *memview,
                int *axes_specs,
                int c_or_f_flag,
                int ndim,
                __Pyx_TypeInfo *dtype, 
                __Pyx_BufFmt_StackElem stack[],
                __Pyx_memviewslice *memviewslice) {

    __Pyx_SetupRefcountContext("ValidateAndInit_memviewslice");
    Py_buffer *buf = &memview->view;
    int stride, i, spec = 0, retval = -1;

    if (!buf) goto fail;

    if(memviewslice->data || memviewslice->memview) {
        PyErr_SetString(PyExc_ValueError,
            "memoryviewslice struct must be initialized to NULL.");
        goto fail;
    }

    if (buf->ndim != ndim) {
        PyErr_Format(PyExc_ValueError,
                "Buffer has wrong number of dimensions (expected %d, got %d)",
                ndim, buf->ndim);
        goto fail;
    }

    __Pyx_BufFmt_Context ctx;
    __Pyx_BufFmt_Init(&ctx, stack, dtype);
    if (!__Pyx_BufFmt_CheckString(&ctx, buf->format)) goto fail;

    if ((unsigned)buf->itemsize != dtype->size) {
        PyErr_Format(PyExc_ValueError,
          "Item size of buffer (%"PY_FORMAT_SIZE_T"d byte%s) does not match size of '%s' (%"PY_FORMAT_SIZE_T"d byte%s)",
          buf->itemsize, (buf->itemsize > 1) ? "s" : "",
          dtype->name,
          dtype->size, (dtype->size > 1) ? "s" : "");
        goto fail;
    }

    if (!buf->strides) {
        PyErr_SetString(PyExc_ValueError,
            "buffer does not supply strides necessary for memoryview.");
        goto fail;
    }

    for(i=0; i<ndim; i++) {
        spec = axes_specs[i];
        if (spec & __Pyx_MEMVIEW_CONTIG) {
            if (buf->strides[i] != buf->itemsize) {
                PyErr_SetString(PyExc_ValueError,
                    "Buffer and memoryview are not contiguous in the same dimension.");
                goto fail;
            }
        }

        if (spec & (__Pyx_MEMVIEW_STRIDED | __Pyx_MEMVIEW_FOLLOW)) {
            if (buf->strides[i] <= buf->itemsize) {
                PyErr_SetString(PyExc_ValueError,
                    "Buffer and memoryview are not contiguous in the same dimension.");
                goto fail;
            }
        }

        if (spec & __Pyx_MEMVIEW_DIRECT) {
            if (buf->suboffsets && buf->suboffsets[i] >= 0) {
                PyErr_SetString(PyExc_ValueError,
                    "Buffer not compatible with direct access.");
                goto fail;
            }
        }

        if (spec & (__Pyx_MEMVIEW_PTR | __Pyx_MEMVIEW_FULL)) {
            if (!buf->suboffsets) {
                PyErr_SetString(PyExc_ValueError,
                    "Buffer not able to be indirectly accessed.");
                goto fail;
            }
        }

        if (spec & __Pyx_MEMVIEW_PTR) {
            if (buf->suboffsets[i] < 0) {
                PyErr_Format(PyExc_ValueError,
                    "Buffer not indirectly accessed in %d dimension, although memoryview is.", i);
                goto fail;
            }
        }
    }

    if (c_or_f_flag & __Pyx_IS_F_CONTIG) {
        stride = 1;
        for(i=0; i<ndim; i++) {
            if(stride * buf->itemsize != buf->strides[i]) {
                PyErr_SetString(PyExc_ValueError,
                    "Buffer not fortran contiguous.");
                goto fail;
            }
            stride = stride * buf->shape[i];
        }
    } else if (c_or_f_flag & __Pyx_IS_F_CONTIG) {
        for(i=ndim-1; i>-1; i--) {
            if(stride * buf->itemsize != buf->strides[i]) {
                PyErr_SetString(PyExc_ValueError,
                    "Buffer not C contiguous.");
                goto fail;
            }
            stride = stride * buf->shape[i];
        }
    }

    if(unlikely(__Pyx_init_memviewslice(memview, ndim, memviewslice) == -1)) {
        goto fail;
    }

    retval = 0;
    goto no_fail;
fail:
    __Pyx_XDECREF(memviewslice->memview);
    memviewslice->memview = 0;
    memviewslice->data = 0;
    retval = -1;

no_fail:
    __Pyx_FinishRefcountContext();
    return retval;
}

static int __Pyx_init_memviewslice(
                struct __pyx_obj_memoryview *memview,
                int ndim,
                __Pyx_memviewslice *memviewslice) {
    
    __Pyx_SetupRefcountContext("init_memviewslice");
    int i, retval=-1;
    Py_buffer *buf = &memview->view;

    if(!buf) {
        PyErr_SetString(PyExc_ValueError,
            "buf is NULL.");
        goto fail;
    } else if(memviewslice->memview || memviewslice->data) {
        PyErr_SetString(PyExc_ValueError,
            "memviewslice is already initialized!");
        goto fail;
    }

    for(i=0; i<ndim; i++) {
        memviewslice->diminfo[i].strides = buf->strides[i];
        memviewslice->diminfo[i].shape   = buf->shape[i];
        if(buf->suboffsets) {
            memviewslice->diminfo[i].suboffsets = buf->suboffsets[i];
        }
    }

    __Pyx_INCREF((PyObject *)memview);
    __Pyx_GIVEREF((PyObject *)memview);
    memviewslice->memview = memview;
    memviewslice->data = (char *)buf->buf;
    retval = 0;
    goto no_fail;

fail:
    __Pyx_XDECREF(memviewslice->memview);
    memviewslice->memview = 0;
    memviewslice->data = 0;
    retval = -1;
no_fail:
    __Pyx_FinishRefcountContext();
    return retval;
}
""")

memviewslice_init_code.requires = [memviewslice_declare_code]

