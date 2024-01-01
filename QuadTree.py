from utilities.Point import Point
from utilities.Rectangle import Rectangle

class QuadTree:
    def __init__(self, points, max_capacity=1, points_in_node=False):
        if len(points) == 0:
            raise ValueError("The list of points is empty.")
        if not all(len(point) == 2 for point in points):
            raise ValueError("The points have different dimensions than 2.")
        points = [Point(point) for point in points]
        self._root = QuadTreeNode(points, Rectangle.from_points(points), max_capacity, points_in_node)
        self._max_capacity = max_capacity
        self._points_in_node = points_in_node

    def if_contains(self,point):
        if len(point) != 2:
            raise ValueError("The point has different dimension than 2.")
        if not isinstance(point, Point):
            point = Point(point)
        if self._root._rectangle.contains(point):
            return self._root._if_contains(point)
        return False

    def search_in_rectangle(self, rectangle, raw = False):
        if not isinstance(rectangle, Rectangle):
            raise ValueError("The rectangle is not a Rectangle object.")
        if len(rectangle) != 2:
            raise ValueError("The rectangle has different dimension than 2.")
        area = rectangle.intersection(self._root._rectangle)
        if area is None:
            return []
        result = list(set(self._root._search_in_rectangle(area, self._points_in_node)))
        if raw:
            return [point.point for point in result]
        return result
        
        

class QuadTreeNode:
    def __init__(self, points, rectangle, max_capacity=1, points_in_node=False):
        if points_in_node:
            self.points = points.copy()    # points in the node
        elif len(points) <= max_capacity:
            self.points = points           # points in the leaf
        self._left_up = None               # left up subtree
        self._right_up = None              # right up subtree
        self._left_down = None             # left down subtree
        self._right_down = None            # right down subtree
        self._rectangle = rectangle        # rectangle that contains all points in the node
        self._build(points, max_capacity, points_in_node)

    def _build(self, points, max_capacity, points_in_node):
        if len(points) > max_capacity:
            rec_left_down, rec_right_down, rec_right_up, rec_left_up = self._rectangle.to_quaters()
            points_left_up = []
            points_right_up = []
            points_left_down = []
            points_right_down = []
            center = self._rectangle.center()
            for point in points:
                if point.x <= center.x:
                    if point.y <= center.y:
                        points_left_down.append(point)
                    if point.y >= center.y:
                        points_left_up.append(point)
                if point.x >= center.x:
                    if point.y <= center.y:
                        points_right_down.append(point)
                    if point.y >= center.y:
                        points_right_up.append(point)
            self._left_up = QuadTreeNode(points_left_up, rec_left_up, max_capacity, points_in_node)
            self._right_up = QuadTreeNode(points_right_up, rec_right_up, max_capacity, points_in_node)
            self._left_down = QuadTreeNode(points_left_down, rec_left_down, max_capacity, points_in_node)
            self._right_down = QuadTreeNode(points_right_down, rec_right_down, max_capacity, points_in_node)

    def _if_contains(self, point):
        if self._left_up is None:
            return point in self.points
        center = self._rectangle.center()
        ld = lu = rd = ru = False
        if point.x <= center.x:
            if point.y <= center.y:
                ld = self._left_down._if_contains(point)
            if point.y >= center.y:
                lu = self._left_up._if_contains(point)
        if point.x >= center.x:
            if point.y <= center.y:
                rd = self._right_down._if_contains(point)
            if point.y >= center.y:
                ru = self._right_up._if_contains(point)
        return ld or lu or rd or ru
    
    def _add_leaves(self, points_in_node=False):
        if points_in_node:
            return self.points
        else:
            if self._left_down is None:
                return self.points
            return self._left_down._add_leaves() + self._right_down._add_leaves() + self._right_up._add_leaves() + self._left_up._add_leaves()
        
    def _search_in_rectangle(self, rectangle, points_in_node=False):
        if self._left_up is None:
            return [point for point in self.points if rectangle.contains(point)]
        if rectangle.contains(self._rectangle):
            return self._add_leaves(points_in_node)
        if rectangle.does_intersect(self._rectangle):
            return self._left_up._search_in_rectangle(rectangle, points_in_node) + self._right_up._search_in_rectangle(rectangle, points_in_node) + self._left_down._search_in_rectangle(rectangle, points_in_node) + self._right_down._search_in_rectangle(rectangle, points_in_node)
        return []
        

# ------------------------------------------------------------------------------------------------------------------------
        
from utilities.Point import Point
from utilities.Rectangle import Rectangle
from visualizer.main import Visualizer



class QuadTree_visualizer:
    def __init__(self, points, depth=0):
        if len(points) == 0:
            raise ValueError("The list of points is empty.")
        if not all(len(point) == len(points[0]) for point in points):
            raise ValueError("The points have different dimensions.")
        points = [Point(point) for point in points]
        self.vis = Visualizer()
        self.vis.add_point(points)
        self._root = QuadTreeNode(points, Rectangle.from_points(points), depth)
        self.vis.add_polygon(self._root._rectangle.vertices2D)
        self._dimension = len(points[0])
        self._build(self._root)

    def _build(self,root):
        if root is None:
            return
        if len(root.points) < 2:
            return
        else:
            rec_left_down, rec_right_down, rec_right_up, rec_left_up = root._rectangle.to_quaters()
            self.vis.add_polygon(rec_left_down.vertices2D)
            self.vis.add_polygon(rec_right_down.vertices2D)
            self.vis.add_polygon(rec_right_up.vertices2D)
            self.vis.add_polygon(rec_left_up.vertices2D)
            points_left_up = []
            points_right_up = []
            points_left_down = []
            points_right_down = []
            for point in root.points:
                if rec_left_up.contains(point):
                    points_left_up.append(point)
                elif rec_right_up.contains(point):
                    points_right_up.append(point)
                elif rec_left_down.contains(point):
                    points_left_down.append(point)
                else:
                    points_right_down.append(point)

            root._left_up = QuadTreeNode(points_left_up, rec_left_up, root._depth + 1)
            root._right_up = QuadTreeNode(points_right_up, rec_right_up, root._depth + 1)
            root._left_down = QuadTreeNode(points_left_down, rec_left_down, root._depth + 1)
            root._right_down = QuadTreeNode(points_right_down, rec_right_down, root._depth + 1)

            self._build(root._left_up)
            self._build(root._right_up)
            self._build(root._left_down)
            self._build(root._right_down)

    def if_contains(self,point):
        if len(point) != self._dimension:
            raise ValueError("The point has different dimension than the points in the tree.")
        def search_point(root, point):
            if root is None:
                return False
            if len(root.points) == 1:
                return point == root.points[0]
            if root._rectangle.contains(point):
                return search_point(root._left_up, point) or search_point(root._right_up, point) or search_point(root._left_down, point) or search_point(root._right_down, point)
            else:
                return False
            
        return search_point(self._root, point)
        

    
    def search_in_rectangle(self, rectangle, raw = False):
        result = []

        def search(root, rectangle):
            if root is None:
                return
            if len(root.points) == 1:
                if rectangle.contains(root.points[0]):
                    result.append(root.points[0])
                else:
                    return
            intersection = root._rectangle.intersection(root._rectangle)
            if intersection != None:
                search(root._left_up, rectangle)
                search(root._right_up, rectangle)
                search(root._left_down, rectangle)
                search(root._right_down, rectangle)
            else:
                return
        search(self._root, rectangle)
        if not raw:
            return result
        else:
            for i in range(len(result)):
                result[i] = result[i]._point
            return result
