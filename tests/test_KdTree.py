import unittest
from utilities.Rectangle import Rectangle, Point
from KdTree import KdTreeNode

class TestKdTree(unittest.TestCase):
    def setUp(self):
        self.points = [Point([1, 2]), Point([3, 4]), Point([5, 6]), Point([7, 8])]
        self.rectangle = Rectangle(Point([0, 0]), Point([10, 10]))

    def test_init(self):
        node = KdTreeNode(self.points, self.rectangle, points_in_node=True)
        self.assertEqual(node._points, self.points)
        self.assertEqual(node._rectangle, self.rectangle)
        self.assertIsNotNone(node._axis)
        self.assertEqual(node._depth, 0)
        self.assertIsNotNone(node._left)
        self.assertIsNotNone(node._right)

    def test_contains(self):
        node = KdTreeNode(self.points, self.rectangle, points_in_node=True)
        self.assertTrue(node._if_contains(Point([1, 2])))
        self.assertFalse(node._if_contains(Point([0, 0])))
        self.assertFalse(node._if_contains(Point([10, 10])))

    def test_search_rectangle(self):
        node = KdTreeNode(self.points, self.rectangle, points_in_node=True)
        search_area = Rectangle(Point([2, 3]), Point([6, 7]))
        result = node._search_rectangle(search_area)
        expected_result = [Point([3, 4]), Point([5, 6])]
        self.assertEqual(result, expected_result)
