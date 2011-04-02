# mode: error

ctypedef struct struct_type_not_boolean:
    int i
    float f

if struct_type_not_boolean:
    print("INVALID CODE")

cdef struct struct_not_boolean:
    int i
    float f

if struct_not_boolean:
    print("INVALID CODE")

ctypedef union union_type_not_boolean:
    int i
    float f

if union_type_not_boolean:
    print("INVALID CODE")

cdef union union_not_boolean:
    int i
    float f

if union_not_boolean:
    print("INVALID CODE")


_ERRORS = u"""
7:26: 'struct_type_not_boolean' is not a constant, variable or function identifier
7:26: Type 'struct_type_not_boolean' not acceptable as a boolean

14:21: 'struct_not_boolean' is not a constant, variable or function identifier
14:21: Type 'struct_not_boolean' not acceptable as a boolean

21:25: 'union_type_not_boolean' is not a constant, variable or function identifier
21:25: Type 'union_type_not_boolean' not acceptable as a boolean

28:20: 'union_not_boolean' is not a constant, variable or function identifier
28:20: Type 'union_not_boolean' not acceptable as a boolean
"""
