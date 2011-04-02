# mode: error

continue

class A:
    continue

cdef class B:
    continue

def test():
    continue

try: continue
except: pass

try: continue
finally: pass

if bool_result():
    continue
else:
    continue

def bool_result():
    return True

_ERRORS = u'''
3:0: continue statement not inside loop
6:4: continue statement not inside loop
9:4: continue statement not inside loop
12:4: continue statement not inside loop
17:5: continue statement not inside loop
21:4: continue statement not inside loop
23:4: continue statement not inside loop
'''
