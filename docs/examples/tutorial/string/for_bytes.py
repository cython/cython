def iterate_bytes():
    bytes_string: bytes = b"hello to A bytes' world"

    c: cython.char
    for c in bytes_string:
        if c == b'A':
            print("Found the letter A")
