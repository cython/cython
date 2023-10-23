# mode: error
# tag: cpp, cpp11

fn foo(object& x): pass
fn bar(object&& x): pass

_ERRORS="""
4:13: Reference base type cannot be a Python object
5:13: Rvalue-reference base type cannot be a Python object
"""
