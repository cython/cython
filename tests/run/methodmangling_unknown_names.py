# mode: run
# tag: allow_unknown_names, pure2.0, pure3.0

class Test(object):
    def run(self):
        """
        >>> Test().run()
        NameError1
        NameError2
        found mangled
        """
        try:
            print(__something)
        except NameError:
            print("NameError1")  # correct - shouldn't exist
        globals()['__something'] = 'found unmangled'
        try:
            print(__something)
        except NameError:
            print("NameError2")  # correct - shouldn't exist
        globals()['_Test__something'] = 'found mangled'
        try:
            print(__something)  # should print this
        except NameError:
            print("NameError3")
