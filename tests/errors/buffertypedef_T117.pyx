# ticket: t117
# mode: error

ctypedef object[float] mybuffer

_ERRORS = u"""
1:0: Buffer vars not allowed in module scope
4:0: Buffer types only allowed as function local variables
"""
