#include <ios>
#include <new>
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

void raise_ios_failure() {
    throw std::ios_base::failure("iostream failure");
}

void raise_memory() {
    // std::bad_alloc can only be default constructed,
    // so we have no control over the error message
    throw std::bad_alloc();
}

void raise_overflow() {
    throw std::overflow_error("overflow_error");
}

void raise_range_error() {
    throw std::range_error("range_error");
}

void raise_underflow() {
    throw std::underflow_error("underflow_error");
}
