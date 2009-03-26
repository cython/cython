
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

if True:
    return None
else:
    return None


_ERRORS = u'''
 2:0: Return not inside a function body
 5:4: Return not inside a function body
 8:4: Return not inside a function body
10:5: Return not inside a function body
13:5: Return not inside a function body
17:4: Return not inside a function body
20:4: Return not inside a function body
23:4: Return not inside a function body
25:4: Return not inside a function body
'''
