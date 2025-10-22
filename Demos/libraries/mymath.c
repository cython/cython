#include <math.h>
#include "mymath.h"

DLL_EXPORT double sinc(double x) {
    return x == 0 ? 1 : sin(x)/x;
}
