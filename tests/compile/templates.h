#ifndef _TEMPLATES_H_
#define _TEMPLATES_H_

template<class T>
class TemplateTest1
{
public:
    T value;
    int t;
    TemplateTest1() { }
    T getValue() { return value; }
};

template<class T, class U>
class TemplateTest2
{
public:
    T value1;
    U value2;
    TemplateTest2() { }
    T getValue1() { return value1; }
    U getValue2() { return value2; }
};

template <typename T>
void template_function(TemplateTest1<T> &)
{
}

#endif
