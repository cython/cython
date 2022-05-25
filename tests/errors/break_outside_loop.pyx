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


def break_after_loop():
    for _ in range(2):
        pass

    if bool_result():
        break

    try:
        if bool_result():
            break
    except Exception:
        pass

    if bool_result():
        break


_ERRORS = u'''
4:0: break statement not inside loop
7:4: break statement not inside loop
10:4: break statement not inside loop
13:4: break statement not inside loop
15:5: break statement not inside loop
18:5: break statement not inside loop
22:4: break statement not inside loop
24:4: break statement not inside loop
35:8: break statement not inside loop
39:12: break statement not inside loop
44:8: break statement not inside loop
'''
