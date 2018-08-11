#include "C_func_file.h"

void multiply_by_10_in_C(double arr[], unsigned int n)
{
    unsigned int i;
    for (i = 0; i < n; i++) {
        arr[i] *= 10;
    }
}
