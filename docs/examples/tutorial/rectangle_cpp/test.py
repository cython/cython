#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import unittest
import os


class TestRectangleCppExtension(unittest.TestCase):
    def setUp(self):
        self.directory_at_runtime = os.listdir()
        os.system("python setup.py build_ext --inplace")
        import rect
        self.x0, self.y0, self.x1, self.y1 = 1, 2, 3, 4
        self.rect_obj = rect.PyRectangle(self.x0, self.y0, self.x1, self.y1)

    def test_get_area(self):
        width = self.x1 - self.x0
        height = self.y1 - self.y0
        area = width * height
        self.assertEqual(
                self.rect_obj.get_area(),
                area)

    def test_get_size(self):
        true_width = self.x1 - self.x0
        true_height = self.y1 - self.y0
        width, height = self.rect_obj.get_size()
        self.assertEqual(true_width, width)
        self.assertEqual(true_height, height)

    def test_move(self):
        x0, x1 = self.rect_obj.x0, self.rect_obj.x1
        y0, y1 = self.rect_obj.y0, self.rect_obj.y1
        dx, dy = 10, 5
        self.rect_obj.move(dx, dy)
        self.assertEqual(
                (x0+dx, x1+dx, y0+dy, y1+dy),
                (self.rect_obj.x0, self.rect_obj.x1,
                    self.rect_obj.y0, self.rect_obj.y1))

    def tearDown(self):
        files_to_remove = [f for f in os.listdir()
                                if f not in self.directory_at_runtime]
        for f in files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
            elif os.path.isdir(f):
                os.system("rm -rf {}".format(f))


if __name__ == "__main__":
    unittest.main()

