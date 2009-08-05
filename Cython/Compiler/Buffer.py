from Visitor import VisitorTransform, CythonTransform
from ModuleNode import ModuleNode
from Nodes import *
from ExprNodes import *
from StringEncoding import EncodedString
from Errors import CompileError
from UtilityCode import CythonUtilityCode
from Code import UtilityCode
import Cython.Compiler.Options
import Interpreter
import PyrexTypes
import Naming
import Symtab

import textwrap

def dedent(text, reindent=0):
    text = textwrap.dedent(text)
    if reindent > 0:
        indent = " " * reindent
        text = '\n'.join([indent + x for x in text.split('\n')])
    return text

class IntroduceBufferAuxiliaryVars(CythonTransform):

    #
    # Entry point
    #

    buffers_exists = False
    using_memoryview = False

    def __call__(self, node):
        assert isinstance(node, ModuleNode)
        self.max_ndim = 0
        result = super(IntroduceBufferAuxiliaryVars, self).__call__(node)
        if self.buffers_exists or self.using_memoryview:
            use_bufstruct_declare_code(node.scope)
            use_py2_buffer_functions(node.scope)
            use_empty_bufstruct_code(node.scope, self.max_ndim)
        return result


    #
    # Basic operations for transforms
    #
    def handle_scope(self, node, scope):
        # For all buffers, insert extra variables in the scope.
        # The variables are also accessible from the buffer_info
        # on the buffer entry
        bufvars = [entry for name, entry
                   in scope.entries.iteritems()
                   if entry.type.is_buffer]
        if len(bufvars) > 0:
            self.buffers_exists = True

        memviewslicevars = [entry for name, entry
                in scope.entries.iteritems()
                if entry.type.is_memoryviewslice]
        if len(memviewslicevars) > 0:
            self.buffers_exists = True


        for (name, entry) in scope.entries.iteritems():
            if name == 'memoryview' and isinstance(entry.utility_code_definition, CythonUtilityCode):
                self.using_memoryview = True
                break


        if isinstance(node, ModuleNode) and len(bufvars) > 0:
            # for now...note that pos is wrong
            raise CompileError(node.pos, "Buffer vars not allowed in module scope")
        for entry in bufvars:
            if entry.type.dtype.is_ptr:
                raise CompileError(node.pos, "Buffers with pointer types not yet supported.")

            name = entry.name
            buftype = entry.type
            if buftype.ndim > Options.buffer_max_dims:
                raise CompileError(node.pos,
                        "Buffer ndims exceeds Options.buffer_max_dims = %d" % Options.buffer_max_dims)
            if buftype.ndim > self.max_ndim:
                self.max_ndim = buftype.ndim

            # Declare auxiliary vars
            def decvar(type, prefix):
                cname = scope.mangle(prefix, name)
                aux_var = scope.declare_var(name="$%s" % cname, cname=cname,
                                            type=type, pos=node.pos)
                if entry.is_arg:
                    aux_var.used = True # otherwise, NameNode will mark whether it is used

                return aux_var

            auxvars = ((PyrexTypes.c_pyx_buffer_nd_type, Naming.pybuffernd_prefix),
                      (PyrexTypes.c_pyx_buffer_type, Naming.pybufferstruct_prefix))
            pybuffernd, rcbuffer = [decvar(type, prefix) for (type, prefix) in auxvars]

            entry.buffer_aux = Symtab.BufferAux(pybuffernd, rcbuffer)

        scope.buffer_entries = bufvars
        self.scope = scope

    def visit_ModuleNode(self, node):
        self.handle_scope(node, node.scope)
        self.visitchildren(node)
        return node

    def visit_FuncDefNode(self, node):
        self.handle_scope(node, node.local_scope)
        self.visitchildren(node)
        return node

#
# Analysis
#
buffer_options = ("dtype", "ndim", "mode", "negative_indices", "cast") # ordered!
buffer_defaults = {"ndim": 1, "mode": "full", "negative_indices": True, "cast": False}
buffer_positional_options_count = 1 # anything beyond this needs keyword argument

ERR_BUF_OPTION_UNKNOWN = '"%s" is not a buffer option'
ERR_BUF_TOO_MANY = 'Too many buffer options'
ERR_BUF_DUP = '"%s" buffer option already supplied'
ERR_BUF_MISSING = '"%s" missing'
ERR_BUF_MODE = 'Only allowed buffer modes are: "c", "fortran", "full", "strided" (as a compile-time string)'
ERR_BUF_NDIM = 'ndim must be a non-negative integer'
ERR_BUF_DTYPE = 'dtype must be "object", numeric type or a struct'
ERR_BUF_BOOL = '"%s" must be a boolean'

def analyse_buffer_options(globalpos, env, posargs, dictargs, defaults=None, need_complete=True):
    """
    Must be called during type analysis, as analyse is called
    on the dtype argument.

    posargs and dictargs should consist of a list and a dict
    of tuples (value, pos). Defaults should be a dict of values.

    Returns a dict containing all the options a buffer can have and
    its value (with the positions stripped).
    """
    if defaults is None:
        defaults = buffer_defaults

    posargs, dictargs = Interpreter.interpret_compiletime_options(posargs, dictargs, type_env=env, type_args = (0,'dtype'))

    if len(posargs) > buffer_positional_options_count:
        raise CompileError(posargs[-1][1], ERR_BUF_TOO_MANY)

    options = {}
    for name, (value, pos) in dictargs.iteritems():
        if not name in buffer_options:
            raise CompileError(pos, ERR_BUF_OPTION_UNKNOWN % name)
        options[name] = value

    for name, (value, pos) in zip(buffer_options, posargs):
        if not name in buffer_options:
            raise CompileError(pos, ERR_BUF_OPTION_UNKNOWN % name)
        if name in options:
            raise CompileError(pos, ERR_BUF_DUP % name)
        options[name] = value

    # Check that they are all there and copy defaults
    for name in buffer_options:
        if not name in options:
            try:
                options[name] = defaults[name]
            except KeyError:
                if need_complete:
                    raise CompileError(globalpos, ERR_BUF_MISSING % name)

    dtype = options.get("dtype")
    if dtype and dtype.is_extension_type:
        raise CompileError(globalpos, ERR_BUF_DTYPE)

    ndim = options.get("ndim")
    if ndim and (not isinstance(ndim, int) or ndim < 0):
        raise CompileError(globalpos, ERR_BUF_NDIM)

    mode = options.get("mode")
    if mode and not (mode in ('full', 'strided', 'c', 'fortran')):
        raise CompileError(globalpos, ERR_BUF_MODE)

    def assert_bool(name):
        x = options.get(name)
        if not isinstance(x, bool):
            raise CompileError(globalpos, ERR_BUF_BOOL % name)

    assert_bool('negative_indices')
    assert_bool('cast')

    return options


