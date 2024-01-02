from utilities.Point import Point
from utilities.Rectangle import Rectangle

from copy import deepcopy

class KdTree:
    def __init__(self, points, depth=0, points_in_node=False):
        if len(points) == 0:
            raise ValueError("The list of points is empty.")
        if not all(len(point) == len(points[0]) for point in points):
            raise ValueError("The points have different dimensions.")
        points = [Point(point) for point in points]
        if len(set(points)) != len(points):
            raise ValueError("The points are not unique.")
        self._root = KdTreeNode(points, Rectangle.from_points(points), depth, points_in_node)
        self._points_in_node = points_in_node
        self._dimension = len(points[0])

    # check if the tree contains the point
    def if_contains(self, point):
        if len(point) != self._dimension:
            raise ValueError("The point has different dimension than the points in the tree.")
        if not isinstance(point, Point):
            point = Point(point)
        if self._root._rectangle.contains(point):
            return self._root._if_contains(point)
        return False
    
    # find all points in the given rectangle
    def search_in_rectangle(self, rectangle, raw=False):
        if not isinstance(rectangle, Rectangle):
            raise ValueError("The rectangle is not a Rectangle object.")
        if len(rectangle) != self._dimension:
            raise ValueError("The rectangle has different dimension than the points in the tree.")
        area = rectangle.intersection(self._root._rectangle)
        if area is None:
            return []
        result = self._root._search_rectangle(area, self._points_in_node)
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
            self._left = KdTreeNode([p for p in points if lr.contains(p)], lr, depth + 1, points_in_node)
            self._right = KdTreeNode([p for p in points if not lr.contains(p)], rr, depth + 1, points_in_node)

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
    def __init__(self, points, depth=0, points_in_node=False, visualize_gif=True, title="KdTree", filename="KdTree-construction"):
        if len(points) == 0:
            raise ValueError("The list of points is empty.")
        if not all(len(point) == len(points[0]) for point in points):
            raise ValueError("The points have different dimensions.")
        points = [Point(point) for point in points]
        if len(set(points)) != len(points):
            raise ValueError("The points are not unique.")
        self.points = [Point(point) for point in points]
        self.vis = Visualizer()
        self.vis.add_title(title)
        self.vis.add_point([(p.point) for p in self.points])
        self.scene = {}
        self._root = KdTreeNode_v(self.points, Rectangle.from_points(self.points), self.vis, self.scene, depth, points_in_node)
        if visualize_gif:
            self.vis.save_gif(filename=filename)
        else:
            self.vis.save(filename=filename)
        self._points_in_node = points_in_node
        self._dimension = len(points[0])

    # check if the tree contains the point
    def if_contains(self, point, visualize_gif=True, title="KdTree", filename="KdTree-contains"):
        if len(point) != self._dimension:
            raise ValueError("The point has different dimension than the points in the tree.")
        if not isinstance(point, Point):
            point = Point(point)
        vis = deepcopy(self.vis)
        vis.add_title(title)
        vis.add_point([(p.point) for p in self.points])
        result = self._root._if_contains(point, vis)
        if visualize_gif:
            self.vis.save_gif(filename=filename)
        else:
            self.vis.save(filename=filename)
        return result
    
    # find all points in the given rectangle
    def search_in_rectangle(self, rectangle, raw=False, visualize_gif=True, title="KdTree", filename="KdTree-search"):
        if not isinstance(rectangle, Rectangle):
            raise ValueError("The rectangle is not a Rectangle object.")
        if len(rectangle) != self._dimension:
            raise ValueError("The rectangle has different dimension than the points in the tree.")
        vis = deepcopy(self.vis)
        vis.add_title(title)
        ll, lr, ur, ul = rectangle.vertices2D
        vis.add_line_segment([(ll,lr), (ll,ul), (ul,ur),(lr,ur)], color="red")
        vis.add_point([(p.point) for p in self.points])
        result = self._root._search_rectangle(rectangle, vis, self._points_in_node)
        if visualize_gif:
            self.vis.save_gif(filename=filename)
        else:
            self.vis.save(filename=filename)
        if raw:
            return [point.point for point in result]
        return result

class KdTreeNode_v:
    def __init__(self, points, rectangle, vis, scene, depth=0, points_in_node=False):
        self.vis = vis
        self.scene = scene
        if points_in_node:
            self._points = points.copy()      # points in the node
        elif len(points) == 1:
            self._points = points             # leaf node
            vis.add_point([point.point for point in points], color="orange")  
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
            area = self.vis.add_polygon(self._rectangle.vertices2D, color="orange", alpha=0.3)
            self.vis.remove_figure(self.vis.add_point([point.point for point in points], color="red"))
            self.vis.remove_figure(area)
            self._axis = points[median][depth % len(points[median])]
            self.vis.add_line_segment([self._rectangle.opposite(points[median].point, depth%2)], color='blue')
            lr, rr = self._rectangle.divide(depth % len(self._rectangle), self._axis)
            self._left = KdTreeNode_v([p for p in points if lr.contains(p)], lr, self.vis, self.scene, depth + 1, points_in_node)
            self._right = KdTreeNode_v([p for p in points if not lr.contains(p)], rr, self.vis, self.scene, depth + 1, points_in_node)

    # check if the tree contains the point
    def _if_contains(self, point, vis):
        vis.remove_figure(vis.add_polygon(self._rectangle.vertices2D, color="orange", alpha=0.3))
        if self._axis == None:
            if point == self._points[0]:
                vis.add_point([point.point], color="green")
            else:
                vis.add_point([point.point], color="black")
            return point == self._points[0]
        if self._axis >= point[self._depth % len(point)]:
            return self._left._if_contains(point, vis)
        if self._axis < point[self._depth % len(point)]:
            return self._right._if_contains(point, vis)
        
    def _add_leaves(self, vis, points_in_node=False):
        if points_in_node:
            vis.add_point([(point.point) for point in self._points], color="black")
            return self._points
        else:
            if self._axis is None:
                vis.add_point([point.point for point in self._points], color="black")
                return self._points
            return self._left._add_leaves(vis) + self._right._add_leaves(vis)
        
    # find all points in the given rectangle 
    def _search_rectangle(self, area, vis, points_in_node=False):
        vis.remove_figure(vis.add_polygon(self._rectangle.vertices2D, color="orange", alpha=0.3))
        if self._axis is None:
            vis.add_point([point for point in self._points if area.contains(point)], color="black")
            return [point for point in self._points if area.contains(point)]
        if area.contains(self._rectangle):
            return self._add_leaves(vis, points_in_node)
        if area.does_intersect(self._rectangle):
            return self._left._search_rectangle(area, vis, points_in_node) + self._right._search_rectangle(area, vis, points_in_node)
        return []
    