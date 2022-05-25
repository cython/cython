# mode: error

DEF t = (1,2,3)
DEF t_const = (1,t,2)
DEF t_non_const = (1,[1,2,3],3,t[4])

x = t_non_const

_ERRORS = u"""
5:32: Error in compile-time expression: IndexError: tuple index out of range
7:4: Invalid type for compile-time constant: [1, 2, 3] (type list)
"""
