cdef class UnicodeLiteralBuilder:
    cdef public list chars

    cpdef append(self, characters)
    cpdef append_charval(self, char_number)
    cpdef getstring(self)


cdef class BytesLiteralBuilder:
    cdef public list chars
    cdef public str target_encoding

    cpdef append(self, characters)
    cpdef append_charval(self, char_number)
    cpdef getstring(self)


cdef class StrLiteralBuilder:
    cdef BytesLiteralBuilder _bytes
    cdef UnicodeLiteralBuilder _unicode

    cpdef append(self, characters)
    cpdef append_charval(self, char_number)
