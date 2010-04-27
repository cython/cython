
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
2:0: continue statement not inside loop
5:4: continue statement not inside loop
8:4: continue statement not inside loop
11:4: continue statement not inside loop
16:5: continue statement not inside loop
20:4: continue statement not inside loop
22:4: continue statement not inside loop
'''
