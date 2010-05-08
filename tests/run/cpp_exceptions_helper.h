#include <stdexcept>

int raise_int(int fire) {
    if (fire) {
        throw 1;
    }
    return 0;
}

int raise_index(int fire) {
    if (fire) {
        throw std::out_of_range("c++ error");
    }
    return 0;
}

class Foo {
 public:
  int bar(int fire) {
    if (fire) {
      throw 1;
    }
    return 0;
  }
};
