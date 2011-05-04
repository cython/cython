# cython: remove_unreachable=False
# mode: error

break

class A:
    break

cdef class B:
    break

def test():
    break

try: break
except: pass

try: break
finally: pass

if bool_result():
    break
else:
    break

def bool_result():
    return True


_ERRORS = u'''
4:0: break statement not inside loop
7:4: break statement not inside loop
10:4: break statement not inside loop
13:4: break statement not inside loop
18:5: break statement not inside loop
22:4: break statement not inside loop
24:4: break statement not inside loop
'''
