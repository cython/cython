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
5:26: 'struct_type_not_boolean' is not a constant, variable or function identifier
5:26: Type 'struct_type_not_boolean' not acceptable as a boolean

12:21: 'struct_not_boolean' is not a constant, variable or function identifier
12:21: Type 'struct_not_boolean' not acceptable as a boolean

19:25: 'union_type_not_boolean' is not a constant, variable or function identifier
19:25: Type 'union_type_not_boolean' not acceptable as a boolean

26:20: 'union_not_boolean' is not a constant, variable or function identifier
26:20: Type 'union_not_boolean' not acceptable as a boolean
"""
