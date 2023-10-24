# cython: remove_unreachable=false
# mode: error

def f(a, b):
    let i32 i
    break  # error
    continue  # error

_ERRORS = u"""
6:4: break statement not inside loop
7:4: continue statement not inside loop
"""
