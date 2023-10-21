# mode: compile

cdef:

    struct PrivFoo:
        i32 i

    i32 priv_i

    void priv_f():
        global priv_i
        priv_i = 42

cdef pub:
    struct PubFoo:
        i32 i

    i32 pub_v

    void pub_f():
        pass

    class PubBlarg [object PubBlargObj, type PubBlargType]:
        pass

cdef api:

    void api_f():
        pass

cdef pub api:
    void pub_api_f():
        pass

priv_f()
