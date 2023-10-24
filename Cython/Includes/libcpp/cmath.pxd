extern from "<cmath>" namespace "std" nogil:
    # all C99 functions
    fn f32 acos(f32 x) except +
    fn f64 acos(f64 x) except +
    fn long double acos(long double x) except +
    fn f32 acosf(f32 x) except +
    fn long double acosl(long double x) except +

    fn f32 asin(f32 x) except +
    fn f64 asin(f64 x) except +
    fn long double asin(long double x) except +
    fn f32 asinf(f32 x) except +
    fn long double asinl(long double x) except +

    fn f32 atan(f32 x) except +
    fn f64 atan(f64 x) except +
    fn long double atan(long double x) except +
    fn f32 atanf(f32 x) except +
    fn long double atanl(long double x) except +

    fn f32 atan2(f32 y, f32 x) except +
    fn f64 atan2(f64 y, f64 x) except +
    fn long double atan2(long double y, long double x) except +
    fn f32 atan2f(f32 y, f32 x) except +
    fn long double atan2l(long double y, long double x) except +

    fn f32 cos(f32 x) except +
    fn f64 cos(f64 x) except +
    fn long double cos(long double x) except +
    fn f32 cosf(f32 x) except +
    fn long double cosl(long double x) except +

    fn f32 sin(f32 x) except +
    fn f64 sin(f64 x) except +
    fn long double sin(long double x) except +
    fn f32 sinf(f32 x) except +
    fn long double sinl(long double x) except +

    fn f32 tan(f32 x) except +
    fn f64 tan(f64 x) except +
    fn long double tan(long double x) except +
    fn f32 tanf(f32 x) except +
    fn long double tanl(long double x) except +

    fn f32 acosh(f32 x) except +
    fn f64 acosh(f64 x) except +
    fn long double acosh(long double x) except +
    fn f32 acoshf(f32 x) except +
    fn long double acoshl(long double x) except +

    fn f32 asinh(f32 x) except +
    fn f64 asinh(f64 x) except +
    fn long double asinh(long double x) except +
    fn f32 asinhf(f32 x) except +
    fn long double asinhl(long double x) except +

    fn f32 atanh(f32 x) except +
    fn f64 atanh(f64 x) except +
    fn long double atanh(long double x) except +
    fn f32 atanhf(f32 x) except +
    fn long double atanhl(long double x) except +

    fn f32 cosh(f32 x) except +
    fn f64 cosh(f64 x) except +
    fn long double cosh(long double x) except +
    fn f32 coshf(f32 x) except +
    fn long double coshl(long double x) except +

    fn f32 sinh(f32 x) except +
    fn f64 sinh(f64 x) except +
    fn long double sinh(long double x) except +
    fn f32 sinhf(f32 x) except +
    fn long double sinhl(long double x) except +

    fn f32 tanh(f32 x) except +
    fn f64 tanh(f64 x) except +
    fn long double tanh(long double x) except +
    fn f32 tanhf(f32 x) except +
    fn long double tanhl(long double x) except +

    fn f32 exp(f32 x) except +
    fn f64 exp(f64 x) except +
    fn long double exp(long double x) except +
    fn f32 expf(f32 x) except +
    fn long double expl(long double x) except +

    fn f32 exp2(f32 x) except +
    fn f64 exp2(f64 x) except +
    fn long double exp2(long double x) except +
    fn f32 exp2f(f32 x) except +
    fn long double exp2l(long double x) except +

    fn f32 expm1(f32 x) except +
    fn f64 expm1(f64 x) except +
    fn long double expm1(long double x) except +
    fn f32 expm1f(f32 x) except +
    fn long double expm1l(long double x) except +

    fn f32 frexp(f32 value, i32* exp) except +
    fn f64 frexp(f64 value, i32* exp) except +
    fn long double frexp(long double value, i32* exp) except +
    fn f32 frexpf(f32 value, i32* exp) except +
    fn long double frexpl(long double value, i32* exp) except +

    fn int ilogb(f32 x) except +
    fn int ilogb(f64 x) except +
    fn int ilogb(long double x) except +
    fn int ilogbf(f32 x) except +
    fn int ilogbl(long double x) except +

    fn f32 ldexp(f32 x, i32 exp) except +
    fn f64 ldexp(f64 x, i32 exp) except +
    fn long double ldexp(long double x, i32 exp) except +
    fn f32 ldexpf(f32 x, i32 exp) except +
    fn long double ldexpl(long double x, i32 exp) except +

    fn f32 log(f32 x) except +
    fn f64 log(f64 x) except +
    fn long double log(long double x) except +
    fn f32 logf(f32 x) except +
    fn long double logl(long double x) except +

    fn f32 log10(f32 x) except +
    fn f64 log10(f64 x) except +
    fn long double log10(long double x) except +
    fn f32 log10f(f32 x) except +
    fn long double log10l(long double x) except +

    fn f32 log1p(f32 x) except +
    fn f64 log1p(f64 x) except +
    fn long double log1p(long double x) except +
    fn f32 log1pf(f32 x) except +
    fn long double log1pl(long double x) except +

    fn f32 log2(f32 x) except +
    fn f64 log2(f64 x) except +
    fn long double log2(long double x) except +
    fn f32 log2f(f32 x) except +
    fn long double log2l(long double x) except +

    fn f32 logb(f32 x) except +
    fn f64 logb(f64 x) except +
    fn long double logb(long double x) except +
    fn f32 logbf(f32 x) except +
    fn long double logbl(long double x) except +

    fn f32 modf(f32 value, f32* iptr) except +
    fn f64 modf(f64 value, double* iptr) except +
    fn long double modf(long double value, long double* iptr) except +
    fn f32 modff(f32 value, f32* iptr) except +
    fn long double modfl(long double value, long double* iptr) except +

    fn f32 scalbn(f32 x, i32 n) except +
    fn f64 scalbn(f64 x, i32 n) except +
    fn long double scalbn(long double x, i32 n) except +
    fn f32 scalbnf(f32 x, i32 n) except +
    fn long double scalbnl(long double x, i32 n) except +

    fn f32 scalbln(f32 x, i64 n) except +
    fn f64 scalbln(f64 x, i64 n) except +
    fn long double scalbln(long double x, i64 n) except +
    fn f32 scalblnf(f32 x, i64 n) except +
    fn long double scalblnl(long double x, i64 n) except +

    fn f32 cbrt(f32 x) except +
    fn f64 cbrt(f64 x) except +
    fn long double cbrt(long double x) except +
    fn f32 cbrtf(f32 x) except +
    fn long double cbrtl(long double x) except +

    # absolute values
    fn i32 abs(i32 j) except +
    fn i64 abs(i64 j) except +
    fn i128 abs(i128 j) except +
    fn f32 abs(f32 j) except +
    fn f64 abs(f64 j) except +
    fn long double abs(long double j) except +

    fn f32 fabs(f32 x) except +
    fn f64 fabs(f64 x) except +
    fn long double fabs(long double x) except +
    fn f32 fabsf(f32 x) except +
    fn long double fabsl(long double x) except +

    fn f32 hypot(f32 x, f32 y) except +
    fn f64 hypot(f64 x, f64 y) except +
    fn long double hypot(long double x, long double y) except +
    fn f32 hypotf(f32 x, f32 y) except +
    fn long double hypotl(long double x, long double y) except +

    # C++17 three-dimensional hypotenuse
    fn f32 hypot(f32 x, f32 y, f32 z) except +
    fn f64 hypot(f64 x, f64 y, f64 z) except +
    fn long double hypot(long double x, long double y, long double z) except +

    fn f32 pow(f32 x, f32 y) except +
    fn f64 pow(f64 x, f64 y) except +
    fn long double pow(long double x, long double y) except +
    fn f32 powf(f32 x, f32 y) except +
    fn long double powl(long double x, long double y) except +

    fn f32 sqrt(f32 x) except +
    fn f64 sqrt(f64 x) except +
    fn long double sqrt(long double x) except +
    fn f32 sqrtf(f32 x) except +
    fn long double sqrtl(long double x) except +

    fn f32 erf(f32 x) except +
    fn f64 erf(f64 x) except +
    fn long double erf(long double x) except +
    fn f32 erff(f32 x) except +
    fn long double erfl(long double x) except +

    fn f32 erfc(f32 x) except +
    fn f64 erfc(f64 x) except +
    fn long double erfc(long double x) except +
    fn f32 erfcf(f32 x) except +
    fn long double erfcl(long double x) except +

    fn f32 lgamma(f32 x) except +
    fn f64 lgamma(f64 x) except +
    fn long double lgamma(long double x) except +
    fn f32 lgammaf(f32 x) except +
    fn long double lgammal(long double x) except +

    fn f32 tgamma(f32 x) except +
    fn f64 tgamma(f64 x) except +
    fn long double tgamma(long double x) except +
    fn f32 tgammaf(f32 x) except +
    fn long double tgammal(long double x) except +

    fn f32 ceil(f32 x) except +
    fn f64 ceil(f64 x) except +
    fn long double ceil(long double x) except +
    fn f32 ceilf(f32 x) except +
    fn long double ceill(long double x) except +

    fn f32 floor(f32 x) except +
    fn f64 floor(f64 x) except +
    fn long double floor(long double x) except +
    fn f32 floorf(f32 x) except +
    fn long double floorl(long double x) except +

    fn f32 nearbyint(f32 x) except +
    fn f64 nearbyint(f64 x) except +
    fn long double nearbyint(long double x) except +
    fn f32 nearbyintf(f32 x) except +
    fn long double nearbyintl(long double x) except +

    fn f32 rint(f32 x) except +
    fn f64 rint(f64 x) except +
    fn long double rint(long double x) except +
    fn f32 rintf(f32 x) except +
    fn long double rintl(long double x) except +

    fn i64 lrint(f32 x) except +
    fn i64 lrint(f64 x) except +
    fn i64 lrint(long double x) except +
    fn i64 lrintf(f32 x) except +
    fn i64 lrintl(long double x) except +

    fn i128 llrint(f32 x) except +
    fn i128 llrint(f64 x) except +
    fn i128 llrint(long double x) except +
    fn i128 llrintf(f32 x) except +
    fn i128 llrintl(long double x) except +

    fn f32 round(f32 x) except +
    fn f64 round(f64 x) except +
    fn long double round(long double x) except +
    fn f32 roundf(f32 x) except +
    fn long double roundl(long double x) except +

    fn i64 lround(f32 x) except +
    fn i64 lround(f64 x) except +
    fn i64 lround(long double x) except +
    fn i64 lroundf(f32 x) except +
    fn i64 lroundl(long double x) except +

    fn i128 llround(f32 x) except +
    fn i128 llround(f64 x) except +
    fn i128 llround(long double x) except +
    fn i128 llroundf(f32 x) except +
    fn i128 llroundl(long double x) except +

    fn f32 trunc(f32 x) except +
    fn f64 trunc(f64 x) except +
    fn long double trunc(long double x) except +
    fn f32 truncf(f32 x) except +
    fn long double truncl(long double x) except +

    fn f32 fmod(f32 x, f32 y) except +
    fn f64 fmod(f64 x, f64 y) except +
    fn long double fmod(long double x, long double y) except +
    fn f32 fmodf(f32 x, f32 y) except +
    fn long double fmodl(long double x, long double y) except +

    fn f32 remainder(f32 x, f32 y) except +
    fn f64 remainder(f64 x, f64 y) except +
    fn long double remainder(long double x, long double y) except +
    fn f32 remainderf(f32 x, f32 y) except +
    fn long double remainderl(long double x, long double y) except +

    fn f32 remquo(f32 x, f32 y, i32* quo) except +
    fn f64 remquo(f64 x, f64 y, i32* quo) except +
    fn long double remquo(long double x, long double y, i32* quo) except +
    fn f32 remquof(f32 x, f32 y, i32* quo) except +
    fn long double remquol(long double x, long double y, i32* quo) except +

    fn f32 copysign(f32 x, f32 y) except +
    fn f64 copysign(f64 x, f64 y) except +
    fn long double copysign(long double x, long double y) except +
    fn f32 copysignf(f32 x, f32 y) except +
    fn long double copysignl(long double x, long double y) except +

    fn f64 nan(const char* tagp) except +
    fn f32 nanf(const char* tagp) except +
    fn long double nanl(const char* tagp) except +

    fn f32 nextafter(f32 x, f32 y) except +
    fn f64 nextafter(f64 x, f64 y) except +
    fn long double nextafter(long double x, long double y) except +
    fn f32 nextafterf(f32 x, f32 y) except +
    fn long double nextafterl(long double x, long double y) except +

    fn f32 nexttoward(f32 x, long double y) except +
    fn f64 nexttoward(f64 x, long double y) except +
    fn long double nexttoward(long double x, long double y) except +
    fn f32 nexttowardf(f32 x, long double y) except +
    fn long double nexttowardl(long double x, long double y) except +

    fn f32 fdim(f32 x, f32 y) except +
    fn f64 fdim(f64 x, f64 y) except +
    fn long double fdim(long double x, long double y) except +
    fn f32 fdimf(f32 x, f32 y) except +
    fn long double fdiml(long double x, long double y) except +

    fn f32 fmax(f32 x, f32 y) except +
    fn f64 fmax(f64 x, f64 y) except +
    fn long double fmax(long double x, long double y) except +
    fn f32 fmaxf(f32 x, f32 y) except +
    fn long double fmaxl(long double x, long double y) except +

    fn f32 fmin(f32 x, f32 y) except +
    fn f64 fmin(f64 x, f64 y) except +
    fn long double fmin(long double x, long double y) except +
    fn f32 fminf(f32 x, f32 y) except +
    fn long double fminl(long double x, long double y) except +

    fn f32 fma(f32 x, f32 y, f32 z) except +
    fn f64 fma(f64 x, f64 y, f64 z) except +
    fn long double fma(long double x, long double y, long double z) except +
    fn f32 fmaf(f32 x, f32 y, f32 z) except +
    fn long double fmal(long double x, long double y, long double z) except +

    # C++20 linear interpolation
    fn f32 lerp(f32 a, f32 b, f32 t)
    fn f64 lerp(f64 a, f64 b, f64 t)
    fn long double lerp(long double a, long double b, long double t)

    # classification / comparison functions
    fn i32 fpclassify(f32 x) except +
    fn i32 fpclassify(f64 x) except +
    fn i32 fpclassify(long double x) except +

    fn bint isfinite(f32 x) except +
    fn bint isfinite(f64 x) except +
    fn bint isfinite(long double x) except +

    fn bint isinf(f32 x) except +
    fn bint isinf(f64 x) except +
    fn bint isinf(long double x) except +

    fn bint isnan(f32 x) except +
    fn bint isnan(f64 x) except +
    fn bint isnan(long double x) except +

    fn bint isnormal(f32 x) except +
    fn bint isnormal(f64 x) except +
    fn bint isnormal(long double x) except +

    fn bint signbit(f32 x) except +
    fn bint signbit(f64 x) except +
    fn bint signbit(long double x) except +

    fn bint isgreater(f32 x, f32 y) except +
    fn bint isgreater(f64 x, f64 y) except +
    fn bint isgreater(long double x, long double y) except +

    fn bint isgreaterequal(f32 x, f32 y) except +
    fn bint isgreaterequal(f64 x, f64 y) except +
    fn bint isgreaterequal(long double x, long double y) except +

    fn bint isless(f32 x, f32 y) except +
    fn bint isless(f64 x, f64 y) except +
    fn bint isless(long double x, long double y) except +

    fn bint islessequal(f32 x, f32 y) except +
    fn bint islessequal(f64 x, f64 y) except +
    fn bint islessequal(long double x, long double y) except +

    fn bint islessgreater(f32 x, f32 y) except +
    fn bint islessgreater(f64 x, f64 y) except +
    fn bint islessgreater(long double x, long double y) except +

    fn bint isunordered(f32 x, f32 y) except +
    fn bint isunordered(f64 x, f64 y) except +
    fn bint isunordered(long double x, long double y) except +

    # C++17 mathematical special functions

    # associated Laguerre polynomials
    fn f64          assoc_laguerre(u32 n, u32 m, f64 x) except +
    fn f32          assoc_laguerref(u32 n, u32 m, f32 x) except +
    fn long double  assoc_laguerrel(u32 n, u32 m, long double x) except +

    # associated Legendre functions
    fn f64          assoc_legendre(u32 l, u32 m, f64 x) except +
    fn f32          assoc_legendref(u32 l, u32 m, f32 x) except +
    fn long double  assoc_legendrel(u32 l, u32 m, long double x) except +

    # beta function
    fn f64          beta(f64 x, f64 y) except +
    fn f32          betaf(f32 x, f32 y) except +
    fn long double  betal(long double x, long double y) except +

    # complete elliptic integral of the first kind
    fn f64          comp_ellint_1(f64 k) except +
    fn f32          comp_ellint_1f(f32 k) except +
    fn long double  comp_ellint_1l(long double k) except +

    # complete elliptic integral of the second kind
    fn f64          comp_ellint_2(f64 k) except +
    fn f32          comp_ellint_2f(f32 k) except +
    fn long double  comp_ellint_2l(long double k) except +

    # complete elliptic integral of the third kind
    fn f64          comp_ellint_3(f64 k, f64 nu) except +
    fn f32          comp_ellint_3f(f32 k, f32 nu) except +
    fn long double  comp_ellint_3l(long double k, long double nu) except +

    # regular modified cylindrical Bessel functions
    fn f64          cyl_bessel_i(f64 nu, f64 x) except +
    fn f32          cyl_bessel_if(f32 nu, f32 x) except +
    fn long double  cyl_bessel_il(long double nu, long double x) except +

    # cylindrical Bessel functions of the first kind
    fn f64          cyl_bessel_j(f64 nu, f64 x) except +
    fn f32          cyl_bessel_jf(f32 nu, f32 x) except +
    fn long double  cyl_bessel_jl(long double nu, long double x) except +

    # irregular modified cylindrical Bessel functions
    fn f64          cyl_bessel_k(f64 nu, f64 x) except +
    fn f32          cyl_bessel_kf(f32 nu, f32 x) except +
    fn long double  cyl_bessel_kl(long double nu, long double x) except +

    # cylindrical Neumann functions
    # cylindrical Bessel functions of the second kind
    fn f64          cyl_neumann(f64 nu, f64 x) except +
    fn f32          cyl_neumannf(f32 nu, f32 x) except +
    fn long double  cyl_neumannl(long double nu, long double x) except +

    # incomplete elliptic integral of the first kind
    fn f64          ellint_1(f64 k, f64 phi) except +
    fn f32          ellint_1f(f32 k, f32 phi) except +
    fn long double  ellint_1l(long double k, long double phi) except +

    # incomplete elliptic integral of the second kind
    fn f64          ellint_2(f64 k, f64 phi) except +
    fn f32          ellint_2f(f32 k, f32 phi) except +
    fn long double  ellint_2l(long double k, long double phi) except +

    # incomplete elliptic integral of the third kind
    fn f64          ellint_3(f64 k, f64 nu, f64 phi) except +
    fn f32          ellint_3f(f32 k, f32 nu, f32 phi) except +
    fn long double  ellint_3l(long double k, long double nu, long double phi) except +

    # exponential integral
    fn f64          expint(f64 x) except +
    fn f32          expintf(f32 x) except +
    fn long double  expintl(long double x) except +

    # Hermite polynomials
    fn f64          hermite(u32 n, f64 x) except +
    fn f32          hermitef(u32 n, f32 x) except +
    fn long double  hermitel(u32 n, long double x) except +

    # Laguerre polynomials
    fn f64          laguerre(u32 n, f64 x) except +
    fn f32          laguerref(u32 n, f32 x) except +
    fn long double  laguerrel(u32 n, long double x) except +

    # Legendre polynomials
    fn f64          legendre(u32 l, f64 x) except +
    fn f32          legendref(u32 l, f32 x) except +
    fn long double  legendrel(u32 l, long double x) except +

    # Riemann zeta function
    fn f64          riemann_zeta(f64 x) except +
    fn f32          riemann_zetaf(f32 x) except +
    fn long double  riemann_zetal(long double x) except +

    # spherical Bessel functions of the first kind
    fn f64          sph_bessel(u32 n, f64 x) except +
    fn f32          sph_besself(u32 n, f32 x) except +
    fn long double  sph_bessell(u32 n, long double x) except +

    # spherical associated Legendre functions
    fn f64          sph_legendre(u32 l, u32 m, f64 theta) except +
    fn f32          sph_legendref(u32 l, u32 m, f32 theta) except +
    fn long double  sph_legendrel(u32 l, u32 m, long double theta) except +

    # spherical Neumann functions
    # spherical Bessel functions of the second kind
    fn f64          sph_neumann(u32 n, f64 x) except +
    fn f32          sph_neumannf(u32 n, f32 x) except +
    fn long double  sph_neumannl(u32 n, long double x) except +
