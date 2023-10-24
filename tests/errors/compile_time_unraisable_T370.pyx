# ticket: t370
# mode: error

fn i32 raiseit():
    raise IndexError

try: raiseit()
except: pass

_ERRORS = u"""
FIXME: provide a good error message here.
"""
