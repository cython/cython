def process_byte_data(unsigned char[:] data, bint return_all):
    # ... process the data
    if return_all:
        return bytes(data)
    else:
        # example for returning a slice
        return bytes(data[5:35])