#
# Code generation
#

def get_buf_suboffsetvars(entry):
    return [("%s.diminfo[%d].suboffsets" % \
            (entry.buffer_aux.buflocal_nd_var.cname, i)) for i in range(entry.type.ndim)]
def get_buf_stridevars(entry):
    return [("%s.diminfo[%d].strides" % \
            (entry.buffer_aux.buflocal_nd_var.cname, i)) for i in range(entry.type.ndim)]
def get_buf_shapevars(entry):
    return [("%s.diminfo[%d].shape" % \
            (entry.buffer_aux.buflocal_nd_var.cname, i)) for i in range(entry.type.ndim)]

def get_flags(buffer_aux, buffer_type):
    flags = 'PyBUF_FORMAT'
    mode = buffer_type.mode
    if mode == 'full':
        flags += '| PyBUF_INDIRECT'
    elif mode == 'strided':
        flags += '| PyBUF_STRIDES'
    elif mode == 'c':
        flags += '| PyBUF_C_CONTIGUOUS'
    elif mode == 'fortran':
        flags += '| PyBUF_F_CONTIGUOUS'
    else:
        assert False
    if buffer_aux.writable_needed: flags += "| PyBUF_WRITABLE"
    return flags

def used_buffer_aux_vars(entry):
    buffer_aux = entry.buffer_aux
    buffer_aux.buflocal_nd_var.used = True
    buffer_aux.rcbuf_var.used = True

def put_unpack_buffer_aux_into_scope(buf_entry, code):
    # Generate code to copy the needed struct info into local
    # variables.
    buffer_aux, mode = buf_entry.buffer_aux, buf_entry.type.mode
    pybuffernd_struct = buffer_aux.buflocal_nd_var.cname

    fldnames = ['strides', 'shape']
    if mode == 'full':
        fldnames.append('suboffsets')

    ln = []
    for i in range(buf_entry.type.ndim):
        for fldname in fldnames:
            ln.append("%s.diminfo[%d].%s = %s.rcbuffer->pybuffer.%s[%d];" % \
                    (pybuffernd_struct, i, fldname,
                     pybuffernd_struct, fldname, i))
    code.putln(' '.join(ln))

def put_init_vars(entry, code):
    bufaux = entry.buffer_aux
    pybuffernd_struct = bufaux.buflocal_nd_var.cname
    pybuffer_struct = bufaux.rcbuf_var.cname
    # init pybuffer_struct
    code.putln("%s.pybuffer.buf = NULL;" % pybuffer_struct)
    code.putln("%s.refcount = 0;" % pybuffer_struct)
    # init the buffer object
    # code.put_init_var_to_py_none(entry)
    # init the pybuffernd_struct
    code.putln("%s.data = NULL;" % pybuffernd_struct)
    code.putln("%s.rcbuffer = &%s;" % (pybuffernd_struct, pybuffer_struct))

def put_acquire_arg_buffer(entry, code, pos):
    code.globalstate.use_utility_code(acquire_utility_code)
    buffer_aux = entry.buffer_aux
    getbuffer = get_getbuffer_call(code, entry.cname, buffer_aux, entry.type)

    # Acquire any new buffer
    code.putln("{")
    code.putln("__Pyx_BufFmt_StackElem __pyx_stack[%d];" % entry.type.dtype.struct_nesting_depth())
    code.putln(code.error_goto_if("%s == -1" % getbuffer, pos))
    code.putln("}")
    # An exception raised in arg parsing cannot be catched, so no
    # need to care about the buffer then.
    put_unpack_buffer_aux_into_scope(entry, code)

def put_release_buffer_code(code, entry):
    code.globalstate.use_utility_code(acquire_utility_code)
    code.putln("__Pyx_SafeReleaseBuffer(&%s.rcbuffer->pybuffer);" % entry.buffer_aux.buflocal_nd_var.cname)

def get_getbuffer_call(code, obj_cname, buffer_aux, buffer_type):
    ndim = buffer_type.ndim
    cast = int(buffer_type.cast)
    flags = get_flags(buffer_aux, buffer_type)
    pybuffernd_struct = buffer_aux.buflocal_nd_var.cname

    dtype_typeinfo = get_type_information_cname(code, buffer_type.dtype)

    return ("__Pyx_GetBufferAndValidate(&%(pybuffernd_struct)s.rcbuffer->pybuffer, "
            "(PyObject*)%(obj_cname)s, &%(dtype_typeinfo)s, %(flags)s, %(ndim)d, "
            "%(cast)d, __pyx_stack)" % locals())

