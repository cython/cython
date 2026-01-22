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
