#ifndef SHAPES_H
#define SHAPES_H

namespace shapes {

    class Shape
    {
    public:
        virtual float area() = 0;
        virtual ~Shape() { }
    };
    
    class Rectangle : public Shape
    {
    public:
        Rectangle(int width, int height);
        float area() { return width * height; }
        int width;
        int height;
    };
    
    class Square : public Shape
    {
    public:
        Square(int side);
        float area() { return side * side; }
        int side;
    };

}
#endif
