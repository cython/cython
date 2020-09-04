cdef extern from *:
    cpdef enum: # ExternPxd
        FOUR "4"
        EIGHT "8"

    cdef enum: # ExternSecretPxd
        SIXTEEN "16"

cpdef enum PxdEnum:
    RANK_0 = 11
    RANK_1 = 37
    RANK_2 = 389

cpdef enum cpdefPxdDocEnum:
    """Home is where...
    """
    RANK_6 = 159

cpdef enum cpdefPxdDocLineEnum:
    """Home is where..."""
    RANK_7 = 889

cdef enum PxdSecretEnum:
    RANK_8 = 5077

cdef enum cdefPxdDocEnum:
    """the heart is.
    """
    RANK_9 = 2458
