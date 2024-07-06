def iterate_string():
    ustring: unicode = u'Hello world'

    # NOTE: no typing required for 'uchar' !
    for uchar in ustring:
        if uchar == u'A':
            print("Found the letter A")
