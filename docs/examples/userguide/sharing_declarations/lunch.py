import cython
from cython.cimports.c_lunch import eject_tomato as c_eject_tomato

def eject_tomato(speed: cython.float):
    c_eject_tomato(speed)
