from tests.TestManager import TestManager
from visualizer.main import Visualizer
from KdTree import KdTree
#from QuadTree import QuadTree
from utilities.Point import Point
from utilities.Rectangle import Rectangle

if __name__ == '__main__':
    # TODO: Add command line arguments
    TestManager(KdTree).all_tests()
    pass