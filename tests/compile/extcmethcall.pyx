# mode: compile

cdef class Spam:
    cdef i32 tons

    fn void add_tons(self, i32 x):
        pass

cdef class SuperSpam(Spam):
    pass

fn void tomato():
    let Spam spam
    let SuperSpam superspam = SuperSpam()
    spam = superspam
    spam.add_tons(42)
    superspam.add_tons(1764)

tomato()
