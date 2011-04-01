# mode: compile

cdef:

    struct PrivFoo:
        int i

    int priv_i

    void priv_f():
        global priv_i
        priv_i = 42

cdef public:

    struct PubFoo:
        int i

    int pub_v

    void pub_f():
        pass

    class PubBlarg [object PubBlargObj, type PubBlargType]:
        pass

cdef api:

    void api_f():
        pass

cdef public api:

    void pub_api_f():
        pass

priv_f()
