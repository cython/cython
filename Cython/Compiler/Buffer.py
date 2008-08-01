from Cython.Compiler.Visitor import VisitorTransform, temp_name_handle, CythonTransform
from Cython.Compiler.ModuleNode import ModuleNode
from Cython.Compiler.Nodes import *
from Cython.Compiler.ExprNodes import *
from Cython.Compiler.TreeFragment import TreeFragment
from Cython.Utils import EncodedString
from Cython.Compiler.Errors import CompileError
import PyrexTypes
from sets import Set as set
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

    def __call__(self, node):
        assert isinstance(node, ModuleNode)
        self.max_ndim = 0
        result = super(IntroduceBufferAuxiliaryVars, self).__call__(node)
        if self.buffers_exists:
            if "endian.h" not in node.scope.include_files:
                node.scope.include_files.append("endian.h")
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


        if isinstance(node, ModuleNode) and len(bufvars) > 0:
            # for now...note that pos is wrong 
            raise CompileError(node.pos, "Buffer vars not allowed in module scope")
        for entry in bufvars:
            name = entry.name
            buftype = entry.type
            if buftype.ndim > self.max_ndim:
                self.max_ndim = buftype.ndim

            # Declare auxiliary vars
            cname = scope.mangle(Naming.bufstruct_prefix, name)
            bufinfo = scope.declare_var(name="$%s" % cname, cname=cname,
                                        type=PyrexTypes.c_py_buffer_type, pos=node.pos)

            bufinfo.used = True

            def var(prefix, idx, initval):
                cname = scope.mangle(prefix, "%d_%s" % (idx, name))
                result = scope.declare_var("$%s" % cname, PyrexTypes.c_py_ssize_t_type,
                                         node.pos, cname=cname, is_cdef=True)

                result.init = initval
                if entry.is_arg:
                    result.used = True
                return result
            

            stridevars = [var(Naming.bufstride_prefix, i, "0") for i in range(entry.type.ndim)]
            shapevars = [var(Naming.bufshape_prefix, i, "0") for i in range(entry.type.ndim)]            
            mode = entry.type.mode
            if mode == 'full':
                suboffsetvars = [var(Naming.bufsuboffset_prefix, i, "-1") for i in range(entry.type.ndim)]
            elif mode == 'strided':
                suboffsetvars = None

            entry.buffer_aux = Symtab.BufferAux(bufinfo, stridevars, shapevars, suboffsetvars)
            
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




def get_flags(buffer_aux, buffer_type):
    flags = 'PyBUF_FORMAT'
    if buffer_type.mode == 'full':
        flags += '| PyBUF_INDIRECT'
    elif buffer_type.mode == 'strided':
        flags += '| PyBUF_STRIDES'
    else:
        assert False
    if buffer_aux.writable_needed: flags += "| PyBUF_WRITABLE"
    return flags
        
def used_buffer_aux_vars(entry):
    buffer_aux = entry.buffer_aux
    buffer_aux.buffer_info_var.used = True
    for s in buffer_aux.shapevars: s.used = True
    for s in buffer_aux.stridevars: s.used = True
    for s in buffer_aux.suboffsetvars: s.used = True

def put_unpack_buffer_aux_into_scope(buffer_aux, mode, code):
    # Generate code to copy the needed struct info into local
    # variables.
    bufstruct = buffer_aux.buffer_info_var.cname

    varspec = [("strides", buffer_aux.stridevars),
               ("shape", buffer_aux.shapevars)]
    if mode == 'full':
        varspec.append(("suboffsets", buffer_aux.suboffsetvars))

    for field, vars in varspec:
        code.putln(" ".join(["%s = %s.%s[%d];" %
                             (s.cname, bufstruct, field, idx)
                             for idx, s in enumerate(vars)]))

