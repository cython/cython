cimport libc

cimport libc.stdio
cimport libc.errno
cimport libc.float
cimport libc.limits
cimport libc.locale
cimport libc.signal
cimport libc.stddef
cimport libc.stdint
cimport libc.stdio
cimport libc.stdlib
cimport libc.string

from libc cimport errno
from libc cimport float
from libc cimport limits
from libc cimport locale
from libc cimport signal
from libc cimport stddef
from libc cimport stdint
from libc cimport stdio
from libc cimport stdlib
from libc cimport string

from libc.errno  cimport *
from libc.float  cimport *
from libc.limits cimport *
from libc.locale cimport *
from libc.signal cimport *
from libc.stddef cimport *
from libc.stdint cimport *
from libc.stdio  cimport *
from libc.stdlib cimport *
from libc.string cimport *

libc.stdio.printf("hello\n")
stdio.printf("hello\n")
printf("hello\n")
