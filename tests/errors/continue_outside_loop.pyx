# cython: remove_unreachable=False
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


_ERRORS = '''
4:0: continue statement not inside loop
7:4: continue statement not inside loop
10:4: continue statement not inside loop
13:4: continue statement not inside loop
15:5: continue statement not inside loop
18:5: continue statement not inside loop
22:4: continue statement not inside loop
24:4: continue statement not inside loop
'''