def put_acquire_arg_buffer(entry, code, pos):
    code.globalstate.use_utility_code(acquire_utility_code)
    buffer_aux = entry.buffer_aux
    getbuffer_cname = get_getbuffer_code(entry.type.dtype, code)
    # Acquire any new buffer
    code.putln(code.error_goto_if("%s(%s, &%s, %s, %d) == -1" % (
        getbuffer_cname,
        entry.cname,
        entry.buffer_aux.buffer_info_var.cname,
        get_flags(buffer_aux, entry.type),
        entry.type.ndim), pos))
    # An exception raised in arg parsing cannot be catched, so no
    # need to care about the buffer then.
    put_unpack_buffer_aux_into_scope(buffer_aux, entry.type.mode, code)

#def put_release_buffer_normal(entry, code):
#    code.putln("if (%s != Py_None) PyObject_ReleaseBuffer(%s, &%s);" % (
#        entry.cname,
#        entry.cname,
#        entry.buffer_aux.buffer_info_var.cname))

def get_release_buffer_code(entry):
    return "if (%s != Py_None) PyObject_ReleaseBuffer(%s, &%s)" % (
        entry.cname,
        entry.cname,
        entry.buffer_aux.buffer_info_var.cname)

def put_assign_to_buffer(lhs_cname, rhs_cname, buffer_aux, buffer_type,
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
    
    code.globalstate.use_utility_code(acquire_utility_code)
    bufstruct = buffer_aux.buffer_info_var.cname
    flags = get_flags(buffer_aux, buffer_type)

    getbuffer = "%s(%%s, &%s, %s, %d)" % (get_getbuffer_code(buffer_type.dtype, code),
                                          # note: object is filled in later (%%s)
                                          bufstruct,
                                          flags,
                                          buffer_type.ndim)

    if is_initialized:
        # Release any existing buffer
        code.put('if (%s != Py_None) ' % lhs_cname)
        code.begin_block();
        code.putln('PyObject_ReleaseBuffer(%s, &%s);' % (
            lhs_cname, bufstruct))
        code.end_block()
        # Acquire
        retcode_cname = code.funcstate.allocate_temp(PyrexTypes.c_int_type)
        code.putln("%s = %s;" % (retcode_cname, getbuffer % rhs_cname))
        code.putln('if (%s) ' % (code.unlikely("%s < 0" % retcode_cname)))
        # If acquisition failed, attempt to reacquire the old buffer
        # before raising the exception. A failure of reacquisition
        # will cause the reacquisition exception to be reported, one
        # can consider working around this later.
        code.begin_block()
        type, value, tb = [code.funcstate.allocate_temp(PyrexTypes.py_object_type)
                           for i in range(3)]
        code.putln('PyErr_Fetch(&%s, &%s, &%s);' % (type, value, tb))
        code.put('if (%s) ' % code.unlikely("%s == -1" % (getbuffer % lhs_cname)))
        code.begin_block()
        code.putln('Py_XDECREF(%s); Py_XDECREF(%s); Py_XDECREF(%s);' % (type, value, tb))
        code.putln('__Pyx_RaiseBufferFallbackError();')
        code.putln('} else {')
        code.putln('PyErr_Restore(%s, %s, %s);' % (type, value, tb))
        for t in (type, value, tb):
            code.funcstate.release_temp(t)
        code.end_block()
        # Unpack indices
        code.end_block()
        put_unpack_buffer_aux_into_scope(buffer_aux, buffer_type.mode, code)
        code.putln(code.error_goto_if_neg(retcode_cname, pos))
        code.funcstate.release_temp(retcode_cname)
    else:
        # Our entry had no previous value, so set to None when acquisition fails.
        # In this case, auxiliary vars should be set up right in initialization to a zero-buffer,
        # so it suffices to set the buf field to NULL.
        code.putln('if (%s) {' % code.unlikely("%s == -1" % (getbuffer % rhs_cname)))
        code.putln('%s = Py_None; Py_INCREF(Py_None); %s.buf = NULL;' % (lhs_cname, bufstruct))
        code.putln(code.error_goto(pos))
        code.put('} else {')
        # Unpack indices
        put_unpack_buffer_aux_into_scope(buffer_aux, buffer_type.mode, code)
        code.putln('}')


def put_access(entry, index_signeds, index_cnames, pos, code):
    """Returns a c string which can be used to access the buffer
    for reading or writing.

    As the bounds checking can have any number of combinations of unsigned
    arguments, smart optimizations etc. we insert it directly in the function
    body. The lookup however is delegated to a inline function that is instantiated
    once per ndim (lookup with suboffsets tend to get quite complicated).
    """
    code.globalstate.use_utility_code(access_utility_code)
    bufaux = entry.buffer_aux
    bufstruct = bufaux.buffer_info_var.cname
    # Check bounds and fix negative indices
    boundscheck = True
    nonegs = True
    tmp_cname = code.funcstate.allocate_temp(PyrexTypes.c_int_type)

    if boundscheck:
        code.putln("%s = -1;" % tmp_cname)
    for idx, (signed, cname, shape) in enumerate(zip(index_signeds, index_cnames,
                                  bufaux.shapevars)):
        if signed != 0:
            nonegs = False
            # not unsigned, deal with negative index
            code.putln("if (%s < 0) {" % cname)
            code.putln("%s += %s;" % (cname, shape.cname))
            if boundscheck:
                code.putln("if (%s) %s = %d;" % (
                    code.unlikely("%s < 0" % cname), tmp_cname, idx))
            code.put("} else ")
        else:
            if idx > 0: code.put("else ")
        if boundscheck:
            # check bounds in positive direction
            code.putln("if (%s) %s = %d;" % (
                code.unlikely("%s >= %s" % (cname, shape.cname)),
                tmp_cname, idx))
    if boundscheck:  
        code.put("if (%s) " % code.unlikely("%s != -1" % tmp_cname))
        code.begin_block()
        code.putln('__Pyx_BufferIndexError(%s);' % tmp_cname)
        code.putln(code.error_goto(pos))
        code.end_block()
    code.funcstate.release_temp(tmp_cname)



    

    # Create buffer lookup and return it
    params = []
    nd = entry.type.ndim
    if entry.type.mode == 'full':
        for i, s, o in zip(index_cnames, bufaux.stridevars, bufaux.suboffsetvars):
            params.append(i)
            params.append(s.cname)
            params.append(o.cname)

        funcname = "__Pyx_BufPtrFull%dd" % nd
        funcgen = buf_lookup_full_code
    else:
        for i, s in zip(index_cnames, bufaux.stridevars):
            params.append(i)
            params.append(s.cname)
        funcname = "__Pyx_BufPtrStrided%dd" % nd
        funcgen = buf_lookup_strided_code
        
    code.globalstate.use_generated_code(funcgen, name=funcname, nd=nd)

    ptrcode = "%s(%s.buf, %s)" % (funcname, bufstruct, ", ".join(params))
    valuecode = "*%s" % entry.type.buffer_ptr_type.cast_code(ptrcode)
    return valuecode



def use_empty_bufstruct_code(env, max_ndim):
    code = dedent("""
        Py_ssize_t __Pyx_zeros[] = {%s};
        Py_ssize_t __Pyx_minusones[] = {%s};
    """) % (", ".join(["0"] * max_ndim), ", ".join(["-1"] * max_ndim))
    env.use_utility_code([code, ""], "empty_bufstruct_code")


def buf_lookup_strided_code(proto, defin, name, nd):
    """
    Generates a buffer lookup function for the right number
    of dimensions. The function gives back a void* at the right location.
    """
    # _i_ndex, _s_tride
    args = ", ".join(["i%d, s%d" % (i, i) for i in range(nd)])
    offset = " + ".join(["i%d * s%d" % (i, i) for i in range(nd)])
    proto.putln("#define %s(buf, %s) ((char*)buf + %s)" % (name, args, offset))

def buf_lookup_full_code(proto, defin, name, nd):
    """
    Generates a buffer lookup function for the right number
    of dimensions. The function gives back a void* at the right location.
    """
    # _i_ndex, _s_tride, sub_o_ffset
    args = ", ".join(["Py_ssize_t i%d, Py_ssize_t s%d, Py_ssize_t o%d" % (i, i, i) for i in range(nd)])
    proto.putln("static INLINE void* %s(void* buf, %s);" % (name, args))
    defin.putln(dedent("""
        static INLINE void* %s(void* buf, %s) {
          char* ptr = (char*)buf;
        """) % (name, args) + "".join([dedent("""\
          ptr += s%d * i%d;
          if (o%d >= 0) ptr = *((char**)ptr) + o%d; 
        """) % (i, i, i, i) for i in range(nd)]
        ) + "\nreturn ptr;\n}")


#
# Utils for creating type string checkers
#
def mangle_dtype_name(dtype):
    # Use prefixes to seperate user defined types from builtins
    # (consider "typedef float unsigned_int")
    if dtype.typestring is None:
        prefix = "nn_"
    else:
        prefix = ""
    return prefix + dtype.declaration_code("").replace(" ", "_")

def get_ts_check_item(dtype, writer):
    # See if we can consume one (unnamed) dtype as next item
    # Put native types and structs in seperate namespaces (as one could create a struct named unsigned_int...)
    name = "__Pyx_BufferTypestringCheck_item_%s" % mangle_dtype_name(dtype)
    if not writer.globalstate.has_utility_code(name):
        char = dtype.typestring
        if char is not None:
                # Can use direct comparison
            code = dedent("""\
                if (*ts != '%s') {
                  PyErr_Format(PyExc_ValueError, "Buffer datatype mismatch (rejecting on '%%s')", ts);
                  return NULL;
                } else return ts + 1;
            """, 2) % char
        else:
            # Cannot trust declared size; but rely on int vs float and
            # signed/unsigned to be correctly declared
            ctype = dtype.declaration_code("")
            code = dedent("""\
                int ok;
                switch (*ts) {""", 2)
            if dtype.is_int:
                types = [
                    ('b', 'char'), ('h', 'short'), ('i', 'int'),
                    ('l', 'long'), ('q', 'long long')
                ]
                if dtype.signed == 0:
                    code += "".join(["\n    case '%s': ok = (sizeof(%s) == sizeof(%s) && (%s)-1 > 0); break;" %
                                 (char.upper(), ctype, against, ctype) for char, against in types])
                else:
                    code += "".join(["\n    case '%s': ok = (sizeof(%s) == sizeof(%s) && (%s)-1 < 0); break;" %
                                 (char, ctype, against, ctype) for char, against in types])
                code += dedent("""\
                      default: ok = 0;
                    }
                    if (!ok) {
                      PyErr_Format(PyExc_ValueError, "Buffer datatype mismatch (rejecting on '%s')", ts);
                      return NULL;
                    } else return ts + 1;
                """, 2)
        writer.globalstate.use_utility_code([dedent("""\
            static const char* %s(const char* ts); /*proto*/
        """) % name, dedent("""
            static const char* %s(const char* ts) {
            %s
            }
        """) % (name, code)], name=name)

    return name

def get_getbuffer_code(dtype, code):
    """
    Generate a utility function for getting a buffer for the given dtype.
    The function will:
    - Call PyObject_GetBuffer
    - Check that ndim matched the expected value
    - Check that the format string is right
    - Set suboffsets to all -1 if it is returned as NULL.
    """

    name = "__Pyx_GetBuffer_%s" % mangle_dtype_name(dtype)
    if not code.globalstate.has_utility_code(name):
        code.globalstate.use_utility_code(acquire_utility_code)
        itemchecker = get_ts_check_item(dtype, code)
        utilcode = [dedent("""
        static int %s(PyObject* obj, Py_buffer* buf, int flags, int nd); /*proto*/
        """) % name, dedent("""
        static int %(name)s(PyObject* obj, Py_buffer* buf, int flags, int nd) {
          const char* ts;
          if (obj == Py_None) {
            __Pyx_ZeroBuffer(buf);
            return 0;
          }
          buf->buf = NULL;
          if (PyObject_GetBuffer(obj, buf, flags) == -1) goto fail;
          if (buf->ndim != nd) {
            __Pyx_BufferNdimError(buf, nd);
            goto fail;
          }
          ts = buf->format;
          ts = __Pyx_ConsumeWhitespace(ts);
          ts = __Pyx_BufferTypestringCheckEndian(ts);
          if (!ts) goto fail;
          ts = __Pyx_ConsumeWhitespace(ts);
          ts = %(itemchecker)s(ts);
          if (!ts) goto fail;
          ts = __Pyx_ConsumeWhitespace(ts);
          if (*ts != 0) {
            PyErr_Format(PyExc_ValueError,
              "Expected non-struct buffer data type (rejecting on '%%s')", ts);
            goto fail;
          }
          if (buf->suboffsets == NULL) buf->suboffsets = __Pyx_minusones;
          return 0;
        fail:;
          __Pyx_ZeroBuffer(buf);
          return -1;
        }""") % locals()]
        code.globalstate.use_utility_code(utilcode, name)
    return name

def buffer_type_checker(dtype, code):
    # Creates a type checker function for the given type.
    if dtype.is_struct_or_union:
        assert False
    elif dtype.is_int or dtype.is_float:
        # This includes simple typedef-ed types
        funcname = get_getbuffer_code(dtype, code)
    else:
        assert False
    return funcname

def use_py2_buffer_functions(env):
    codename = "PyObject_GetBuffer" # just a representative unique key

    # Search all types for __getbuffer__ overloads
    types = []
    def find_buffer_types(scope):
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

    # For now, hard-code numpy imported as "numpy"
    try:
        ndarrtype = env.entries[u'numpy'].as_module.entries['ndarray'].type
        types.append((ndarrtype.typeptr_cname, "numpy_getbuffer", "numpy_releasebuffer"))
        env.use_utility_code(numpy_code)
    except KeyError:
        pass

    code = dedent("""
        #if PY_VERSION_HEX < 0x02060000
        static int PyObject_GetBuffer(PyObject *obj, Py_buffer *view, int flags) {
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

        static void PyObject_ReleaseBuffer(PyObject *obj, Py_buffer *view) {
    """)
    if len(types) > 0:
        clause = "if"
        for t, get, release in types:
            if release:
                code += "%s (PyObject_TypeCheck(obj, %s)) %s(obj, view);" % (clause, t, release)
                clause = "else if"
    code += dedent("""
        }

        #endif
    """)
                   
    env.use_utility_code([dedent("""\
        #if PY_VERSION_HEX < 0x02060000
        static int PyObject_GetBuffer(PyObject *obj, Py_buffer *view, int flags);
        static void PyObject_ReleaseBuffer(PyObject *obj, Py_buffer *view);
        #endif
    """), code], codename)

#
# Static utility code
#


# Utility function to set the right exception
# The caller should immediately goto_error
access_utility_code = [
"""\
static void __Pyx_BufferIndexError(int axis); /*proto*/
""","""\
static void __Pyx_BufferIndexError(int axis) {
  PyErr_Format(PyExc_IndexError,
     "Out of bounds on buffer access (axis %d)", axis);
}

"""]

#
# Buffer type checking. Utility code for checking that acquired
# buffers match our assumptions. We only need to check ndim and
# the format string; the access mode/flags is checked by the
# exporter.
#
acquire_utility_code = ["""\
static INLINE void __Pyx_ZeroBuffer(Py_buffer* buf); /*proto*/
static INLINE const char* __Pyx_ConsumeWhitespace(const char* ts); /*proto*/
static INLINE const char* __Pyx_BufferTypestringCheckEndian(const char* ts); /*proto*/
static void __Pyx_BufferNdimError(Py_buffer* buffer, int expected_ndim); /*proto*/
static void __Pyx_RaiseBufferFallbackError(void); /*proto*/
""", """
static INLINE void __Pyx_ZeroBuffer(Py_buffer* buf) {
  buf->buf = NULL;
  buf->strides = __Pyx_zeros;
  buf->shape = __Pyx_zeros;
  buf->suboffsets = __Pyx_minusones;
}

static INLINE const char* __Pyx_ConsumeWhitespace(const char* ts) {
  while (1) {
    switch (*ts) {
      case 10:
      case 13:
      case ' ':
        ++ts;
      default:
        return ts;
    }
  }
}

static INLINE const char* __Pyx_BufferTypestringCheckEndian(const char* ts) {
  int ok = 1;
  switch (*ts) {
    case '@':
    case '=':
      ++ts; break;
    case '<':
      if (__BYTE_ORDER == __LITTLE_ENDIAN) ++ts;
      else ok = 0;
      break;
    case '>':
    case '!':
      if (__BYTE_ORDER == __BIG_ENDIAN) ++ts;
      else ok = 0;
      break;
  }
  if (!ok) {
    PyErr_Format(PyExc_ValueError, "Buffer has wrong endianness (rejecting on '%s')", ts);
    return NULL;
  }
  return ts;
}

static void __Pyx_BufferNdimError(Py_buffer* buffer, int expected_ndim) {
  PyErr_Format(PyExc_ValueError,
               "Buffer has wrong number of dimensions (expected %d, got %d)",
               expected_ndim, buffer->ndim);
}

static void __Pyx_RaiseBufferFallbackError(void) {
  PyErr_Format(PyExc_ValueError,
     "Buffer acquisition failed on assignment; and then reacquiring the old buffer failed too!");
}

"""]


numpy_code = ["""
static int numpy_getbuffer(PyObject *obj, Py_buffer *view, int flags);
static void numpy_releasebuffer(PyObject *obj, Py_buffer *view);
""","""
static int numpy_getbuffer(PyObject *obj, Py_buffer *view, int flags) {
  /* This function is always called after a type-check; safe to cast */
  PyArrayObject *arr = (PyArrayObject*)obj;
  PyArray_Descr *type = (PyArray_Descr*)arr->descr;

  
  int typenum = PyArray_TYPE(obj);
  if (!PyTypeNum_ISNUMBER(typenum)) {
    PyErr_Format(PyExc_TypeError, "Only numeric NumPy types currently supported.");
    return -1;
  }

  /*
  NumPy format codes doesn't completely match buffer codes;
  seems safest to retranslate.
                            01234567890123456789012345*/
  const char* base_codes = "?bBhHiIlLqQfdgfdgO";

  char* format = (char*)malloc(4);
  char* fp = format;
  *fp++ = type->byteorder;
  if (PyTypeNum_ISCOMPLEX(typenum)) *fp++ = 'Z';
  *fp++ = base_codes[typenum];
  *fp = 0;

  view->buf = arr->data;
  view->readonly = !PyArray_ISWRITEABLE(obj);
  view->ndim = PyArray_NDIM(arr);
  view->strides = PyArray_STRIDES(arr);
  view->shape = PyArray_DIMS(arr);
  view->suboffsets = NULL;
  view->format = format;
  view->itemsize = type->elsize;

  view->internal = 0;
  return 0;
}

static void numpy_releasebuffer(PyObject *obj, Py_buffer *view) {
  free((char*)view->format);
  view->format = NULL;
}

"""]
