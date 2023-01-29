#ifndef CPP_NESTED_NAMES_HELPER_H
#define CPP_NESTED_NAMES_HELPER_H

#include <string>

struct OuterClass {
  struct NestedClass {
    std::string get_str() { return "NestedClass"; }
  };

  static NestedClass get() { return OuterClass::NestedClass(); }
};

#endif
