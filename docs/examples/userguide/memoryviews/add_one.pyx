import numpy as np

def add_one(int[:,:] buf):
    for x in range(buf.shape[0]):
        for y in range(buf.shape[1]):
            buf[x, y] += 1

# exporting_object must be a Python object
# implementing the buffer interface, e.g. a numpy array.
exporting_object = np.zeros((10, 20), dtype=np.intc)

add_one(exporting_object)
