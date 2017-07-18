#include "cpp_function_lib.h"

double add_one(double a, int b)
{
    return a + (double) b + 1.0;
}

double add_two(double a, int b)
{
    return a + (double) b + 2.0;
}


AddAnotherFunctor::AddAnotherFunctor(double to_add)
    : to_add(to_add)
{
}

double AddAnotherFunctor::operator()(double a, int b) const
{
    return a + (double) b + this->to_add;
};


FunctionKeeper::FunctionKeeper(std::function<double(double, int)> user_function)
    : my_function(user_function)
{
}

FunctionKeeper::~FunctionKeeper()
{
}

void FunctionKeeper::set_function(std::function<double(double, int)> user_function)
{
    this->my_function = user_function;
}

std::function<double(double, int)> FunctionKeeper::get_function() const
{
    return this->my_function;
}

double FunctionKeeper::call_function(double a, int b) const
{
    if (!this->my_function) {
        throw std::runtime_error("Trying to call undefined function!");
    }
    return this->my_function(a, b);
};
