# ticket: 307
# mode: error

nonexisting(3, with_kw_arg=4)

_ERRORS = u"""
4:0: undeclared name not builtin: nonexisting
"""
