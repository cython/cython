# mode: run
# tag: cpp

from libcpp cimport bool as bool_t

cdef:
    struct S1:
        int i

    struct S2:
        int i

    extern from *:
        """
        #include <stdio.h>
        #include <map>

        unsigned int i;

        void test(std::map<unsigned int, unsigned int> m) {
            printf("Map size: %d\n", m.size());
        }

        class testclass {
        public:
            void a() {
                printf("testclass->a();\n");
            }
            void a(unsigned int i) {
                printf("testclass->a(%d);\n", i);
            }
        };
        """
        cppclass testclass:
            testclass()
            void a()
            void a(unsigned int i)

    cppclass testclass2(testclass):
        testclass2()

    cppclass testclass3(testclass):
        testclass3()
        void a(S1 v)

    cppclass testclass4(testclass):
        testclass4()
        void a(S2 v)

    testclass t1 = testclass()
    testclass2 t2 = testclass2()
    testclass3 t3 = testclass3()
    testclass4 t4 = testclass4()

cdef S1 s1
cdef S2 s2

t1.a()
t1.a(1)

t2.a()
t2.a(2)

t3.a()
t3.a(3)
t3.a(s1)

t4.a()
t4.a(4)
t4.a(s2)
