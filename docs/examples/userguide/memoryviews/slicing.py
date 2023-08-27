import numpy as np

def main():
    exporting_object = np.arange(0, 15 * 10 * 20, dtype=np.intc).reshape((15, 10, 20))

    my_view: cython.int[:, :, :] = exporting_object

    # These are all equivalent
    my_view[10]
    my_view[10, :, :]
    my_view[10, ...]
