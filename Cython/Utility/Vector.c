////////// GetOrder.proto //////////

#define __PYX_ARRAY_C_ORDER 0x1

#define __PYX_ARRAYS_ARE_CONTIG 0x2
#define __PYX_ARRAYS_ARE_INNER_CONTIG 0x4
#define __PYX_ARRAYS_ARE_MIXED_CONTIG 0x10
#define __PYX_ARRAYS_ARE_STRIDED 0x20
#define __PYX_ARRAYS_ARE_MIXED_STRIDED 0x40

static int
__pyx_get_arrays_ordering(const {{memviewslice_name}} **ops, const int *ndims,
                          const Py_ssize_t *itemsizes, int nops);


////////// GetOrder //////////
static int
__pyx_get_arrays_ordering(const {{memviewslice_name}} **ops, const int *ndims,
                          const Py_ssize_t *itemsizes, int nops)
{
    int all_c_contig = 1;
    int all_f_contig = 1;
    int seen_c_contig = 0;
    int seen_f_contig = 0;
    int seen_c_ish = 0;
    int seen_f_ish = 0;

    int i;

    for (i = 0; i < nops; i++) {
        char order = __pyx_get_best_slice_order(*ops[i], ndims[i]);
        int contig = __pyx_memviewslice_is_contig2(*ops[i], 'C', ndims[i], itemsizes[i]);

        if (order == 'C') {
            all_f_contig = 0;
            all_c_contig &= contig;
            seen_c_contig += all_c_contig;
            seen_c_ish = 1;
        } else {
            all_c_contig = 0;
            all_f_contig &= contig;
            seen_f_contig += all_f_contig;
            seen_f_ish = 1;
        }
    }

    if (all_c_contig || all_f_contig) {
        return __PYX_ARRAYS_ARE_CONTIG | all_c_contig;
    } else if (seen_c_contig + seen_f_contig == nops) {
        return __PYX_ARRAYS_ARE_MIXED_CONTIG;
    } else if (seen_c_ish && seen_f_ish) {
        return __PYX_ARRAYS_ARE_MIXED_STRIDED;
    } else {
        for (i = 0; i < nops; i++) {
            int dim = 0;
            if (seen_c_ish)
                dim = ndims[i] - 1;

            if (ops[i]->strides[dim] != itemsizes[i])
                return __PYX_ARRAYS_ARE_STRIDED | seen_c_ish;
        }
    }

    return __PYX_ARRAYS_ARE_INNER_CONTIG | seen_c_ish;
}