def put_assign_to_buffer(lhs_cname, rhs_cname, buf_entry,
                         is_initialized, pos, code):
    """
    Generate code for reassigning a buffer variables. This only deals with getting
    the buffer auxiliary structure and variables set up correctly, the assignment
    itself and refcounting is the responsibility of the caller.

    However, the assignment operation may throw an exception so that the reassignment
    never happens.

    Depending on the circumstances there are two possible outcomes:
    - Old buffer released, new acquired, rhs assigned to lhs
    - Old buffer released, new acquired which fails, reaqcuire old lhs buffer
      (which may or may not succeed).
    """

    buffer_aux, buffer_type = buf_entry.buffer_aux, buf_entry.type
    code.globalstate.use_utility_code(acquire_utility_code)
    pybuffernd_struct = buffer_aux.buflocal_nd_var.cname
    flags = get_flags(buffer_aux, buffer_type)

    code.putln("{")  # Set up necesarry stack for getbuffer
    code.putln("__Pyx_BufFmt_StackElem __pyx_stack[%d];" % buffer_type.dtype.struct_nesting_depth())

    getbuffer = get_getbuffer_call(code, "%s", buffer_aux, buffer_type) # fill in object below

    if is_initialized:
        # Release any existing buffer
        code.putln('__Pyx_SafeReleaseBuffer(&%s.rcbuffer->pybuffer);' % pybuffernd_struct)
        # Acquire
        retcode_cname = code.funcstate.allocate_temp(PyrexTypes.c_int_type, manage_ref=False)
        code.putln("%s = %s;" % (retcode_cname, getbuffer % rhs_cname))
        code.putln('if (%s) {' % (code.unlikely("%s < 0" % retcode_cname)))
        # If acquisition failed, attempt to reacquire the old buffer
        # before raising the exception. A failure of reacquisition
        # will cause the reacquisition exception to be reported, one
        # can consider working around this later.
        type, value, tb = [code.funcstate.allocate_temp(PyrexTypes.py_object_type, manage_ref=False)
                           for i in range(3)]
        code.putln('PyErr_Fetch(&%s, &%s, &%s);' % (type, value, tb))
        code.putln('if (%s) {' % code.unlikely("%s == -1" % (getbuffer % lhs_cname)))
        code.putln('Py_XDECREF(%s); Py_XDECREF(%s); Py_XDECREF(%s);' % (type, value, tb)) # Do not refnanny these!
        code.globalstate.use_utility_code(raise_buffer_fallback_code)
        code.putln('__Pyx_RaiseBufferFallbackError();')
        code.putln('} else {')
        code.putln('PyErr_Restore(%s, %s, %s);' % (type, value, tb))
        for t in (type, value, tb):
            code.funcstate.release_temp(t)
        code.putln('}')
        code.putln('}')
        # Unpack indices
        put_unpack_buffer_aux_into_scope(buf_entry, code)
        code.putln(code.error_goto_if_neg(retcode_cname, pos))
        code.funcstate.release_temp(retcode_cname)
    else:
        # Our entry had no previous value, so set to None when acquisition fails.
        # In this case, auxiliary vars should be set up right in initialization to a zero-buffer,
        # so it suffices to set the buf field to NULL.
        code.putln('if (%s) {' % code.unlikely("%s == -1" % (getbuffer % rhs_cname)))
        code.putln('%s = %s; __Pyx_INCREF(Py_None); %s.rcbuffer->pybuffer.buf = NULL;' %
                   (lhs_cname,
                    PyrexTypes.typecast(buffer_type, PyrexTypes.py_object_type, "Py_None"),
                    pybuffernd_struct))
        code.putln(code.error_goto(pos))
        code.put('} else {')
        # Unpack indices
        put_unpack_buffer_aux_into_scope(buf_entry, code)
        code.putln('}')

    code.putln("}") # Release stack

def put_buffer_lookup_code(entry, index_signeds, index_cnames, directives, pos, code):
    """
    Generates code to process indices and calculate an offset into
    a buffer. Returns a C string which gives a pointer which can be
    read from or written to at will (it is an expression so caller should
    store it in a temporary if it is used more than once).

    As the bounds checking can have any number of combinations of unsigned
    arguments, smart optimizations etc. we insert it directly in the function
    body. The lookup however is delegated to a inline function that is instantiated
    once per ndim (lookup with suboffsets tend to get quite complicated).

    """
    bufaux = entry.buffer_aux
    pybuffernd_struct = bufaux.buflocal_nd_var.cname
    # bufstruct = bufaux.buffer_info_var.cname
    negative_indices = directives['wraparound'] and entry.type.negative_indices

    if directives['boundscheck']:
        # Check bounds and fix negative indices.
        # We allocate a temporary which is initialized to -1, meaning OK (!).
        # If an error occurs, the temp is set to the dimension index the
        # error is occuring at.
        tmp_cname = code.funcstate.allocate_temp(PyrexTypes.c_int_type, manage_ref=False)
        code.putln("%s = -1;" % tmp_cname)
        for dim, (signed, cname, shape) in enumerate(zip(index_signeds, index_cnames,
                                                         get_buf_shapevars(entry))):
            if signed != 0:
                # not unsigned, deal with negative index
                code.putln("if (%s < 0) {" % cname)
                if negative_indices:
                    code.putln("%s += %s;" % (cname, shape))
                    code.putln("if (%s) %s = %d;" % (
                        code.unlikely("%s < 0" % cname), tmp_cname, dim))
                else:
                    code.putln("%s = %d;" % (tmp_cname, dim))
                code.put("} else ")
            # check bounds in positive direction
            if signed != 0:
                cast = ""
            else:
                cast = "(size_t)"
            code.putln("if (%s) %s = %d;" % (
                code.unlikely("%s >= %s%s" % (cname, cast, shape)),
                tmp_cname, dim))
        code.globalstate.use_utility_code(raise_indexerror_code)
        code.putln("if (%s) {" % code.unlikely("%s != -1" % tmp_cname))
        code.putln('__Pyx_RaiseBufferIndexError(%s);' % tmp_cname)
        code.putln(code.error_goto(pos))
        code.putln('}')
        code.funcstate.release_temp(tmp_cname)
    elif negative_indices:
        # Only fix negative indices.
        for signed, cname, shape in zip(index_signeds, index_cnames,
                                        get_buf_shapevars(entry)):
            if signed != 0:
                code.putln("if (%s < 0) %s += %s;" % (cname, cname, shape))

    # Create buffer lookup and return it
    # This is done via utility macros/inline functions, which vary
    # according to the access mode used.
    params = []
    nd = entry.type.ndim
    mode = entry.type.mode
    if mode == 'full':
        for i, s, o in zip(index_cnames, get_buf_stridevars(entry), get_buf_suboffsetvars(entry)):
            params.append(i)
            params.append(s)
            params.append(o)
        funcname = "__Pyx_BufPtrFull%dd" % nd
        funcgen = buf_lookup_full_code
    else:
        if mode == 'strided':
            funcname = "__Pyx_BufPtrStrided%dd" % nd
            funcgen = buf_lookup_strided_code
        elif mode == 'c':
            funcname = "__Pyx_BufPtrCContig%dd" % nd
            funcgen = buf_lookup_c_code
        elif mode == 'fortran':
            funcname = "__Pyx_BufPtrFortranContig%dd" % nd
            funcgen = buf_lookup_fortran_code
        else:
            assert False
        for i, s in zip(index_cnames, get_buf_stridevars(entry)):
            params.append(i)
            params.append(s)

    # Make sure the utility code is available
    if funcname not in code.globalstate.utility_codes:
        code.globalstate.utility_codes.add(funcname)
        protocode = code.globalstate['utility_code_proto']
        defcode = code.globalstate['utility_code_def']
        funcgen(protocode, defcode, name=funcname, nd=nd)

    ptr_type = entry.type.buffer_ptr_type
    ptrcode = "%s(%s, %s.rcbuffer->pybuffer.buf, %s)" % (funcname,
                                      ptr_type.declaration_code(""),
                                      pybuffernd_struct,
                                      ", ".join(params))
    return ptrcode


