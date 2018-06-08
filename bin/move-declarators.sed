# Moves
#
# use: sed [-E | -r] -i -f move-declarators.sed [files]

# Arrays
# cdef int a[5] -> cdef int[5] a
s/^([ \t]*)cdef +([_0-9a-zA-Z. ]+) +([_0-9a-zA-Z]+)((\[[0-9]*\])+)$/\1cdef \2\4 \3/

# Pointers
# cdef int a, *b -> cdef int a \n cdef int *b

s/^([ \t]*)cdef +([_0-9a-zA-Z. ]+)( +[_0-9a-zA-Z]+ +(=[^()]+)?),( *[*]+ *)([^()]+)/\1cdef \2\3\
\1cdef \2\5\6/
s/^([ \t]*)cdef +([_0-9a-zA-Z. ]+)( +[_0-9a-zA-Z]+ +(=[^()]+)?),( *[*]+ *)([^()]+)/\1cdef \2\3\
\1cdef \2\5\6/
s/^([ \t]*)cdef +([_0-9a-zA-Z. ]+)( +[_0-9a-zA-Z]+ +(=[^()]+)?),( *[*]+ *)([^()]+)/\1cdef \2\3\
\1cdef \2\5\6/
s/^([ \t]*)cdef +([_0-9a-zA-Z. ]+)( +[_0-9a-zA-Z]+ +(=[^()]+)?),( *[*]+ *)([^()]+)/\1cdef \2\3\
\1cdef \2\5\6/
s/^([ \t]*)cdef +([_0-9a-zA-Z. ]+)( +[_0-9a-zA-Z]+ +(=[^()]+)?),( *[*]+ *)([^()]+)/\1cdef \2\3\
\1cdef \2\5\6/
