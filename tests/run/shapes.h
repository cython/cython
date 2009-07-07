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
        Rectangle(int width, int height) 
        {
            this->width = width;
            this->height = height;
        }
        float area() { return width * height; }
        int width;
        int height;
    };

    class Square : public Rectangle
    {
    public:
        Square(int side) : Rectangle(side, side) { this->side = side; }
        /* need until function overloading in Cython */
        Square(int side, int ignored) : Rectangle(side, side) { this->side = side; }
        int side;
    };

    class Circle : public Shape {
    public:
        Circle(int radius) { this->radius = radius; }
        float area() { return 3.1415926535897931f * radius; }
        int radius;
    };

}

#endif
