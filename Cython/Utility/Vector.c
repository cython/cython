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
            seen_c_ish++;
        } else {
            all_c_contig = 0;
            all_f_contig &= contig;
            seen_f_contig += all_f_contig;
            seen_f_ish++;
        }
    }

    if (all_c_contig || all_f_contig) {
        return __PYX_ARRAYS_ARE_CONTIG | all_c_contig;
    } else if (seen_c_contig + seen_f_contig == nops) {
        return __PYX_ARRAYS_ARE_MIXED_CONTIG | (seen_c_ish > seen_f_ish);
    } else if (seen_c_ish && seen_f_ish) {
        return __PYX_ARRAYS_ARE_MIXED_STRIDED | (seen_c_ish > seen_f_ish);
    } else {
        for (i = 0; i < nops; i++) {
            int dim = 0;
            if (seen_c_ish)
                dim = ndims[i] - 1;

            if (ops[i]->strides[dim] != itemsizes[i])
                return __PYX_ARRAYS_ARE_STRIDED | !!seen_c_ish;
        }
    }

    return __PYX_ARRAYS_ARE_INNER_CONTIG | !!seen_c_ish;
}

////////// RestrictUtility.proto //////////
#ifndef CYTHON_RESTRICT
  #if defined(__GNUC__)
    #define CYTHON_RESTRICT __restrict__
  #elif defined(_MSC_VER)
    #define CYTHON_RESTRICT __restrict
  #elif defined (__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
    #define CYTHON_RESTRICT restrict
  #else
    #define CYTHON_RESTRICT
  #endif
#endif

////////// OpenMPAutoTune.proto /////////
static CYTHON_INLINE int __pyx_compiled_with_openmp(void);
static CYTHON_INLINE void __pyx_test_sequential(double *a, int upper_limit);
static CYTHON_INLINE void __pyx_test_parallel(double *a, int upper_limit);

////////// OpenMPAutoTune /////////
static CYTHON_INLINE
int __pyx_compiled_with_openmp(void)
{
#ifdef _OPENMP
    return 1;
#else
    return 0;
#endif
}

static CYTHON_INLINE
void __pyx_test_sequential(double *a, const int upper_limit)
{
    int i;
    for (i = 0; i < upper_limit - 1; i++) {
        a[i] = a[i] + a[i + 1];
    }
}
static CYTHON_INLINE
void __pyx_test_parallel(double *a, const int upper_limit)
{
    int i;
    #ifdef _OPENMP
    #pragma omp parallel for
    #endif
    for (i = 0; i < upper_limit - 1; i++) {
        a[i] = a[i] + a[i + 1];
    }
}
