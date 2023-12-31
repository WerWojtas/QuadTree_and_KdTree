import unittest
from utilities.Rectangle import Rectangle
from utilities.Point import Point
from tests.test_CaseGenerator import TestCaseGenerator
from tests.test_KdTree import TestKdTree
from tests.test_Rectangle import TestRectangle
from tests.test_Point import TestPoint
from KdTree import KdTree

class TestManager:
    def __init__(self, tree):
        self._tests = [self.contain_point_int,
                       self.contain_point_float,
                       self.points_in_rectangle_int,
                       self.points_in_rectangle_float]
        self.mytree = tree

    def all_tests(self):
        print("Running all tests:")
        good = all = 0
        for test in self._tests:
            g, a = test()
            good += g
            all += a
        print(f"Passed {good}/{all} of all self tests.")
        print("Running all unittests:")
        return unittest.main()
    
    def contain_point_int(self):
        print("Test contain_point_int:")
        points = [((1,2), (3,4), (5,6), (7,8), (9,10)),
                  ((-1,-2), (-3,-4), (-5,-6), (-7,-8), (-9,-10)),
                  ((3,4), (3,8), (8,4), (8,8)),
                  ((10, 85), (18, 89), (29, 33), (32, 76), (34, 21), (39, 69), (43, 94), (44, 74), (60, 48), (61, 49), (61, 90), (66, 6), (69, 60), (71, 72), (84, 49))]
        checks = [{(1,2):True, (3,4):True, (5,6):True, (7,8):True, (9,10):True, (0,0):False, (2,2):False, (4,4):False, (6,6):False, (8,9):False, (10,10):False},
                  {(-1,-2):True, (-3,-4):True, (-5,-6):True, (-7,-8):True, (-9,-10):True, (0,0):False, (-2,-2):False, (-4,-4):False, (-6,-6):False, (-8,-9):False, (-10,-10):False},
                  {(3,4):True, (3,8):True, (8,4):True, (8,8):True, (0,0):False, (4,4):False, (4,8):False, (8,9):False, (9,9):False, (10,10):False},
                  {(10, 85):True, (18, 89):True, (29, 33):True, (32, 76):True, (34, 21):True, (39, 69):True, (43, 94):True, (44, 74):True, (60, 48):True, (61, 49):True, (61, 90):True, (66, 6):True, (69, 60):True, (71, 72):True, (84, 49):True, (0,0):False, (10,10):False, (20,20):False, (30,30):False, (40,40):False, (50,50):False, (60,60):False, (70,70):False, (80,80):False, (90,90):False}]
        good = all = 0
        for i in range(len(points)):
            tree = self.mytree(points[i])
            for point, expected in checks[i].items():
                actual = tree.if_contains(point)
                if actual != expected:
                    print("0", end="")
                    print(f"Expected {expected} for {point} in {points[i]}")
                else:
                    print("+", end="")
                    good += 1
                all += 1
        print(f"\nPassed {good}/{all} tests.")
        return good, all
        
    def contain_point_float(self):
        print("Test contain_point_float:")
        points = [((10.23823, 97.54655), (21.69386, 61.08857), (26.5443, 51.29767),
                  (30.22109, 19.83629), (35.83114, 79.59375), (41.02798, 69.55036),
                  (43.06388, 62.39269), (44.71609, 22.87838), (50.30803, 77.5922),
                  (60.28991, 69.49429), (69.76965, 34.37997), (72.70958, 94.48302),
                  (86.78683, 74.22789), (88.1796, 52.55651),  (93.06464, 56.67088))]
        checks = [{(16.185, 80.25312):False, (29.37526, 54.58067):False, (85.70135, 83.52599):False, (72.70958, 94.48302):True, (88.1796, 52.55651):True, 
                   (19.91432, 49.7068):False, (84.99745, 36.34022):False, (21.69386, 61.08857):True, (86.78683, 74.22789):True, (10.23823, 97.54655):True}]
        good = all = 0
        for i in range(len(points)):
            tree = self.mytree(points[i])
            for point, expected in checks[i].items():
                actual = tree.if_contains(point)
                if actual != expected:
                    print("0", end="")
                else:
                    print("+", end="")
                    good += 1
                all += 1
        print(f"\nPassed {good}/{all} tests.")
        return good, all
    
    def points_in_rectangle_int(self):
        print("Test points_in_rectangle_int:")
        points = [((1,2), (3,4), (5,6), (7,8), (9,10)),
                  ((-1,-2), (-3,-4), (-5,-6), (-7,-8), (-9,-10)),
                  ((14, 93), (17, 73), (19, 33), (27, 68), (29, 72), (33, 30), (50, 57), (59, 17), (62, 63), (66, 41), (85, 56), (86, 58), (91, 11), (92, 98), (98, 47))]
        checks = [{Rectangle((1,1), (2,2)):[(1,2)], Rectangle((-4,-5), (0,0)):[]},
                  {Rectangle((-10,-10), (-1,-1)):[(-1,-2), (-3,-4), (-5,-6), (-7,-8), (-9,-10)]},
                  {Rectangle((30,10), (95, 70)): [(33, 30), (50, 57), (59, 17), (62, 63), (66, 41), (85, 56), (86, 58), (91, 11)]}]
        good = all = 0
        for i in range(len(points)):
            tree = self.mytree(points[i])
            for rect, expected in checks[i].items():
                actual = tree.search_in_rectangle(rect, raw=True)
                if not self.same(actual, expected):
                    print("0", end="")
                else:
                    print("+", end="")
                    good += 1
                all += 1
        print(f"\nPassed {good}/{all} tests.")
        return good, all
    
    def points_in_rectangle_float(self):
        print("Test points_in_rectangle_float:")
        points = [((13.0088, 73.47405),  (19.37122, 92.27245), (26.81686, 60.45529),
                  (30.86009, 77.78741), (31.64859, 88.05649), (47.89563, 63.91615),
                  (54.94825, 57.69471), (58.60036, 39.4115),  (66.36514, 72.69857),
                  (69.98282, 24.71197), (71.91889, 40.94198), (81.91302, 87.35569),
                  (89.44507, 18.6295),  (97.43819, 18.13145), (98.47172, 44.33949))]
        checks = [{Rectangle((22.123, 15.423), (87.639, 82.873)):[(26.81686, 60.45529), (30.86009, 77.78741),
                                                                  (47.89563, 63.91615), (54.94825, 57.69471),
                                                                  (58.60036, 39.4115),  (66.36514, 72.69857),
                                                                  (69.98282, 24.71197), (71.91889, 40.94198)]}]
        good = all = 0
        for i in range(len(points)):
            tree = self.mytree(points[i])
            for rect, expected in checks[i].items():
                actual = tree.search_in_rectangle(rect, raw=True)
                if not self.same(actual, expected):
                    print("0", end="")
                else:
                    print("+", end="")
                    good += 1
                all += 1
        print(f"\nPassed {good}/{all} tests.")
        return good, all

    def same(self, act, exp):
        act = [tuple(i) for i in act]
        exp = [tuple(i) for i in exp]
        if len(act) != len(exp):
            return False
        for i in act:
            if i not in exp:
                return False
        for i in exp:
            if i not in act:
                return False
        return True

tm = TestManager(KdTree)
tm.all_tests()