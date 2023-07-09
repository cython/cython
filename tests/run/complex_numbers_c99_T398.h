#if !defined(__cplusplus)
#if (defined(__STDC_VERSION__) && (__STDC_VERSION__ >= 199901L)) \
  || defined(__GNUC__)						 \
  || defined(__INTEL_COMPILER)					 \
  || defined(__IBMC__)						 \

#include <complex.h>
#if !defined(_Complex_I)
#error The "complex.h" header does not define the '_Complex_I' macro.
#error Please report this to Cython developers <cython-dev@codespeak.net>
#endif

#endif
#endif
#if (defined(__cplusplus) || (defined(__STDC_VERSION__) && (__STDC_VERSION__ >= 199901L)) \
  || defined(_MSC_VER))

// All these should be able to support CComplex  at this stage
// (along MSVC won't define _Complex_I)
#define CYTHON_CCOMPLEX 1
#endif
