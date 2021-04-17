# ticket: t262
# mode: error

cdef class Album

cdef class SessionStruct:
     cdef Album _create_album(self, void* album, bint take_owner):
          pass

cdef class Album(SessionStruct):
     pass


_ERROR = u"""
"""
