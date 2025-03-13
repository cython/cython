# cython: remove_unreachable=False
# ticket: t135
# mode: error

def _runtime_True():
    return True

return 'bar'

class A:
    return None

cdef class B:
    return None

try: return None
except: pass

try: return None
finally: pass

for i in (1,2):
    return None

while True:
    return None

if _runtime_True():
    return None
else:
    return None


_ERRORS = u'''
8:0: Return not inside a function body
11:4: Return not inside a function body
14:4: Return not inside a function body
16:5: Return not inside a function body
19:5: Return not inside a function body
23:4: Return not inside a function body
26:4: Return not inside a function body
29:4: Return not inside a function body
31:4: Return not inside a function body
'''
