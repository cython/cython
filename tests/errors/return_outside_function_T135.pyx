
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
 5:0: Return not inside a function body
 8:4: Return not inside a function body
11:4: Return not inside a function body
13:5: Return not inside a function body
16:5: Return not inside a function body
20:4: Return not inside a function body
23:4: Return not inside a function body
26:4: Return not inside a function body
28:4: Return not inside a function body
'''
