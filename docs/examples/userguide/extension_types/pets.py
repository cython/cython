import cython

@cython.cclass
class Parrot:

    @cython.cfunc
    def describe(self) -> cython.void:
        print("This parrot is resting.")

@cython.cclass
class Norwegian(Parrot):

    @cython.cfunc
    def describe(self) -> cython.void:
        Parrot.describe(self)
        print("Lovely plumage!")

cython.declare(p1=Parrot, p2=Parrot)
p1 = Parrot()
p2 = Norwegian()
print("p2:")
p2.describe()