def use_bufstruct_declare_code(env):
    env.use_utility_code(buffer_struct_declare_code)

def use_empty_bufstruct_code(env, max_ndim):
    code = dedent("""
        Py_ssize_t __Pyx_zeros[] = {%s};
        Py_ssize_t __Pyx_minusones[] = {%s};
    """) % (", ".join(["0"] * max_ndim), ", ".join(["-1"] * max_ndim))
    env.use_utility_code(UtilityCode(proto=code))


def buf_lookup_full_code(proto, defin, name, nd):
    """
    Generates a buffer lookup function for the right number
    of dimensions. The function gives back a void* at the right location.
    """
    # _i_ndex, _s_tride, sub_o_ffset
    macroargs = ", ".join(["i%d, s%d, o%d" % (i, i, i) for i in range(nd)])
    proto.putln("#define %s(type, buf, %s) (type)(%s_imp(buf, %s))" % (name, macroargs, name, macroargs))

    funcargs = ", ".join(["Py_ssize_t i%d, Py_ssize_t s%d, Py_ssize_t o%d" % (i, i, i) for i in range(nd)])
    proto.putln("static CYTHON_INLINE void* %s_imp(void* buf, %s);" % (name, funcargs))
    defin.putln(dedent("""
        static CYTHON_INLINE void* %s_imp(void* buf, %s) {
          char* ptr = (char*)buf;
        """) % (name, funcargs) + "".join([dedent("""\
          ptr += s%d * i%d;
          if (o%d >= 0) ptr = *((char**)ptr) + o%d;
        """) % (i, i, i, i) for i in range(nd)]
        ) + "\nreturn ptr;\n}")

def buf_lookup_strided_code(proto, defin, name, nd):
    """
    Generates a buffer lookup function for the right number
    of dimensions. The function gives back a void* at the right location.
    """
    # _i_ndex, _s_tride
    args = ", ".join(["i%d, s%d" % (i, i) for i in range(nd)])
    offset = " + ".join(["i%d * s%d" % (i, i) for i in range(nd)])
    proto.putln("#define %s(type, buf, %s) (type)((char*)buf + %s)" % (name, args, offset))

def buf_lookup_c_code(proto, defin, name, nd):
    """
    Similar to strided lookup, but can assume that the last dimension
    doesn't need a multiplication as long as.
    Still we keep the same signature for now.
    """
    if nd == 1:
        proto.putln("#define %s(type, buf, i0, s0) ((type)buf + i0)" % name)
    else:
        args = ", ".join(["i%d, s%d" % (i, i) for i in range(nd)])
        offset = " + ".join(["i%d * s%d" % (i, i) for i in range(nd - 1)])
        proto.putln("#define %s(type, buf, %s) ((type)((char*)buf + %s) + i%d)" % (name, args, offset, nd - 1))

def buf_lookup_fortran_code(proto, defin, name, nd):
    """
    Like C lookup, but the first index is optimized instead.
    """
    if nd == 1:
        proto.putln("#define %s(type, buf, i0, s0) ((type)buf + i0)" % name)
    else:
        args = ", ".join(["i%d, s%d" % (i, i) for i in range(nd)])
        offset = " + ".join(["i%d * s%d" % (i, i) for i in range(1, nd)])
        proto.putln("#define %s(type, buf, %s) ((type)((char*)buf + %s) + i%d)" % (name, args, offset, 0))


def use_py2_buffer_functions(env):
    # Emulation of PyObject_GetBuffer and PyBuffer_Release for Python 2.
    # For >= 2.6 we do double mode -- use the new buffer interface on objects
    # which has the right tp_flags set, but emulation otherwise.

    # Search all types for __getbuffer__ overloads
    types = []
    visited_scopes = set()
    def find_buffer_types(scope):
        if scope in visited_scopes:
            return
        visited_scopes.add(scope)
        for m in scope.cimported_modules:
            find_buffer_types(m)
        for e in scope.type_entries:
            t = e.type
            if t.is_extension_type:
                release = get = None
                for x in t.scope.pyfunc_entries:
                    if x.name == u"__getbuffer__": get = x.func_cname
                    elif x.name == u"__releasebuffer__": release = x.func_cname
                if get:
                    types.append((t.typeptr_cname, get, release))

    find_buffer_types(env)

    code = dedent("""
        #if PY_MAJOR_VERSION < 3
        static int __Pyx_GetBuffer(PyObject *obj, Py_buffer *view, int flags) {
          #if PY_VERSION_HEX >= 0x02060000
          if (PyObject_CheckBuffer(obj)) return PyObject_GetBuffer(obj, view, flags);
          #endif
    """)
    if len(types) > 0:
        clause = "if"
        for t, get, release in types:
            code += "  %s (PyObject_TypeCheck(obj, %s)) return %s(obj, view, flags);\n" % (clause, t, get)
            clause = "else if"
        code += "  else {\n"
    code += dedent("""\
        PyErr_Format(PyExc_TypeError, "'%100s' does not have the buffer interface", Py_TYPE(obj)->tp_name);
        return -1;
    """, 2)
    if len(types) > 0: code += "  }"
    code += dedent("""
        }

        static void __Pyx_ReleaseBuffer(Py_buffer *view) {
          PyObject* obj = view->obj;
          if (obj) {
            #if PY_VERSION_HEX >= 0x02060000
            if (PyObject_CheckBuffer(obj)) {PyBuffer_Release(view); return;}
            #endif
    """)
    if len(types) > 0:
        clause = "if"
        for t, get, release in types:
            if release:
                code += "    "
                code += "%s (PyObject_TypeCheck(obj, %s)) %s(obj, view);" % (clause, t, release)
                clause = "else if"
    code += dedent("""
            Py_DECREF(obj);
            view->obj = NULL;
          }
        }

        #endif
    """)

    env.use_utility_code(UtilityCode(
            proto = dedent("""\
        #if PY_MAJOR_VERSION < 3
        static int __Pyx_GetBuffer(PyObject *obj, Py_buffer *view, int flags);
        static void __Pyx_ReleaseBuffer(Py_buffer *view);
        #else
        #define __Pyx_GetBuffer PyObject_GetBuffer
        #define __Pyx_ReleaseBuffer PyBuffer_Release
        #endif
    """), impl = code))


