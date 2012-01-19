#ifndef _TEMPLATE_ARGS_H_
#define _TEMPLATE_ARGS_H_

template <typename T>
struct Bar {
    Bar & ref() { return *this; }
    T value;
};

template <typename T>
struct Foo {
    int bar_value(const Bar<int> & bar) { return bar.value; }
};

#endif
