cdef extern from "graminit.c":
    ctypedef struct grammar:
        pass
    cdef grammar _PyParser_Grammar
    cdef int Py_file_input

cdef extern from "node.h":
    ctypedef struct node
    void PyNode_Free(node* n)
    int NCH(node* n)
    node* CHILD(node* n, int ix)
    node* RCHILD(node* n, int ix)
    short TYPE(node* n)
    char* STR(node* n)

cdef extern from "parsetok.h":
    ctypedef struct perrdetail:
        pass
    cdef void PyParser_SetError(perrdetail *err) except *
    cdef node * PyParser_ParseStringFlagsFilenameEx(
        const char * s,
        const char * filename,
        grammar * g,
        int start,
        perrdetail * err_ret,
        int * flags)

if sys.version_info < (3, 9):
    from distutils import sysconfig as _sysconfig

    class sysconfig(object):

        @staticmethod
        def get_path(name):
            assert name == 'include'
            return _sysconfig.get_python_inc()
else:
    # sysconfig can be trusted from cpython >= 3.8.7
    import sysconfig

import os
import re

def extract_names(path):
    # All parse tree types are #defined in these files as ints.
    type_names = {}
    with open(path) as fid:
        for line in fid:
            if line.startswith('#define'):
                try:
                    _, name, value = line.strip().split()
                    type_names[int(value)] = name
                except:
                    pass
    return type_names

cdef dict type_names = {}

cdef print_tree(node* n, indent=""):
    if not type_names:
        type_names.update(extract_names(
            os.path.join(sysconfig.get_path('include'), 'token.h')))
        type_names.update(extract_names(
            os.path.join(os.path.dirname(__file__), 'graminit.h')))

    print indent, type_names.get(TYPE(n), 'unknown'), <object>STR(n) if NCH(n) == 0 else NCH(n)
    indent += "  "
    for i in range(NCH(n)):
        print_tree(CHILD(n, i), indent)

def handle_includes(source, path):
    # TODO: Use include directory.
    def include_here(include_line):
        included = os.path.join(os.path.dirname(path), include_line.group(1)[1:-1])
        if not os.path.exists(included):
            return include_line.group(0) + ' # no such path: ' + included
        with open(included) as fid:
            return handle_includes(fid.read(), path)
    # TODO: Proper string tokenizing.
    return re.sub(r'^include\s+([^\n]+[\'"])\s*(#.*)?$', include_here, source, flags=re.M)

def p_module(path):
    cdef perrdetail err
    cdef int flags
    cdef node* n
    with open(path) as fid:
        source = fid.read()
    if '\ninclude ' in source:
        # TODO: Tokanizer needs to understand includes.
        source = handle_includes(source, path)
        path = "preparse(%s)" % path
    n = PyParser_ParseStringFlagsFilenameEx(
        source,
        path,
        &_PyParser_Grammar,
        Py_file_input,
        &err,
        &flags)
    if n:
#        print_tree(n)
        PyNode_Free(n)
    else:
        PyParser_SetError(&err)