def mangle_dtype_name(dtype):
    # Use prefixes to seperate user defined types from builtins
    # (consider "typedef float unsigned_int")
    if dtype.is_pyobject:
        return "object"
    elif dtype.is_ptr:
        return "ptr"
    else:
        if dtype.is_typedef or dtype.is_struct_or_union:
            prefix = "nn_"
        else:
            prefix = ""
        return prefix + dtype.declaration_code("").replace(" ", "_")

def get_type_information_cname(code, dtype, maxdepth=None):
    # Output the run-time type information (__Pyx_TypeInfo) for given dtype,
    # and return the name of the type info struct.
    #
    # Structs with two floats of the same size are encoded as complex numbers.
    # One can seperate between complex numbers declared as struct or with native
    # encoding by inspecting to see if the fields field of the type is
    # filled in.
    namesuffix = mangle_dtype_name(dtype)
    name = "__Pyx_TypeInfo_%s" % namesuffix
    structinfo_name = "__Pyx_StructFields_%s" % namesuffix

    if dtype.is_error: return "<error>"

    # It's critical that walking the type info doesn't use more stack
    # depth than dtype.struct_nesting_depth() returns, so use an assertion for this
    if maxdepth is None: maxdepth = dtype.struct_nesting_depth()
    if maxdepth <= 0:
        assert False

    if name not in code.globalstate.utility_codes:
        code.globalstate.utility_codes.add(name)
        typecode = code.globalstate['typeinfo']

        complex_possible = dtype.is_struct_or_union and dtype.can_be_complex()

        declcode = dtype.declaration_code("")
        if dtype.is_simple_buffer_dtype():
            structinfo_name = "NULL"
        elif dtype.is_struct:
            fields = dtype.scope.var_entries
            # Must pre-call all used types in order not to recurse utility code
            # writing.
            assert len(fields) > 0
            types = [get_type_information_cname(code, f.type, maxdepth - 1)
                     for f in fields]
            typecode.putln("static __Pyx_StructField %s[] = {" % structinfo_name, safe=True)
            for f, typeinfo in zip(fields, types):
                typecode.putln('  {&%s, "%s", offsetof(%s, %s)},' %
                           (typeinfo, f.name, dtype.declaration_code(""), f.cname), safe=True)
            typecode.putln('  {NULL, NULL, 0}', safe=True)
            typecode.putln("};", safe=True)
        else:
            assert False

        rep = str(dtype)
        if dtype.is_int:
            if dtype.signed == 0:
                typegroup = 'U'
            else:
                typegroup = 'I'
        elif complex_possible or dtype.is_complex:
            typegroup = 'C'
        elif dtype.is_float:
            typegroup = 'R'
        elif dtype.is_struct:
            typegroup = 'S'
        elif dtype.is_pyobject:
            typegroup = 'O'
        else:
            print dtype
            assert False

        typecode.putln(('static __Pyx_TypeInfo %s = { "%s", %s, sizeof(%s), \'%s\' };'
                        ) % (name,
                             rep,
                             structinfo_name,
                             declcode,
                             typegroup,
                        ), safe=True)
    return name

buffer_struct_declare_code = UtilityCode(proto="""

/* structs for buffer access */

typedef struct {
  Py_ssize_t shape, strides, suboffsets;
} __Pyx_Buf_DimInfo;

typedef struct {
  size_t refcount;
  Py_buffer pybuffer;
} __Pyx_Buffer;

typedef struct {
  __Pyx_Buffer *rcbuffer;
  char *data;
  __Pyx_Buf_DimInfo diminfo[%d];
} __Pyx_LocalBuf_ND;

""" % Options.buffer_max_dims)


# Utility function to set the right exception
# The caller should immediately goto_error
raise_indexerror_code = UtilityCode(
proto = """\
static void __Pyx_RaiseBufferIndexError(int axis); /*proto*/
""",
impl = """\
static void __Pyx_RaiseBufferIndexError(int axis) {
  PyErr_Format(PyExc_IndexError,
     "Out of bounds on buffer access (axis %d)", axis);
}

""")

parse_typestring_repeat_code = UtilityCode(
proto = """
""",
impl = """
""")

raise_buffer_fallback_code = UtilityCode(
proto = """
static void __Pyx_RaiseBufferFallbackError(void); /*proto*/
""",
impl = """
static void __Pyx_RaiseBufferFallbackError(void) {
  PyErr_Format(PyExc_ValueError,
     "Buffer acquisition failed on assignment; and then reacquiring the old buffer failed too!");
}

""")



