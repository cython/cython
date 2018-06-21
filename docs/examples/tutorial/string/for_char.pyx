cdef char* c_string = "Hello world"

cdef char c
for c in c_string[:11]:
    if c == 'A':
        print("Found the letter A")
