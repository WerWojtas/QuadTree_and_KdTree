import unittest
from utilities.Point import Point

class TestPoint(unittest.TestCase):
    def test_init(self):
        p = Point([1, 2, 3])
        self.assertEqual(p.point, [1, 2, 3])

    def test_eq(self):
        p1 = Point([1, 2, 3])
        p2 = Point([1, 2, 3])
        p3 = Point([4, 5, 6])
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)

    def test_hash(self):
        p1 = Point([1, 2, 3])
        p2 = Point([1, 2, 3])
        self.assertEqual(hash(p1), hash(p2))

    def test_str(self):
        p = Point([1, 2, 3])
        self.assertEqual(str(p), "(1, 2, 3)")

    def test_len(self):
        p = Point([1, 2, 3])
        self.assertEqual(len(p), 3)

    def test_getitem(self):
        p = Point([1, 2, 3])
        self.assertEqual(p[0], 1)
        self.assertEqual(p[1], 2)
        self.assertEqual(p[2], 3)

    def test_x(self):
        p = Point([1, 2, 3])
        self.assertEqual(p.x, 1)

    def test_y(self):
        p = Point([1, 2, 3])
        self.assertEqual(p.y, 2)

    def test_follows(self):
        p1 = Point([1, 2, 3])
        p2 = Point([0, 1, 2])
        p3 = Point([2, 3, 4])
        self.assertTrue(p1.follows(p2))
        self.assertFalse(p1.follows(p3))

    def test_precedes(self):
        p1 = Point([1, 2, 3])
        p2 = Point([0, 1, 2])
        p3 = Point([2, 3, 4])
        self.assertFalse(p1.precedes(p2))
        self.assertTrue(p1.precedes(p3))

    def test_distance(self):
        p1 = Point([1, 2, 3])
        p2 = Point([4, 5, 6])
        self.assertAlmostEqual(p1.distance(p2), 5.196152, places=6)

    def test_minimum(self):
        p1 = Point([4, 2, 3])
        p2 = Point([1, 5, 6])
        p3 = Point([1, 2, 3])
        self.assertEqual(p1.minimum(p2), p3)

    def test_maximum(self):
        p1 = Point([1, 2, 3])
        p2 = Point([4, 5, 6])
        p3 = Point([4, 5, 6])
        self.assertEqual(p1.maximum(p2), p3)
