obj = [1, 2, 3]
l1 = cython.cast(list, obj)
l2 = cython.cast(list, obj, typecheck=True)
