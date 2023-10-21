cdef enum CheeseType:
    Cheddar, Edam,
    Camembert

cdef enum CheeseState:
    Hard = 1
    Soft = 2
    Runny = 3

print(CheeseType.Cheddar)
print(CheeseState.Hard)
