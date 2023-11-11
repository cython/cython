Food = cython.union(
    spam=cython.p_char,
    eggs=cython.p_float)

def main():
    arr: cython.p_float = [1.0, 2.0]
    spam: Food = Food(spam='b')
    eggs: Food = Food(eggs=arr)
    print(spam.spam, eggs.eggs[0])
