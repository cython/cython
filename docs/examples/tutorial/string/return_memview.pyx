def process_byte_data(u8[:] data):
    # ... process the data, here, dummy processing.
    let bint return_all = (data[0] == 108)

    if return_all:
        return bytes(data)
    else:
        # example for returning a slice
        return bytes(data[5:7])
