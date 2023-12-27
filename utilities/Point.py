from math import sqrt

class Point:
    def __init__(self, point):
        self._point = tuple(point)

    def __eq__(self, other):
        return self._point == other._point
    
    def __str__(self):
        return str(self._point)
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self._point)
    
    def getpoint(self):
        return self._point.copy()
    
    def x(self):
        return self._point[0]
    
    def y(self):
        assert len(self._point) >= 2
        return self._point[1]
    
    def follows(self, other):
        return all(x >= y for x, y in zip(self._point, other._point))
    
    def precedes(self, other):
        return all(x <= y for x, y in zip(self._point, other._point))
    
    def distance(self, other):
        return sqrt(sum((x - y) ** 2 for x, y in zip(self._point, other._point)))
    
    def minimum(self, other):
        return Point([min(x, y) for x, y in zip(self._point, other._point)])
    
    def maximum(self, other):
        return Point([max(x, y) for x, y in zip(self._point, other._point)])
    