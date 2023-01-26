#pragma once

#include <iostream>

struct A {
  struct B {
    std::string get_str() { return "B"; }
  };

  static B get() { return A::B(); }
};
