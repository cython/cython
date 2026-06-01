import numpy as np

def main():

    to_view: cython.int[:, :, :] = np.empty((20, 15, 30), dtype=np.intc)
    from_view: cython.int[:, :, :] = np.ones((20, 15, 30), dtype=np.intc)

    # copy the elements in from_view to to_view
    to_view[...] = from_view
    # or
    to_view[:] = from_view
    # or
    to_view[:, :, :] = from_view
