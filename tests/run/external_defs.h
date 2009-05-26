
typedef float FloatTypedef;
typedef double DoubleTypedef;
typedef long double LongDoubleTypedef;

typedef char CharTypedef;
typedef short ShortTypedef;
typedef int IntTypedef;
typedef long LongTypedef;
#if defined(T_LONGLONG)
typedef PY_LONG_LONG LongLongTypedef;
#else
typedef long LongLongTypedef;
#endif

typedef unsigned char UCharTypedef;
typedef unsigned short UShortTypedef;
typedef unsigned int UIntTypedef;
typedef unsigned long ULongTypedef;
#if defined(T_LONGLONG)
typedef unsigned PY_LONG_LONG ULongLongTypedef;
#else
typedef unsigned long ULongLongTypedef;
#endif
