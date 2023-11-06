cimport shrubbing
import shrubbing

def main():
    cdef shrubbing.Shrubbery sh
    sh = shrubbing.standard_shrubbery()
    print("Shrubbery size is", sh.width, 'x', sh.length)
