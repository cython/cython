#ifndef SHAPES_H
#define SHAPES_H

namespace shapes {

    int constructor_count = 0;
    int destructor_count = 0;

    class Shape
    {
    public:
        virtual float area() const = 0;
        Shape() { constructor_count++; }
        virtual ~Shape() { destructor_count++; }
    };

    class Rectangle : public Shape
    {
    public:
    	Rectangle() { }
        Rectangle(int width, int height)
        {
            this->width = width;
            this->height = height;
        }

        float area() const { return width * height; }
        int width;
        int height;

        int method(int arg) {
            return width * height + arg;
        }

    };

    class Square : public Rectangle
    {
    public:
        Square(int side) : Rectangle(side, side) { this->side = side; }
        int side;
    };
    
    class Ellipse : public Shape {
    public:
        Ellipse(int a, int b) { this->a = a; this->b = b; }
        float area() const { return 3.1415926535897931f * a * b; }
        int a, b;
    };
    
    class Circle : public Ellipse {
    public:
        Circle(int radius) : Ellipse(radius, radius) { this->radius = radius; }
        int radius;
    };

    class Empty : public Shape {
    public:
        float area() const { return 0; }
    };

}

#endif
