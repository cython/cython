def process_byte_data(unsigned char[:] data):
    length = data.shape[0]
    first_byte = data[0]
    slice_view = data[1:-1]
    # ...
