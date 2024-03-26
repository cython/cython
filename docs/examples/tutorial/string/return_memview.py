def process_byte_data(data: cython.uchar[:]):
    # ... process the data, here, dummy processing.
    return_all: cython.bint = (data[0] == 108)

    if return_all:
        return bytes(data)
    else:
        # example for returning a slice
        return bytes(data[5:7])
