from math import sqrt

class Point:
    def __init__(self, point):
        self._point = tuple(point)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self._point == other._point
    
    def __str__(self):
        return str(self._point)
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self._point)
    
    def __getitem__(self, index):
        return self._point[index]
    
    @property
    def point(self):
        return self._point.copy()
    
    @property
    def x(self):
        return self._point[0]
    
    @property
    def y(self):
        assert len(self._point) >= 2
        return self._point[1]
    
    def follows(self, other):
        if not isinstance(other, Point):
            raise ValueError("Can only compare Points")
        if len(self) != len(other):
            raise ValueError("Can only compare Points of the same dimensionality")
        return all(x >= y for x, y in zip(self._point, other._point))
    
    def precedes(self, other):
        if not isinstance(other, Point):
            raise ValueError("Can only compare Points")
        if len(self) != len(other):
            raise ValueError("Can only compare Points of the same dimensionality")
        return all(x <= y for x, y in zip(self._point, other._point))
    
    def distance(self, other):
        if not isinstance(other, Point):
            raise ValueError("Can only compare Points")
        if len(self) != len(other):
            raise ValueError("Can only compare Points of the same dimensionality")
        return sqrt(sum((x - y) ** 2 for x, y in zip(self._point, other._point)))
    
    def minimum(self, other):
        if not isinstance(other, Point):
            raise ValueError("Can only compare Points")
        if len(self) != len(other):
            raise ValueError("Can only compare Points of the same dimensionality")
        return Point([min(x, y) for x, y in zip(self._point, other._point)])
    
    def maximum(self, other):
        if not isinstance(other, Point):
            raise ValueError("Can only compare Points")
        if len(self) != len(other):
            raise ValueError("Can only compare Points of the same dimensionality")
        return Point([max(x, y) for x, y in zip(self._point, other._point)])
    