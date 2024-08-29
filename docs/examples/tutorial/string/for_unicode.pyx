def iterate_string():
    cdef unicode ustring = u'Hello world'

    # NOTE: no typing required for 'uchar' !
    for uchar in ustring:
        if uchar == u'A':
            print("Found the letter A")
