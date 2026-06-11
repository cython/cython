# mode: error
# tag: ccall,generator,async
"""
Error cases for @ccall / auto_cpdef on generator and async functions.
"""
import cython


# @ccall on async def → compile error
@cython.ccall
async def async_ccall():
    yield 1


_ERRORS = """
10:0: @ccall is not supported for async functions
"""
