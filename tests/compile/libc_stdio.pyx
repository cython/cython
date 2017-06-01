# mode: compile

cimport libc.stdio
from libc cimport stdio
from libc.stdio cimport printf, puts, fputs, putchar, fputc, putc, stdout


with nogil:
    libc.stdio.printf("hello %s\n", b"world")
    stdio.printf("hello %s\n", b"world")
    printf("hello %s\n", b"world")
    printf("printf_output %d %d\n", 1, 2)
    puts("puts_output")
    fputs("fputs_output", stdout)
    putchar(b'z')
    fputc(b'x', stdout)
    putc(b'c', stdout)
