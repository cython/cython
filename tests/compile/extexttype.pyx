# mode: compile

cdef extern class external.Spam [object SpamObject]:
    pass

ctypedef extern class external.Grail [object Grail]:
    pass

cdef extern from "food.h":

    class external.Tomato [object Tomato]:
        pass

    class external.Bicycle [object Bicycle]:
        pass