#
# Buffer format string checking
#
# Buffer type checking. Utility code for checking that acquired
# buffers match our assumptions. We only need to check ndim and
# the format string; the access mode/flags is checked by the
# exporter.
#
# The alignment code is copied from _struct.c in Python.
acquire_utility_code = UtilityCode(proto="""
/* Run-time type information about structs used with buffers */
struct __Pyx_StructField_;

typedef struct {
  const char* name; /* for error messages only */
  struct __Pyx_StructField_* fields;
  size_t size;     /* sizeof(type) */
  char typegroup; /* _R_eal, _C_omplex, Signed _I_nt, _U_nsigned int, _S_truct, _P_ointer, _O_bject */
} __Pyx_TypeInfo;

typedef struct __Pyx_StructField_ {
  __Pyx_TypeInfo* type;
  const char* name;
  size_t offset;
} __Pyx_StructField;

typedef struct {
  __Pyx_StructField* field;
  size_t parent_offset;
} __Pyx_BufFmt_StackElem;


static CYTHON_INLINE int  __Pyx_GetBufferAndValidate(Py_buffer* buf, PyObject* obj, __Pyx_TypeInfo* dtype, int flags, int nd, int cast, __Pyx_BufFmt_StackElem* stack);
static CYTHON_INLINE void __Pyx_SafeReleaseBuffer(Py_buffer* info);
""", impl="""
static CYTHON_INLINE int __Pyx_IsLittleEndian(void) {
  unsigned int n = 1;
  return *(unsigned char*)(&n) != 0;
}

typedef struct {
  __Pyx_StructField root;
  __Pyx_BufFmt_StackElem* head;
  size_t fmt_offset;
  size_t new_count, enc_count;
  int is_complex;
  char enc_type;
  char new_packmode;
  char enc_packmode;
} __Pyx_BufFmt_Context;

static void __Pyx_BufFmt_Init(__Pyx_BufFmt_Context* ctx,
                              __Pyx_BufFmt_StackElem* stack,
                              __Pyx_TypeInfo* type) {
  stack[0].field = &ctx->root;
  stack[0].parent_offset = 0;
  ctx->root.type = type;
  ctx->root.name = "buffer dtype";
  ctx->root.offset = 0;
  ctx->head = stack;
  ctx->head->field = &ctx->root;
  ctx->fmt_offset = 0;
  ctx->head->parent_offset = 0;
  ctx->new_packmode = '@';
  ctx->enc_packmode = '@';
  ctx->new_count = 1;
  ctx->enc_count = 0;
  ctx->enc_type = 0;
  ctx->is_complex = 0;
  while (type->typegroup == 'S') {
    ++ctx->head;
    ctx->head->field = type->fields;
    ctx->head->parent_offset = 0;
    type = type->fields->type;
  }
}

static int __Pyx_BufFmt_ParseNumber(const char** ts) {
    int count;
    const char* t = *ts;
    if (*t < '0' || *t > '9') {
      return -1;
    } else {
        count = *t++ - '0';
        while (*t >= '0' && *t < '9') {
            count *= 10;
            count += *t++ - '0';
        }
    }
    *ts = t;
    return count;
}

static void __Pyx_BufFmt_RaiseUnexpectedChar(char ch) {
  PyErr_Format(PyExc_ValueError,
               "Unexpected format string character: '%c'", ch);
}

static const char* __Pyx_BufFmt_DescribeTypeChar(char ch, int is_complex) {
  switch (ch) {
    case 'b': return "'char'";
    case 'B': return "'unsigned char'";
    case 'h': return "'short'";
    case 'H': return "'unsigned short'";
    case 'i': return "'int'";
    case 'I': return "'unsigned int'";
    case 'l': return "'long'";
    case 'L': return "'unsigned long'";
    case 'q': return "'long long'";
    case 'Q': return "'unsigned long long'";
    case 'f': return (is_complex ? "'complex float'" : "'float'");
    case 'd': return (is_complex ? "'complex double'" : "'double'");
    case 'g': return (is_complex ? "'complex long double'" : "'long double'");
    case 'T': return "a struct";
    case 'O': return "Python object";
    case 'P': return "a pointer";
    case 0: return "end";
    default: return "unparseable format string";
  }
}

static size_t __Pyx_BufFmt_TypeCharToStandardSize(char ch, int is_complex) {
  switch (ch) {
    case '?': case 'c': case 'b': case 'B': return 1;
    case 'h': case 'H': return 2;
    case 'i': case 'I': case 'l': case 'L': return 4;
    case 'q': case 'Q': return 8;
    case 'f': return (is_complex ? 8 : 4);
    case 'd': return (is_complex ? 16 : 8);
    case 'g': {
      PyErr_SetString(PyExc_ValueError, "Python does not define a standard format string size for long double ('g')..");
      return 0;
    }
    case 'O': case 'P': return sizeof(void*);
    default:
      __Pyx_BufFmt_RaiseUnexpectedChar(ch);
      return 0;
    }
}

static size_t __Pyx_BufFmt_TypeCharToNativeSize(char ch, int is_complex) {
  switch (ch) {
    case 'c': case 'b': case 'B': return 1;
    case 'h': case 'H': return sizeof(short);
    case 'i': case 'I': return sizeof(int);
    case 'l': case 'L': return sizeof(long);
    #ifdef HAVE_LONG_LONG
    case 'q': case 'Q': return sizeof(PY_LONG_LONG);
    #endif
    case 'f': return sizeof(float) * (is_complex ? 2 : 1);
    case 'd': return sizeof(double) * (is_complex ? 2 : 1);
    case 'g': return sizeof(long double) * (is_complex ? 2 : 1);
    case 'O': case 'P': return sizeof(void*);
    default: {
      __Pyx_BufFmt_RaiseUnexpectedChar(ch);
      return 0;
    }
  }
}

typedef struct { char c; short x; } __Pyx_st_short;
typedef struct { char c; int x; } __Pyx_st_int;
typedef struct { char c; long x; } __Pyx_st_long;
typedef struct { char c; float x; } __Pyx_st_float;
typedef struct { char c; double x; } __Pyx_st_double;
typedef struct { char c; long double x; } __Pyx_st_longdouble;
typedef struct { char c; void *x; } __Pyx_st_void_p;
#ifdef HAVE_LONG_LONG
typedef struct { char c; PY_LONG_LONG x; } __Pyx_st_longlong;
#endif

static size_t __Pyx_BufFmt_TypeCharToAlignment(char ch, int is_complex) {
  switch (ch) {
    case '?': case 'c': case 'b': case 'B': return 1;
    case 'h': case 'H': return sizeof(__Pyx_st_short) - sizeof(short);
    case 'i': case 'I': return sizeof(__Pyx_st_int) - sizeof(int);
    case 'l': case 'L': return sizeof(__Pyx_st_long) - sizeof(long);
#ifdef HAVE_LONG_LONG
    case 'q': case 'Q': return sizeof(__Pyx_st_longlong) - sizeof(PY_LONG_LONG);
#endif
    case 'f': return sizeof(__Pyx_st_float) - sizeof(float);
    case 'd': return sizeof(__Pyx_st_double) - sizeof(double);
    case 'g': return sizeof(__Pyx_st_longdouble) - sizeof(long double);
    case 'P': case 'O': return sizeof(__Pyx_st_void_p) - sizeof(void*);
    default:
      __Pyx_BufFmt_RaiseUnexpectedChar(ch);
      return 0;
    }
}

static char __Pyx_BufFmt_TypeCharToGroup(char ch, int is_complex) {
  switch (ch) {
    case 'c': case 'b': case 'h': case 'i': case 'l': case 'q': return 'I';
    case 'B': case 'H': case 'I': case 'L': case 'Q': return 'U';
    case 'f': case 'd': case 'g': return (is_complex ? 'C' : 'R');
    case 'O': return 'O';
    case 'P': return 'P';
    default: {
      __Pyx_BufFmt_RaiseUnexpectedChar(ch);
      return 0;
    }
  }
}

static void __Pyx_BufFmt_RaiseExpected(__Pyx_BufFmt_Context* ctx) {
  if (ctx->head == NULL || ctx->head->field == &ctx->root) {
    const char* expected;
    const char* quote;
    if (ctx->head == NULL) {
      expected = "end";
      quote = "";
    } else {
      expected = ctx->head->field->type->name;
      quote = "'";
    }
    PyErr_Format(PyExc_ValueError,
                 "Buffer dtype mismatch, expected %s%s%s but got %s",
                 quote, expected, quote,
                 __Pyx_BufFmt_DescribeTypeChar(ctx->enc_type, ctx->is_complex));
  } else {
    __Pyx_StructField* field = ctx->head->field;
    __Pyx_StructField* parent = (ctx->head - 1)->field;
    PyErr_Format(PyExc_ValueError,
                 "Buffer dtype mismatch, expected '%s' but got %s in '%s.%s'",
                 field->type->name, __Pyx_BufFmt_DescribeTypeChar(ctx->enc_type, ctx->is_complex),
                 parent->type->name, field->name);
  }
}

static int __Pyx_BufFmt_ProcessTypeChunk(__Pyx_BufFmt_Context* ctx) {
  char group;
  size_t size, offset;
  if (ctx->enc_type == 0) return 0;
  group = __Pyx_BufFmt_TypeCharToGroup(ctx->enc_type, ctx->is_complex);
  do {
    __Pyx_StructField* field = ctx->head->field;
    __Pyx_TypeInfo* type = field->type;

    if (ctx->enc_packmode == '@' || ctx->enc_packmode == '^') {
      size = __Pyx_BufFmt_TypeCharToNativeSize(ctx->enc_type, ctx->is_complex);
    } else {
      size = __Pyx_BufFmt_TypeCharToStandardSize(ctx->enc_type, ctx->is_complex);
    }
    if (ctx->enc_packmode == '@') {
      size_t align_at = __Pyx_BufFmt_TypeCharToAlignment(ctx->enc_type, ctx->is_complex);
      size_t align_mod_offset;
      if (align_at == 0) return -1;
      align_mod_offset = ctx->fmt_offset % align_at;
      if (align_mod_offset > 0) ctx->fmt_offset += align_at - align_mod_offset;
    }

    if (type->size != size || type->typegroup != group) {
      if (type->typegroup == 'C' && type->fields != NULL) {
        /* special case -- treat as struct rather than complex number */
        size_t parent_offset = ctx->head->parent_offset + field->offset;
        ++ctx->head;
        ctx->head->field = type->fields;
        ctx->head->parent_offset = parent_offset;
        continue;
      }

      __Pyx_BufFmt_RaiseExpected(ctx);
      return -1;
    }

    offset = ctx->head->parent_offset + field->offset;
    if (ctx->fmt_offset != offset) {
      PyErr_Format(PyExc_ValueError,
                   "Buffer dtype mismatch; next field is at offset %"PY_FORMAT_SIZE_T"d but %"PY_FORMAT_SIZE_T"d expected",
                   (Py_ssize_t)ctx->fmt_offset, (Py_ssize_t)offset);
      return -1;
    }

    ctx->fmt_offset += size;

    --ctx->enc_count; /* Consume from buffer string */

    /* Done checking, move to next field, pushing or popping struct stack if needed */
    while (1) {
      if (field == &ctx->root) {
        ctx->head = NULL;
        if (ctx->enc_count != 0) {
          __Pyx_BufFmt_RaiseExpected(ctx);
          return -1;
        }
        break; /* breaks both loops as ctx->enc_count == 0 */
      }
      ctx->head->field = ++field;
      if (field->type == NULL) {
        --ctx->head;
        field = ctx->head->field;
        continue;
      } else if (field->type->typegroup == 'S') {
        size_t parent_offset = ctx->head->parent_offset + field->offset;
        if (field->type->fields->type == NULL) continue; /* empty struct */
        field = field->type->fields;
        ++ctx->head;
        ctx->head->field = field;
        ctx->head->parent_offset = parent_offset;
        break;
      } else {
        break;
      }
    }
  } while (ctx->enc_count);
  ctx->enc_type = 0;
  ctx->is_complex = 0;
  return 0;
}

static const char* __Pyx_BufFmt_CheckString(__Pyx_BufFmt_Context* ctx, const char* ts) {
  int got_Z = 0;
  while (1) {
    switch(*ts) {
      case 0:
        if (ctx->enc_type != 0 && ctx->head == NULL) {
          __Pyx_BufFmt_RaiseExpected(ctx);
          return NULL;
        }
        if (__Pyx_BufFmt_ProcessTypeChunk(ctx) == -1) return NULL;
        if (ctx->head != NULL) {
          __Pyx_BufFmt_RaiseExpected(ctx);
          return NULL;
        }
        return ts;
      case ' ':
      case 10:
      case 13:
        ++ts;
        break;
      case '<':
        if (!__Pyx_IsLittleEndian()) {
          PyErr_SetString(PyExc_ValueError, "Little-endian buffer not supported on big-endian compiler");
          return NULL;
        }
        ctx->new_packmode = '=';
        ++ts;
        break;
      case '>':
      case '!':
        if (__Pyx_IsLittleEndian()) {
          PyErr_SetString(PyExc_ValueError, "Big-endian buffer not supported on little-endian compiler");
          return NULL;
        }
        ctx->new_packmode = '=';
        ++ts;
        break;
      case '=':
      case '@':
      case '^':
        ctx->new_packmode = *ts++;
        break;
      case 'T': /* substruct */
        {
          const char* ts_after_sub;
          size_t i, struct_count = ctx->new_count;
          ctx->new_count = 1;
          ++ts;
          if (*ts != '{') {
            PyErr_SetString(PyExc_ValueError, "Buffer acquisition: Expected '{' after 'T'");
            return NULL;
          }
          ++ts;
          ts_after_sub = ts;
          for (i = 0; i != struct_count; ++i) {
            ts_after_sub = __Pyx_BufFmt_CheckString(ctx, ts);
            if (!ts_after_sub) return NULL;
          }
          ts = ts_after_sub;
        }
        break;
      case '}': /* end of substruct; either repeat or move on */
        ++ts;
        return ts;
      case 'x':
        if (__Pyx_BufFmt_ProcessTypeChunk(ctx) == -1) return NULL;
        ctx->fmt_offset += ctx->new_count;
        ctx->new_count = 1;
        ctx->enc_count = 0;
        ctx->enc_type = 0;
        ctx->enc_packmode = ctx->new_packmode;
        ++ts;
        break;
      case 'Z':
        got_Z = 1;
        ++ts;
        if (*ts != 'f' && *ts != 'd' && *ts != 'g') {
          __Pyx_BufFmt_RaiseUnexpectedChar('Z');
          return NULL;
        }        /* fall through */
      case 'c': case 'b': case 'B': case 'h': case 'H': case 'i': case 'I':
      case 'l': case 'L': case 'q': case 'Q':
      case 'f': case 'd': case 'g':
      case 'O':
        if (ctx->enc_type == *ts && got_Z == ctx->is_complex &&
            ctx->enc_packmode == ctx->new_packmode) {
          /* Continue pooling same type */
          ctx->enc_count += ctx->new_count;
        } else {
          /* New type */
          if (__Pyx_BufFmt_ProcessTypeChunk(ctx) == -1) return NULL;
          ctx->enc_count = ctx->new_count;
          ctx->enc_packmode = ctx->new_packmode;
          ctx->enc_type = *ts;
          ctx->is_complex = got_Z;
        }
        ++ts;
        ctx->new_count = 1;
        got_Z = 0;
        break;
      case ':':
        ++ts;
        while(*ts != ':') ++ts;
        ++ts;
        break;
      default:
        {
          int number = __Pyx_BufFmt_ParseNumber(&ts);
          if (number == -1) { /* First char was not a digit */
            PyErr_Format(PyExc_ValueError,
                         "Does not understand character buffer dtype format string ('%c')", *ts);
            return NULL;
          }
          ctx->new_count = (size_t)number; 
        }
    }
  }
}

static CYTHON_INLINE void __Pyx_ZeroBuffer(Py_buffer* buf) {
  buf->buf = NULL;
  buf->obj = NULL;
  buf->strides = __Pyx_zeros;
  buf->shape = __Pyx_zeros;
  buf->suboffsets = __Pyx_minusones;
}

static CYTHON_INLINE int __Pyx_GetBufferAndValidate(Py_buffer* buf, PyObject* obj, __Pyx_TypeInfo* dtype, int flags, int nd, int cast, __Pyx_BufFmt_StackElem* stack) {
  if (obj == Py_None || obj == NULL) {
    __Pyx_ZeroBuffer(buf);
    return 0;
  }
  buf->buf = NULL;
  if (__Pyx_GetBuffer(obj, buf, flags) == -1) goto fail;
  if (buf->ndim != nd) {
    PyErr_Format(PyExc_ValueError,
                 "Buffer has wrong number of dimensions (expected %d, got %d)",
                 nd, buf->ndim);
    goto fail;
  }
  if (!cast) {
    __Pyx_BufFmt_Context ctx;
    __Pyx_BufFmt_Init(&ctx, stack, dtype);
    if (!__Pyx_BufFmt_CheckString(&ctx, buf->format)) goto fail;
  }
  if ((unsigned)buf->itemsize != dtype->size) {
    PyErr_Format(PyExc_ValueError,
      "Item size of buffer (%"PY_FORMAT_SIZE_T"d byte%s) does not match size of '%s' (%"PY_FORMAT_SIZE_T"d byte%s)",
      buf->itemsize, (buf->itemsize > 1) ? "s" : "",
      dtype->name, (Py_ssize_t)dtype->size, (dtype->size > 1) ? "s" : "");
    goto fail;
  }
  if (buf->suboffsets == NULL) buf->suboffsets = __Pyx_minusones;
  return 0;
fail:;
  __Pyx_ZeroBuffer(buf);
  return -1;
}

static CYTHON_INLINE void __Pyx_SafeReleaseBuffer(Py_buffer* info) {
  if (info->buf == NULL) return;
  if (info->suboffsets == __Pyx_minusones) info->suboffsets = NULL;
  __Pyx_ReleaseBuffer(info);
}
""")

