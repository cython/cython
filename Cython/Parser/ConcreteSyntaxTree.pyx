cdef extern from "graminit.c":
    ctypedef struct grammar:
        pass
    cdef grammar _PyParser_Grammar
    cdef int Py_file_input

cdef extern from "node.h":
    ctypedef struct node
    void PyNode_Free(node*)
    int NCH(node*)
    node* CHILD(node*, int)
    node* RCHILD(node*, int)
    short TYPE(node*)
    char* STR(node*)

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

import distutils.sysconfig
import os

def extract_names(path):
    # All parse tree types are #defined in these files as ints.
    type_names = {}
    for line in open(path):
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
            os.path.join(distutils.sysconfig.get_python_inc(), 'token.h')))
        type_names.update(extract_names(
            os.path.join(os.path.dirname(__file__), 'graminit.h')))

    print indent, type_names.get(TYPE(n), 'unknown'), <object>STR(n) if NCH(n) == 0 else NCH(n)
    indent += "  "
    for i in range(NCH(n)):
        print_tree(CHILD(n, i), indent)

def p_module(path):
    cdef perrdetail err
    cdef int flags
    cdef node* n
    source = open(path).read()
    n = PyParser_ParseStringFlagsFilenameEx(
        source,
        path,
        &_PyParser_Grammar,
        Py_file_input,
        &err,
        &flags)
    if n:
        print_tree(n)
        PyNode_Free(n)
    else:
        PyParser_SetError(&err)
