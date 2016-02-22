namespace outer {

    int x = 10;

    int outer_value = 10;

    namespace inner {

        int x = 100;

        int inner_value = 100;

    }

}

namespace A {

    typedef int A_t;

    struct S {
        A_t k;
        double x;
    };

    A_t A_func(A_t first, A_t second) {
        return first + second;
    }

}
