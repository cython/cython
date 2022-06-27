typedef struct {
    int field1;
    int field2;
    int newly_added_field;
} StructType;

static StructType global_struct;

static StructType *get_struct_ptr() {
    return &global_struct;
}

#define C_LIB_VERSION 20
