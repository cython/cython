
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
2:0: break statement not inside loop
5:4: break statement not inside loop
8:4: break statement not inside loop
11:4: break statement not inside loop
16:5: break statement not inside loop
20:4: break statement not inside loop
22:4: break statement not inside loop
'''
