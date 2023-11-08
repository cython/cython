import timeit

import integrate0, integrate1, integrate2

number = 10
py_time = None
for m in ('integrate0', 'integrate1', 'integrate2'):
    print(m)
    t = min(timeit.repeat("integrate_f(0.0, 10.0, 100000)", f"from {m} import integrate_f", number=number))
    if py_time is None:
        py_time = t
    print("    ", t / number, "s")
    print("    ", py_time / t)
