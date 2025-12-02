# distutils: sources = embedded_main.c
# tag: py3only
# tag: no-cpp

TEXT_TO_SAY = 'Hello from Python!'

@cython.public
@cython.exceptval(-1)
def say_hello_from_python() -> cython.int:
    print(TEXT_TO_SAY)
    return 0
