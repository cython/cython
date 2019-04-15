# mode: compile
# tag: posonly

# TODO: remove posonly tag before merge (and maybe remove this test,
#       since it seems covered by the runs/ test)

def test(x, y, z=42, /, w=43):
    pass

def test2(x, y, /):
    pass

def test3(x, /, z):
    pass

def test4(x, /, z, *, w):
    pass
