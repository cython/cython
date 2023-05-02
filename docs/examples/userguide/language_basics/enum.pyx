cdef enum CheeseType:
    cheddar, edam,
    camembert

cdef enum CheeseState:
    hard = 1
    soft = 2
    runny = 3

print(CheeseType.cheddar)
print(CheeseState.hard)
