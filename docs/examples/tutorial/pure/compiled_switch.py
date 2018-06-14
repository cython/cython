import cython

if cython.compiled:
    print("Yep, I'm compiled.")
else:
    print("Just a lowly interpreted script.")
