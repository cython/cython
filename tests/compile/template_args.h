#ifndef _TEMPLATE_ARGS_H_
#define _TEMPLATE_ARGS_H_

template <typename T>
struct Bar {
};

template <typename T>
struct Foo {
    void set_bar(const Bar[size_t] & bar) {}
};

#endif
