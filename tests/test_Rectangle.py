import unittest
from utilities.Rectangle import Rectangle, Point

class TestRectangle(unittest.TestCase):
    def test_init(self):
        lowerleft = Point([1, 2])
        upperright = Point([3, 4])
        r = Rectangle(lowerleft, upperright)
        self.assertEqual(r.lowerleft, lowerleft)
        self.assertEqual(r.upperright, upperright)

    def test_eq(self):
        r1 = Rectangle(Point([1, 2]), Point([3, 4]))
        r2 = Rectangle(Point([1, 2]), Point([3, 4]))
        r3 = Rectangle(Point([5, 6]), Point([7, 8]))
        self.assertEqual(r1, r2)
        self.assertNotEqual(r1, r3)

    def test_hash(self):
        r1 = Rectangle(Point([1, 2]), Point([3, 4]))
        r2 = Rectangle(Point([1, 2]), Point([3, 4]))
        self.assertEqual(hash(r1), hash(r2))

    def test_str(self):
        r = Rectangle(Point([1, 2]), Point([3, 4]))
        self.assertEqual(str(r), "((1, 2), (3, 4))")

    def test_len(self):
        r = Rectangle(Point([1, 2]), Point([3, 4]))
        self.assertEqual(len(r), 2)

    def test_from_points(self):
        points = [Point([1, 2]), Point([3, 4]), Point([5, 6])]
        r = Rectangle.from_points(points)
        self.assertEqual(r.lowerleft, Point([1, 2]))
        self.assertEqual(r.upperright, Point([5, 6]))

    def test_does_intersect(self):
        r1 = Rectangle(Point([1, 2]), Point([3, 4]))
        r2 = Rectangle(Point([2, 3]), Point([4, 5]))
        r3 = Rectangle(Point([5, 6]), Point([7, 8]))
        self.assertTrue(r1.does_intersect(r2))
        self.assertFalse(r1.does_intersect(r3))

    def test_contains(self):
        r = Rectangle(Point([1, 2]), Point([3, 4]))
        p1 = Point([2, 3])
        p2 = Point([4, 5])
        r2 = Rectangle(Point([1, 2]), Point([2, 3]))
        self.assertTrue(r.contains(p1))
        self.assertFalse(r.contains(p2))
        self.assertTrue(r.contains(r2))

    def test_divide(self):
        r = Rectangle(Point([1, 2]), Point([3, 4]))
        r1, r2 = r.divide(0, 2)
        self.assertEqual(r1.lowerleft, Point([1, 2]))
        self.assertEqual(r1.upperright, Point([2, 4]))
        self.assertEqual(r2.lowerleft, Point([2, 2]))
        self.assertEqual(r2.upperright, Point([3, 4]))

    def test_intersection(self):
        r1 = Rectangle(Point([1, 2]), Point([3, 4]))
        r2 = Rectangle(Point([2, 3]), Point([4, 5]))
        r3 = Rectangle(Point([5, 6]), Point([7, 8]))
        r4 = Rectangle(Point([2, 3]), Point([3, 4]))
        self.assertEqual(r1.intersection(r2), r4)
        self.assertIsNone(r1.intersection(r3))

    def test_vertices2D(self):
        r = Rectangle(Point([1, 2]), Point([3, 4]))
        vertices = r.vertices2D
        self.assertEqual(vertices, [Point([1, 2]), Point([1, 4]), Point([3, 4]), Point([3, 2])])

    def test_opposite(self):
        r = Rectangle(Point([1, 2]), Point([3, 4]))
        opposite1 = r.opposite(Point([2, 3]), True)
        opposite2 = r.opposite(Point([2, 3]), False)
        self.assertEqual(opposite1, ((1, 3), (3,3)))
        self.assertEqual(opposite2, ((2,2), (2,4)))
