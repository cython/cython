#include "math.h"

double sinc(double x) {
    return x == 0 ? 1 : sin(x)/x;
}
