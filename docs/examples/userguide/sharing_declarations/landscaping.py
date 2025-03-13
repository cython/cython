from cython.cimports.shrubbing import Shrubbery
import shrubbing

def main():
    sh: Shrubbery
    sh = shrubbing.standard_shrubbery()
    print("Shrubbery size is", sh.width, 'x', sh.length)
