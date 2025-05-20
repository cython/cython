def process_byte_data(data: cython.uchar[:]):
    length = data.shape[0]
    first_byte = data[0]
    slice_view = data[1:-1]
    # ...
