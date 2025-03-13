# ticket: t290

"""
>>> f()
(9, 9)
"""

cdef packed struct MyCdefStruct:
    char a
    double b

ctypedef packed struct MyCTypeDefStruct:
    char a
    double b

def f():
    return (sizeof(MyCdefStruct), sizeof(MyCTypeDefStruct))
