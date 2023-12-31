import unittest
from utilities.Rectangle import Rectangle, Point
from comparator.CaseGenerator import CaseGenerator

class TestCaseGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = CaseGenerator()

    def test_check_quantity_positive(self):
        self.assertIsNone(self.generator.check_quantity(10))

    def test_check_quantity_negative(self):
        with self.assertRaises(Exception):
            self.generator.check_quantity(-5)

    def test_check_rectangle_instance(self):
        rectangle = Rectangle(Point([1, 2]), Point([3, 4]))
        self.assertIsNone(self.generator.check_rectangle(rectangle))

    def test_check_rectangle_not_instance(self):
        with self.assertRaises(Exception):
            self.generator.check_rectangle("rectangle")

    def test_check_rectangle_2d(self):
        rectangle = Rectangle(Point([1, 2]), Point([3, 4]))
        self.assertIsNone(self.generator.check_rectangle(rectangle, must2d=True))

    def test_check_rectangle_not_2d(self):
        rectangle = Rectangle(Point([1, 2, 3]), Point([4, 5, 6]))
        with self.assertRaises(Exception):
            self.generator.check_rectangle(rectangle, must2d=True)

    def test_uniform_distribution_raw(self):
        rectangle = Rectangle(Point([1, 2]), Point([3, 4]))
        points = self.generator.uniform_distribution(5, rectangle, raw=True)
        self.assertEqual(len(points), 5)
        for point in points:
            self.assertTrue(rectangle.lowerleft[0] <= point[0] <= rectangle.upperright[0])
            self.assertTrue(rectangle.lowerleft[1] <= point[1] <= rectangle.upperright[1])

    def test_uniform_distribution_not_raw(self):
        rectangle = Rectangle(Point([1, 2]), Point([3, 4]))
        points = self.generator.uniform_distribution(5, rectangle, raw=False)
        self.assertEqual(len(points), 5)
        for point in points:
            self.assertTrue(rectangle.lowerleft[0] <= point.point[0] <= rectangle.upperright[0])
            self.assertTrue(rectangle.lowerleft[1] <= point.point[1] <= rectangle.upperright[1])

    def test_uniform_distribution_2d(self):
        rectangle = Rectangle(Point([1, 2]), Point([3, 4]))
        points = self.generator.uniform_distribution(5, rectangle, raw=False)
        self.assertEqual(len(points), 5)
        for point in points:
            self.assertEqual(len(point.point), 2)

    def test_uniform_distribution_3d(self):
        rectangle = Rectangle(Point([1, 2, 3]), Point([4, 5, 6]))
        points = self.generator.uniform_distribution(5, rectangle, raw=False)
        self.assertEqual(len(points), 5)
        for point in points:
            self.assertEqual(len(point.point), 3)

    def test_normal_distribution_raw(self):
        rectangle = Rectangle(Point([1, 2]), Point([3, 4]))
        points = self.generator.normal_distribution(5, rectangle, raw=True)
        self.assertEqual(len(points), 5)
        for point in points:
            self.assertTrue(rectangle.lowerleft[0] <= point[0] <= rectangle.upperright[0])
            self.assertTrue(rectangle.lowerleft[1] <= point[1] <= rectangle.upperright[1])

    def test_normal_distribution_not_raw(self):
        rectangle = Rectangle(Point([1, 2]), Point([3, 4]))
        points = self.generator.normal_distribution(5, rectangle, raw=False)
        self.assertEqual(len(points), 5)
        for point in points:
            self.assertTrue(rectangle.lowerleft[0] <= point.point[0] <= rectangle.upperright[0])
            self.assertTrue(rectangle.lowerleft[1] <= point.point[1] <= rectangle.upperright[1])

    def test_normal_distribution_2d(self):
        rectangle = Rectangle(Point([1, 2]), Point([3, 4]))
        points = self.generator.normal_distribution(5, rectangle, raw=False)
        self.assertEqual(len(points), 5)
        for point in points:
            self.assertEqual(len(point), 2)

    def test_normal_distribution_3d(self):
        rectangle = Rectangle(Point([1, 2, 3]), Point([4, 5, 6]))
        points = self.generator.normal_distribution(5, rectangle, raw=False)
        self.assertEqual(len(points), 5)
        for point in points:
            self.assertEqual(len(point), 3)
            