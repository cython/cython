import cython

@cython.cclass
class CheeseShop:

    cheeses: object

    def __cinit__(self):
        self.cheeses = []

    @property
    def cheese(self):
        return f"We don't have: {self.cheeses}"

    @cheese.setter
    def cheese(self, value):
        self.cheeses.append(value)

    @cheese.deleter
    def cheese(self):
        del self.cheeses[:]

# Test input
from cheesy import CheeseShop

shop = CheeseShop()
print(shop.cheese)

shop.cheese = "camembert"
print(shop.cheese)

shop.cheese = "cheddar"
print(shop.cheese)

del shop.cheese
print(shop.cheese)
