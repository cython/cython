#pragma once
#ifdef DEFINE_NO_VALUE
#define VAL (DEFINE_WITH_VALUE + 1)
#else
#define VAL DEFINE_WITH_VALUE
#endif
