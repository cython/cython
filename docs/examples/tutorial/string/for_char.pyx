def iterate_char():
    cdef char* c_string = "Hello to A C-string's world"

    cdef char c
    for c in c_string[:11]:
        if c == b'A':
            print("Found the letter A")
