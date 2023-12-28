from utilities.Point import Point
from utilities.Rectangle import Rectangle

class KdTree:
    def __init__(self, points, depth=0, points_in_node=False):
        if len(points) == 0:
            raise ValueError("The list of points is empty.")
        if not all(len(point) == len(points[0]) for point in points):
            raise ValueError("The points have different dimensions.")
        points = [Point(point) for point in points]
        self._root = KdTreeNode(points, Rectangle.from_points(points), depth, points_in_node)
        self._points_in_node = points_in_node
        self._dimension = len(points[0])

    # check if the tree contains the point
    def if_contains(self, point):
        if len(point) != self._dimension:
            raise ValueError("The point has different dimension than the points in the tree.")
        if not isinstance(point, Point):
            point = Point(point)
        return self._root._if_contains(point)
    
    # find all points in the given rectangle
    def search_in_rectangle(self, rectangle, raw=False):
        if not isinstance(rectangle, Rectangle):
            raise ValueError("The rectangle is not a Rectangle object.")
        if len(rectangle) != self._dimension:
            raise ValueError("The rectangle has different dimension than the points in the tree.")
        result = self._root._search_rectangle(rectangle, self._points_in_node)
        if raw:
            return [point.point for point in result]
        return result

class KdTreeNode:
    def __init__(self, points, rectangle, depth=0, points_in_node=False):
        if points_in_node:
            self._points = points.copy()      # points in the node
        elif len(points) == 1:
            self._points = points             # leaf node
        self._points_in_node = points_in_node # bool if points are stored in the node
        self._left = None                     # left subtree [lower or equal to the axis]
        self._right = None                    # right subtree [greater than the axis]
        self._rectangle = rectangle           # rectangle that contains all points in the node
        self._axis = None                     # axis value
        self._depth = depth                   # even: x-axis, odd: y-axis [for more than 2 dimensions, use depth % number_of_dimensions]
        self._build(points, depth, points_in_node)

    def _build(self, points, depth, points_in_node):
        if len(points) > 1:
            points.sort(key=lambda x: x[depth % len(x)])
            median = (len(points)-1) // 2
            self._axis = points[median][depth % len(points[median])]
            lr, rr = self._rectangle.divide(depth % len(self._rectangle), self._axis)
            self._left = KdTreeNode(points[:median+1], lr, depth + 1, points_in_node)
            self._right = KdTreeNode(points[median+1:], rr, depth + 1, points_in_node)

    # check if the tree contains the point
    def _if_contains(self, point):
        if self._axis == None:
            return point == self._points[0]
        if self._axis >= point[self._depth % len(point)]:
            return self._left._if_contains(point)
        if self._axis < point[self._depth % len(point)]:
            return self._right._if_contains(point)
        
    def _add_leaves(self, points_in_node=False):
        if points_in_node:
            return self._points
        else:
            if self._axis is None:
                return self._points
            return self._left._add_leaves() + self._right._add_leaves()
        
    # find all points in the given rectangle 
    def _search_rectangle(self, area, points_in_node=False):
        if self._axis is None:
            return [point for point in self._points if area.contains(point)]
        if area.contains(self._rectangle):
            return self._add_leaves(points_in_node)
        if area.does_intersect(self._rectangle):
            return self._left._search_rectangle(area, points_in_node) + self._right._search_rectangle(area, points_in_node)
        return []
    
# ----------------------------------------------------------------------------------------------------------------------------
    
from utilities.Point import Point
from utilities.Rectangle import Rectangle
from visualizer.main import Visualizer

