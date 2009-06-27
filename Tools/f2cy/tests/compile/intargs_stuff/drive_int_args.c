#include <stdio.h>

void *int_args_subr(signed char *, short *, int *, long *);
long int_args_func(signed char *, short *, int *, long *);

int main(int argc, char **argv) {

    signed char a = 1;
    short b = 2;
    int  c = 4;
    long  d = 8;
    long result = 0;

    printf("before subr call in c\n");
    printf("%hhd %hd %d %ld\n", a,b,c,d);
    int_args_subr(&a, &b, &c, &d);
    printf("after subr call in c\n");
    printf("%hhd %hd %d %ld\n", a,b,c,d);

    printf("before func call in c\n");
    printf("%hhd %hd %d %ld\n", a,b,c,d);
    result = int_args_func(&a, &b, &c, &d);
    printf("after func call in c\n");
    printf("%hhd %hd %d %ld result=%ld\n", a,b,c,d, result);

    return 0;
}
    
