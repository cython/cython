template<typename T, class Derived>
class Base {
public:
    Base(T x) : x_(x) { };

    Derived half() {
        Derived d(x_ / 2);
        return d;
    };

    virtual T calculate() = 0;
    virtual ~Base() { };

protected:
    T x_;
};


template<typename T>
class Square : public Base<T, Square<T> > {
public:
    Square(T x) : Base<T, Square<T> >(x) { };

    T calculate() { return this->x_ * this->x_; }
};


template<typename T>
class Cube : public Base<T, Cube<T> > {
public:
    Cube(T x) : Base<T, Cube<T> >(x) { };

    T calculate() { return this->x_ * this->x_ * this->x_; }
};
