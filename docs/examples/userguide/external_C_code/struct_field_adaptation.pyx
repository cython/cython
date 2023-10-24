extern from "struct_field_adaptation.h":
    """
    #define HAS_NEWLY_ADDED_FIELD  (C_LIB_VERSION >= 20)

    #if HAS_NEWLY_ADDED_FIELD
        #define _mylib_get_newly_added_field(a_struct_ptr)  ((a_struct_ptr)->newly_added_field)
        #define _mylib_set_newly_added_field(a_struct_ptr, value)  ((a_struct_ptr)->newly_added_field) = (value)
    #else
        #define _mylib_get_newly_added_field(a_struct_ptr)  (0)
        #define _mylib_set_newly_added_field(a_struct_ptr, value)  ((void) (value))
    #endif
    """

    # Normal declarations provided by the C header file:
    ctypedef struct StructType:
        i32 field1
        i32 field2

    fn StructType *get_struct_ptr()

    # Special declarations conditionally provided above:
    fn bint HAS_NEWLY_ADDED_FIELD
    fn i32 get_newly_added_field "_mylib_get_newly_added_field" (StructType *struct_ptr)
    fn void set_newly_added_field "_mylib_set_newly_added_field" (StructType *struct_ptr, i32 value)


cdef StructType *some_struct_ptr = get_struct_ptr()

print(some_struct_ptr.field1)
if HAS_NEWLY_ADDED_FIELD:
    print(get_newly_added_field(some_struct_ptr))
