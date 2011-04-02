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
3:0: break statement not inside loop
6:4: break statement not inside loop
9:4: break statement not inside loop
12:4: break statement not inside loop
17:5: break statement not inside loop
21:4: break statement not inside loop
23:4: break statement not inside loop
'''
