# ticket: 135
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
7:0: Return not inside a function body
10:4: Return not inside a function body
13:4: Return not inside a function body
15:5: Return not inside a function body
18:5: Return not inside a function body
22:4: Return not inside a function body
25:4: Return not inside a function body
28:4: Return not inside a function body
30:4: Return not inside a function body
'''
