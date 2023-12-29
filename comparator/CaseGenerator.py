from utilities.Point import Point
from utilities.Rectangle import Rectangle

import random


class CaseGenerator:
    def check_quantity(self, quantity, name="quantity"):
        if quantity < 0:
            raise Exception(f"{name} must be positive")
    def check_rectangle(self, rectangle, must2d=False):
        if not isinstance(rectangle, Rectangle):
            raise Exception("Rectangle must be instance of Rectangle")
        if must2d and len(rectangle) != 2:
            raise Exception("Rectangle must be 2-dimensional")

    def uniform_distribution(self, quantity, rectangle, raw=True):
        self.check_quantity(quantity)
        self.check_rectangle(rectangle)
        if raw:
            return   [[random.uniform(rectangle.lowerleft[i], rectangle.upperright[i]) for i in range(len(rectangle))]  for _ in range(quantity)]
        return [Point([random.uniform(rectangle.lowerleft[i], rectangle.upperright[i]) for i in range(len(rectangle))]) for _ in range(quantity)]
        
    def normal_distribution(self, quantity, rectangle, raw=True, mu=None, sigma=None):
        """
        if mu and sigma are None, then mu is set to the middle of rectangle and sigma is set to 1/6 of rectangle
        """
        def check_param(param, name):
            if param is None:
                return True
            if not isinstance(param, list):
                raise Exception(f"{name} must be list")
            if len(param) != len(rectangle):
                raise Exception(f"{name} must have the same dimensionality as rectangle")
        self.check_quantity(quantity)
        self.check_rectangle(rectangle)
        if check_param(mu, "mu"):
            mu = [rectangle.lowerleft[i] + (rectangle.upperright[i] - rectangle.lowerleft[i])/2 for i in range(len(rectangle))]
        if check_param(sigma, "sigma"):
            sigma = [(rectangle.upperright[i] - rectangle.lowerleft[i])/6 for i in range(len(rectangle))]
        if raw:
            return   [[random.gauss(mu[i], sigma[i]) for i in range(len(rectangle))]  for _ in range(quantity)]
        return [Point([random.gauss(mu[i], sigma[i]) for i in range(len(rectangle))]) for _ in range(quantity)]

    def grid_distribution(self, columns, rows, rectangle, raw=True):
        self.check_quantity(columns, "columns")
        self.check_quantity(rows, "rows")
        self.check_rectangle(rectangle, must2d=True)
        vstep = (rectangle.upperright[1] - rectangle.lowerleft[1]) / (rows+1)
        hstep = (rectangle.upperright[0] - rectangle.lowerleft[0]) / (columns+1)
        if raw:
            return [(rectangle.lowerleft[0] + hstep*(i+1), rectangle.lowerleft[1] + vstep*(j+1)) for i in range(columns) for j in range(rows)]
        return [Point((rectangle.lowerleft[0] + hstep*(i+1), rectangle.lowerleft[1] + vstep*(j+1))) for i in range(columns) for j in range(rows)]

    def cluster_distribution(self, quantity, clusters, raw=True):
        """
        quanity - number of points in each cluster
        """
        self.check_quantity(quantity)
        for cluster in clusters:
            self.check_rectangle(cluster, must2d=True)
        if raw:
            return    [point for cluster in clusters for point in self.uniform_distribution(quantity, cluster, raw)]
        return [Point(point) for cluster in clusters for point in self.uniform_distribution(quantity, cluster, raw)]

    def outliers_distribution(self, quantity, outliers, rectangle, raw=True):
        self.check_quantity(quantity)
        self.check_quantity(outliers, "outliers")
        self.check_rectangle(rectangle)
        hstep = (rectangle.upperright[0] - rectangle.lowerleft[0]) / 4
        vstep = (rectangle.upperright[1] - rectangle.lowerleft[1]) / 4
        small_rect = Rectangle((rectangle.lowerleft[0] + hstep, rectangle.lowerleft[1] + vstep), (rectangle.upperright[0] - hstep, rectangle.upperright[1] - vstep))
        return self.uniform_distribution(quantity, small_rect, raw) + self.uniform_distribution(outliers, rectangle, raw)

    def cross_distribution(self, vertical, horizontal, rectangle, raw=True):
        self.check_quantity(vertical, "vertical")
        self.check_quantity(horizontal, "horizontal")
        self.check_rectangle(rectangle)
        if raw:
            return   [(random.uniform(rectangle.lowerleft[0], rectangle.upperright[0]), rectangle.lowerleft[1] + (rectangle.upperright[1] - rectangle.lowerleft[1])/2)  for i in range(vertical)] +       [(rectangle.lowerleft[0] + (rectangle.upperright[0] - rectangle.lowerleft[0])/2, random.uniform(rectangle.lowerleft[1], rectangle.upperright[1]))  for i in range(horizontal)]
        return [Point((random.uniform(rectangle.lowerleft[0], rectangle.upperright[0]), rectangle.lowerleft[1] + (rectangle.upperright[1] - rectangle.lowerleft[1])/2)) for i in range(vertical)] + [Point((rectangle.lowerleft[0] + (rectangle.upperright[0] - rectangle.lowerleft[0])/2, random.uniform(rectangle.lowerleft[1], rectangle.upperright[1]))) for i in range(horizontal)]

    def rectangle_distribution(self, quantity, rectangle, raw=True):
        self.check_quantity(quantity)
        self.check_rectangle(rectangle, must2d=True)
        points = []
        sum_edges = 2*(rectangle.upperright[0] - rectangle.lowerleft[0] + rectangle.upperright[1] - rectangle.lowerleft[1])
        for i in range(quantity):
            q = random.uniform(0, sum_edges)
            if q <= rectangle.upperright[0] - rectangle.lowerleft[0]:
                points.append((rectangle.lowerleft[0] + q, rectangle.lowerleft[1]))
            elif q <= 2*(rectangle.upperright[0] - rectangle.lowerleft[0]):
                points.append((rectangle.upperright[0], rectangle.lowerleft[1] + q - (rectangle.upperright[0] - rectangle.lowerleft[0])))
            elif q <= 2*(rectangle.upperright[0] - rectangle.lowerleft[0]) + (rectangle.upperright[1] - rectangle.lowerleft[1]):
                points.append((rectangle.upperright[0] - q + 2*(rectangle.upperright[0] - rectangle.lowerleft[0]), rectangle.upperright[1]))
            else:
                points.append((rectangle.lowerleft[0], rectangle.upperright[1] - q + 2*(rectangle.upperright[0] - rectangle.lowerleft[0]) + (rectangle.upperright[1] - rectangle.lowerleft[1])))
        if raw:
            return points
        return [Point(point) for point in points]
