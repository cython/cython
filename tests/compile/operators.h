#ifndef _OPERATORS_H_
#define _OPERATORS_H_

class Operators
{
public:
    int value;
    Operators() { }
    Operators(int value) { this->value = value; }
    virtual ~Operators() { }
    Operators operator+(Operators f) { return Operators(this->value + f.value); }
    Operators operator-(Operators f) { return Operators(this->value - f.value); }
    Operators operator*(Operators f) { return Operators(this->value * f.value); }
    Operators operator/(Operators f) { return Operators(this->value / f.value); }
    bool operator<(Operators f) { return this->value < f.value; }
    bool operator<=(Operators f) { return this->value <= f.value; }
    bool operator==(Operators f) { return this->value == f.value; }
    bool operator!=(Operators f) { return this->value != f.value; }
    bool operator>(Operators f) { return this->value > f.value; }
    bool operator>=(Operators f) { return this->value >= f.value; }
    Operators operator>>(int v) { return Operators(this->value >> v); }
    Operators operator<<(int v) { return Operators(this->value << v); }
    Operators operator%(int v) { return Operators(this->value % v); }
};

#endif
