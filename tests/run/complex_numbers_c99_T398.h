#if !defined(__cplusplus)
#if (defined(__STDC_VERSION__) && (__STDC_VERSION__ >= 199901L)) \
  || defined(__GNUC__)						 \
  || defined(__INTEL_COMPILER)					 \
  || defined(__IBMC__)						 \

#include <complex.h>
#if !defined(_Complex_I)
#error The "complex.h" header does not define the '_Complex_I' macro.
#error Please report this to Cython developers <github.com/cython/cython/issues>
#endif

#elif defined(_MSC_VER)
/* Although the MSVC compilers implementation of complex isn't
   compatible with Cython, it shouldn't cause Cython to define
   CYTHON_CCOMPLEX. Instead Cython should use it's own complex
   implementation.
 */
#include <complex.h>
#endif
#endif
