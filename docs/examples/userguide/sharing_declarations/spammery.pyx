 
from volume cimport cube

def menu(description, size):
    print(description, ":", cube(size),
          "cubic metres of spam")

menu("Entree", 1)
menu("Main course", 3)
menu("Dessert", 2)
