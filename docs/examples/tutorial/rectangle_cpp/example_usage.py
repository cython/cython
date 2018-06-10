#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import rect
except ImportError:
    print("Module rect has not yet been built")
    print("Please run $python setup.py build_ext --inplace")
    print("Then try again")
    import sys
    sys.exit()

x0, y0, x1, y1 = 1, 2, 3, 4

rect_obj = rect.PyRectangle(x0, y0, x1, y1)
print(dir(rect_obj))

