import numpy as np

def main():
    array = np.arange(20, dtype=np.intc).reshape((2, 10))

    c_contig: cython.int[:, ::1] = array
    f_contig: cython.int[::1, :] = c_contig.T
