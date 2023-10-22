cdef class Spam:
    pub object eggs

    def __getattr__(self, name):
        print "Spam getattr:", name
