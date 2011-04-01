# mode: compile

from libc.errno  cimport *

if errno == EDOM   : pass
if errno == EILSEQ : pass
if errno == ERANGE : pass

errno = 0
