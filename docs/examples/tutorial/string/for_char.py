def iterate_char():
    c_string: cython.p_char = "Hello to A C-string's world"

    c: cython.char
    for c in c_string[:11]:
        if c == b'A':
            print("Found the letter A")
