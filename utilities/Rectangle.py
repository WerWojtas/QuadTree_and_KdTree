from utilities.Point import Point

from functools import reduce

class Rectangle:
    def __init__(self, lowerleft, upperright):
        if not isinstance(lowerleft, Point):
            lowerleft = Point(lowerleft)
        if not isinstance(upperright, Point):
            upperright = Point(upperright)
        if len(lowerleft) != len(upperright):
            raise ValueError(f"Points must have the same dimensionality [{len(lowerleft)} != {len(upperright)}]")
        if not lowerleft.precedes(upperright):
            raise ValueError("LowerLeft point must precede the UpperRight point")
        self._lowerleft = lowerleft
        self._upperright = upperright

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return False
        return self._lowerleft == other._lowerleft and self._upperright == other._upperright

    def __hash__(self):
        return hash((self._lowerleft, self._upperright))

    def __str__(self):
        return f"({self._lowerleft}, {self._upperright})"
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self._lowerleft)
    
    @property
    def lowerleft(self):
        return self._lowerleft
    
    @property
    def upperright(self):
        return self._upperright
    
    @classmethod
    def from_points(cls, points):
        """
        Create a rectangle that contains all points from a list of points
        @param points: a list of points
        @return: a rectangle
        raises ValueError if the list of points is empty or if the points are not of the same dimensionality
        """
        if not points:
            raise ValueError("Cannot create a Rectangle from an empty list of points")
        if not all(isinstance(p, Point) for p in points):
            raise ValueError("All points must be instances of Point")
        if not all(len(p) == len(points[0]) for p in points):
            raise ValueError("All points must have the same dimensionality")
        lowerleft = reduce(lambda p1, p2: p1.minimum(p2), points)
        upperright = reduce(lambda p1, p2: p1.maximum(p2), points)
        return cls(lowerleft, upperright)
    
    def does_intersect(self, other):
        """
        Check if two rectangles intersect (share at least one point)
        @param other: another rectangle
        @return: True if the rectangles intersect, False otherwise
        raises ValueError if the other object is not a rectangle or if the rectangles have different dimensionality
        """
        if not isinstance(other, Rectangle):
            raise ValueError("Can only check intersection with another Rectangle")
        if len(self) != len(other):
            raise ValueError("Can only check intersection with a Rectangle of the same dimensionality")
        return self.lowerleft.precedes(other.upperright) and self.upperright.follows(other.lowerleft)

    def contains(self, object):
        """
        Check if a point/rectangle is FULLY contained in the rectangle
        @param object: a point or a rectangle
        @return: True if the point/rectangle is fully contained in the rectangle, False otherwise
        raises ValueError if the object is not a point or a rectangle
        """
        if isinstance(object, Point):
            return self.lowerleft.precedes(object) and self.upperright.follows(object)
        elif isinstance(object, Rectangle):
            return self.lowerleft.precedes(object.lowerleft) and self.upperright.follows(object.upperright)
        else:
            raise ValueError("Can only check containment of a Point or a Rectangle")
        
    def divide(self, dimension, value):
        """
        Divide the rectangle into two rectangles along a given dimension and value
        @param dimension: the dimension along which to divide 0 = x, 1 = y, 2 = z, ...
        @param value: the value along the given dimension
        @return: a tuple of two rectangles
        raises ValueError if the dimension is not between 0 and the dimensionality of the rectangle - 1 or if the value is not between the lowerleft and upperright values along the given dimension
        """
        if dimension < 0 or dimension >= len(self):
            raise ValueError(f"Dimension must be between 0 and {len(self)-1}")
        if value < self.lowerleft[dimension] or value > self.upperright[dimension]:
            raise ValueError(f"Value must be between {self.lowerleft[dimension]} and {self.upperright[dimension]}")
        ll1, ur1 = self.lowerleft.point, self.upperright.point
        ll2, ur2 = self.lowerleft.point, self.upperright.point
        ll2[dimension] = ur1[dimension] = value
        return Rectangle(ll1, ur1), Rectangle(ll2, ur2)

    def intersection(self, other):
        """
        Compute the intersection of two rectangles
        @param other: another rectangle
        @return: rectangle representing the intersection of the two rectangles or None if the rectangles do not intersect
        raises ValueError if the other object is not a rectangle or if the rectangles have different dimensionality
        """
        if not isinstance(other, Rectangle):
            raise ValueError("Can only compute intersection with another Rectangle")
        if len(self) != len(other):
            raise ValueError("Can only compute intersection with a Rectangle of the same dimensionality")
        if not self.does_intersect(other):
            return None
        ll = self.lowerleft.maximum(other.lowerleft)
        ur = self.upperright.minimum(other.upperright)
        return Rectangle(ll, ur)
    