class KdTree_visualizer:
    def __init__(self, points, depth=0, points_in_node=False, title="KdTree", filename="KdTree-construction"):
        if len(points) == 0:
            raise ValueError("The list of points is empty.")
        if not all(len(point) == len(points[0]) for point in points):
            raise ValueError("The points have different dimensions.")
        points = [Point(point) for point in points]
        self.vis = Visualizer()
        self.vis.add_title(title)
        self.vis.add_point([(p.point) for p in points])
        self.scene = {}
        self._root = KdTreeNode_v(points, Rectangle.from_points(points), self.vis, self.scene, depth, points_in_node)
        self.vis.save_gif(filename=filename)
        self._points_in_node = points_in_node
        self._dimension = len(points[0])

    # check if the tree contains the point
    def if_contains(self, point):
        if len(point) != self._dimension:
            raise ValueError("The point has different dimension than the points in the tree.")
        if not isinstance(point, Point):
            point = Point(point)
        result = self._root._if_contains(point)
        self.vis.save_gif(filename="KdTree-contain", interval=2000)
        return result
    
    # find all points in the given rectangle
    def search_in_rectangle(self, rectangle, raw=False):
        if not isinstance(rectangle, Rectangle):
            raise ValueError("The rectangle is not a Rectangle object.")
        if len(rectangle) != self._dimension:
            raise ValueError("The rectangle has different dimension than the points in the tree.")
        result = self._root._search_rectangle(rectangle, self._points_in_node)
        if raw:
            return [point.point for point in result]
        return result

class KdTreeNode_v:
    def __init__(self, points, rectangle, vis, scene, depth=0, points_in_node=False):
        self.vis = vis
        self.scene = scene
        if points_in_node:
            self._points = points.copy()      # points in the node
            vis.remove_figure(vis.add_point([point.point for point in points], color="orange"))
        elif len(points) == 1:
            self._points = points             # leaf node
            vis.remove_figure(vis.add_point([point.point for point in points], color="orange"))        
        self._points_in_node = points_in_node # bool if points are stored in the node
        self._left = None                     # left subtree [lower or equal to the axis]
        self._right = None                    # right subtree [greater than the axis]
        self._rectangle = rectangle           # rectangle that contains all points in the node
        vis.remove_figure(vis.add_polygon(rectangle.vertices2D(), color="orange", alpha=0.3))
        self._axis = None                     # axis value
        self._depth = depth                   # even: x-axis, odd: y-axis [for more than 2 dimensions, use depth % number_of_dimensions]
        self._build(points, depth, points_in_node)

    def _build(self, points, depth, points_in_node):
        if len(points) > 1:
            points.sort(key=lambda x: x[depth % len(x)])
            median = (len(points)-1) // 2
            self.vis.remove_figure(self.vis.add_point([point.point for point in points], color="red"))
            self._axis = points[median][depth % len(points[median])]
            self.vis.add_line_segment([self._rectangle.opposite(points[median].point, depth%2)], color='blue')
            lr, rr = self._rectangle.divide(depth % len(self._rectangle), self._axis)
            self._left = KdTreeNode_v(points[:median+1], lr, self.vis, self.scene, depth + 1, points_in_node)
            self._right = KdTreeNode_v(points[median+1:], rr, self.vis, self.scene, depth + 1, points_in_node)

    # check if the tree contains the point
    def _if_contains(self, point):
        if self._axis == None:
            return point == self._points[0]
        if self._axis >= point[self._depth % len(point)]:
            return self._left._if_contains(point)
        if self._axis < point[self._depth % len(point)]:
            return self._right._if_contains(point)
        
    def _add_leaves(self, points_in_node=False):
        if points_in_node:
            return self._points
        else:
            if self._axis is None:
                return self._points
            return self._left._add_leaves() + self._right._add_leaves()
        
    # find all points in the given rectangle 
    def _search_rectangle(self, area, points_in_node=False):
        if self._axis is None:
            return [point for point in self._points if area.contains(point)]
        if area.contains(self._rectangle):
            return self._add_leaves(points_in_node)
        if area.does_intersect(self._rectangle):
            return self._left._search_rectangle(area, points_in_node) + self._right._search_rectangle(area, points_in_node)
        return []
