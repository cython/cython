Grail = cython.struct(
    age=cython.int,
    volume=cython.float)

def main():
    grail: Grail = Grail(5, 3.0)
    print(grail.age, grail.volume)
