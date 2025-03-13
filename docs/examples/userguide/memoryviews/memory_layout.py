from cython.cimports.cython import view

def main():
    # direct access in both dimensions, strided in the first dimension, contiguous in the last
    a: cython.int[:, ::view.contiguous]

    # contiguous list of pointers to contiguous lists of ints
    b: cython.int[::view.indirect_contiguous, ::1]

    # direct or indirect in the first dimension, direct in the second dimension
    # strided in both dimensions
    c: cython.int[::view.generic, :]
